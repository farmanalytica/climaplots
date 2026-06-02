# -*- coding: utf-8 -*-
"""
ClimaPlots dialog shell (pure-Qt UI, English only).

The window is a left :class:`~view.sidebar.Sidebar` + a ``QStackedWidget`` of
pages (Intro / Coordinates / Trends / Thermo-pluviometric / Indices). The UI is
built by the ``view/pages.py`` ``setup_*_page`` builders, which attach the
interactive widgets onto this dialog; this module owns only behaviour: signal
wiring, navigation, worker orchestration and rendering. The heavy work is
delegated:

  * ``services/``  - NASA POWER fetch, climate indices, stats, figure building.
  * ``workers/``   - the QThread that runs fetch + indices off the GUI thread.
  * ``view/plotly_view`` - renders plotly figures into the QtWebKit web views.

Structure mirrors the sibling plugins (qgis-EasyDEM, terra_valora) and the
QtWebKit/plotly fix mirrors qgis-AGLgis.
"""
import qgis
from qgis.core import QgsApplication, QgsMessageLog, Qgis
from qgis.PyQt.QtCore import Qt, QTimer
from qgis.PyQt.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)
import webbrowser

from .modules import map_tools, save_utils
from .modules.canvas_click_tool import CanvasClickTool
from .services import plot_service, settings_manager
from .view import Sidebar, pages, plotly_view
from .view.styles import STYLE_DIALOG
from .workers import AnalysisWorker

# Plotly chart config (toolbar trimmed) shared by all three views.
_PLOT_CONFIG = {
    "displaylogo": False,
    "responsive": True,
    "modeBarButtonsToRemove": [
        "toImage", "sendDataToCloud", "zoom2d", "pan2d", "select2d",
        "lasso2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
        "hoverClosestCartesian", "hoverCompareCartesian", "zoom3d", "pan3d",
        "orbitRotation", "tableRotation", "resetCameraLastSave",
        "resetCameraDefault3d", "hoverClosest3d", "zoomInGeo", "zoomOutGeo",
        "resetGeo", "hoverClosestGeo", "hoverClosestGl2d", "hoverClosestPie",
        "toggleHover", "toggleSpikelines", "resetViews",
    ],
}

_LOADING_HTML = (
    "<html><body style='font-family:sans-serif;color:#555;text-align:center;"
    "margin-top:40px'><h3>Fetching climate data...</h3></body></html>"
)


class ClimaPlotsDialog(QDialog):
    """Sidebar-navigated dialog with an intro page and three plotly views."""

    def __init__(self, parent=None, iface=None):
        super(ClimaPlotsDialog, self).__init__(parent)
        self.iface = iface

        self._build_ui()

        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowCloseButtonHint
            | Qt.WindowType.WindowMinimizeButtonHint
            | Qt.WindowType.WindowMaximizeButtonHint
        )
        self.setModal(False)

        self.focus_timer = QTimer()
        self.focus_timer.timeout.connect(self.check_focus)

        # Map-click capture ("clicking mode"); needs a live iface.
        self.click_tool = CanvasClickTool(iface) if iface is not None else None

        # State
        self.climate_data = None            # services.types.ClimateData
        self._worker = None                 # AnalysisWorker
        self._figs = {1: None, 2: None, 3: None}      # for "open in browser"
        self._save_data = {1: None, 2: None, 3: None}  # DataFrames for CSV export
        self._tmp_paths = {1: None, 2: None, 3: None}  # temp html per web view

        self._connect_ui_signals()
        self.language = QgsApplication.instance().locale()[:2]
        self._goto("intro")

    # ----------------------------------------------------------------- build UI
    def _build_ui(self):
        """Sidebar + QStackedWidget of pages, built by the view/pages builders."""
        self.setWindowTitle("ClimaPlots")
        self.setStyleSheet(STYLE_DIALOG)
        self.resize(1000, 560)

        self.sidebar = Sidebar(self)
        self.stack = QStackedWidget(self)

        self.intro_page = QWidget()
        self.coords_page = QWidget()
        self.trends_page = QWidget()
        self.thermo_page = QWidget()
        self.indices_page = QWidget()

        pages.setup_intro_page(self, self.intro_page)
        pages.setup_coordinates_page(self, self.coords_page)
        pages.setup_trends_page(self, self.trends_page)
        pages.setup_thermo_page(self, self.thermo_page)
        pages.setup_indices_page(self, self.indices_page)

        for p in (self.intro_page, self.coords_page, self.trends_page,
                  self.thermo_page, self.indices_page):
            self.stack.addWidget(p)

        self._page_for = {
            "intro": self.intro_page, "coords": self.coords_page,
            "trends": self.trends_page, "thermo": self.thermo_page,
            "indices": self.indices_page,
        }

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self.sidebar)
        root.addWidget(self.stack, 1)

    def _connect_ui_signals(self):
        self.sidebar.intro_requested.connect(lambda: self._goto("intro"))
        self.sidebar.coords_requested.connect(lambda: self._goto("coords"))
        self.sidebar.trends_requested.connect(lambda: self._goto("trends"))
        self.sidebar.thermo_requested.connect(lambda: self._goto("thermo"))
        self.sidebar.indices_requested.connect(lambda: self._goto("indices"))

        self.navegador.clicked.connect(lambda: self._open_in_browser(1))
        self.navegador_2.clicked.connect(lambda: self._open_in_browser(2))
        self.navegador_3.clicked.connect(lambda: self._open_in_browser(3))
        self.save_plot.clicked.connect(self.save_clicked)
        self.save_plot2.clicked.connect(self.save_clicked2)
        self.save_plot3.clicked.connect(self.save_clicked3)
        self.save_raw.clicked.connect(self.save_raw_clicked)
        self.rejected.connect(self.fun_fechou)
        self.gerar_req.clicked.connect(self.request_api)
        self.atributo.currentTextChanged.connect(self.plots1)
        self.atributo_2.currentTextChanged.connect(self.plots3)
        self.googlemaps.clicked.connect(map_tools.hybrid_function)
        self.proxy.clicked.connect(self.open_proxy_dialog)
        self.learn.clicked.connect(self.open_learn_dialog)

        if self.click_tool is not None:
            self.pick_point.toggled.connect(self._toggle_pick)
            self.click_tool.point_picked.connect(self._on_point_picked)
        else:
            self.pick_point.setEnabled(False)

    # --------------------------------------------------------------- navigation
    def _goto(self, page_key):
        """Switch the stack + sidebar highlight to ``page_key``."""
        page = self._page_for[page_key]
        self.stack.setCurrentWidget(page)
        self.sidebar.set_active_page(page_key)

    def _on_get_started(self):
        self._goto("coords")

    def on_input_page(self):
        """True when the coordinate-input page is showing (gates map markers)."""
        return self.stack.currentWidget() is self.coords_page

    # ----------------------------------------------------------- clicking mode
    def _toggle_pick(self, enabled):
        """Enter/leave map-click capture mode from the toggle button."""
        if self.click_tool is None:
            return
        if enabled:
            self.click_tool.enable()
        else:
            self.click_tool.disable()

    def _on_point_picked(self, longitude, latitude):
        """A point was clicked: fill the fields and pop the toggle off."""
        self.LongEdit.setText(str(longitude))
        self.LatEdit.setText(str(latitude))
        if self.pick_point.isChecked():
            self.pick_point.setChecked(False)  # tool already auto-disabled

    # -------------------------------------------------------------- data flow
    def request_api(self):
        """Start the background analysis for the entered coordinates."""
        if self._worker is not None and self._worker.isRunning():
            return  # re-entrancy guard

        if not self.LongEdit.text().strip() or not self.LatEdit.text().strip():
            QMessageBox.warning(self, "Missing coordinates",
                                "Click a point on the map (or enter Longitude/Latitude) first.")
            return

        self._reset_results()
        QApplication.setOverrideCursor(Qt.WaitCursor)
        for view in (self.webView_1, self.webView_2, self.webView_3):
            try:
                view.setHtml(_LOADING_HTML)
            except Exception:
                pass

        self._worker = AnalysisWorker(
            self.LongEdit.text(), self.LatEdit.text(), settings_manager.get_proxy(), self
        )
        self._worker.finished_ok.connect(self._on_analysis_done)
        self._worker.failed.connect(self._on_analysis_failed)
        self._worker.progress.connect(self._on_progress)
        self._worker.finished.connect(self._cleanup_worker)
        self._worker.start()

    def _on_progress(self, message):
        QgsMessageLog.logMessage(message, "ClimaPlots", Qgis.Info)

    def _on_analysis_done(self, data):
        """Render all three plots from the worker result (GUI thread)."""
        QApplication.restoreOverrideCursor()
        self.climate_data = data
        self.plots1()
        self.plots2()
        self.plots3()
        self._goto("trends")

    def _on_analysis_failed(self, message):
        QApplication.restoreOverrideCursor()
        QgsMessageLog.logMessage(message, "ClimaPlots", Qgis.Critical)
        QMessageBox.warning(self, "ClimaPlots",
                            "Failed to fetch or process climate data.\nSee the QGIS log for details.")
        for tab in (1, 2, 3):
            self._tmp_paths_clear(tab)

    def _cleanup_worker(self):
        if self._worker is not None:
            self._worker.deleteLater()
            self._worker = None

    def _reset_results(self):
        self.climate_data = None
        for tab in (1, 2, 3):
            self._figs[tab] = None
            self._save_data[tab] = None
            self._tmp_paths_clear(tab)
        if self.click_tool is not None:
            self.click_tool.clear_marker()

    # ----------------------------------------------------------- plot rendering
    def plots1(self):
        self._render(1, self.webView_1,
                     lambda d: plot_service.annual_trends(
                         d.df, self.atributo.currentText(), d.longitude, d.latitude))

    def plots2(self):
        self._render(2, self.webView_2,
                     lambda d: plot_service.thermopluviometric(d.df, d.longitude, d.latitude))

    def plots3(self):
        self._render(3, self.webView_3,
                     lambda d: plot_service.index_plot(
                         d.indices, self.atributo_2.currentText(), d.longitude, d.latitude))

    def _render(self, tab, web_view, builder):
        """Build a figure with ``builder(climate_data)`` and show it in ``web_view``."""
        if self.climate_data is None:
            return
        try:
            result = builder(self.climate_data)
        except plot_service.PlotDataError as e:
            QMessageBox.warning(self, "Data not available", str(e))
            return
        except Exception as e:  # noqa: BLE001
            QgsMessageLog.logMessage(f"Plot {tab} failed: {e}", "ClimaPlots", Qgis.Warning)
            return
        self._figs[tab] = result.figure
        self._save_data[tab] = result.data
        self._tmp_paths[tab] = plotly_view.show_in_webview(
            web_view, result.figure, _PLOT_CONFIG, self._tmp_paths.get(tab)
        )

    def _open_in_browser(self, tab):
        fig = self._figs.get(tab)
        if fig is not None:
            plotly_view.open_in_browser(fig, dict(_PLOT_CONFIG, modeBarButtonsToRemove=[]))

    def _web_view(self, tab):
        return {1: self.webView_1, 2: self.webView_2, 3: self.webView_3}[tab]

    def _tmp_paths_clear(self, tab):
        self._tmp_paths[tab] = plotly_view.clear_webview(self._web_view(tab), self._tmp_paths.get(tab))

    # --------------------------------------------------------------- save (CSV)
    def save_clicked(self):
        save_utils.save(self._save_data[1], f"Anual_trends_{self.atributo.currentText()}.csv", self)

    def save_clicked2(self):
        save_utils.save(self._save_data[2], "Thermopluviometric.csv", self)

    def save_clicked3(self):
        save_utils.save(self._save_data[3], f"{self.atributo_2.currentText()}.csv", self)

    def save_raw_clicked(self):
        df = self.climate_data.df if self.climate_data else None
        save_utils.save(df, "Raw_data.csv", self)

    # ------------------------------------------------------------------ dialogs
    def open_proxy_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Proxy Settings")
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel("Enter proxy (e.g. http://user:pass@host:port):"))
        proxy_edit = QLineEdit()
        proxy_edit.setText(settings_manager.get_proxy())
        layout.addWidget(proxy_edit)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(buttons)

        def accept():
            settings_manager.set_proxy(proxy_edit.text())
            dialog.accept()

        buttons.accepted.connect(accept)
        buttons.rejected.connect(dialog.reject)
        dialog.exec_()

    def open_learn_dialog(self):
        webbrowser.open("https://caioarantes.github.io/climaplots/")

    # ------------------------------------------------------------ window events
    def showEvent(self, event):
        super().showEvent(event)
        if hasattr(self, "focus_timer"):
            self.focus_timer.start(100)

    def hideEvent(self, event):
        super().hideEvent(event)
        if hasattr(self, "focus_timer"):
            try:
                self.focus_timer.stop()
            except RuntimeError:
                pass
        self._remove_markers()

    def check_focus(self):
        if not self.isVisible() or self.isMinimized():
            return
        active_window = QApplication.activeWindow()
        if (active_window == self.iface.mainWindow()
                and not QApplication.activeModalWidget()
                and not self.isActiveWindow()):
            self.raise_()

    def closeEvent(self, event):
        if hasattr(self, "focus_timer"):
            try:
                self.focus_timer.stop()
            except RuntimeError:
                pass
        self._remove_markers()
        self.hide()
        event.ignore()

    def fun_fechou(self):
        self.LongEdit.clear()
        self.LatEdit.clear()
        self._goto("coords")
        qgis.utils.iface.actionPan().trigger()
        self._remove_markers()

    def _remove_markers(self):
        """Clear the canvas marker and leave capture mode (restores map tool)."""
        if self.click_tool is not None:
            self.click_tool.clear_marker()
            self.click_tool.disable()
        if hasattr(self, "pick_point") and self.pick_point.isChecked():
            self.pick_point.setChecked(False)
