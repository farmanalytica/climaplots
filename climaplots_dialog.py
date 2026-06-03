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
from qgis.PyQt.QtCore import QCoreApplication, Qt, QTimer
from qgis.PyQt.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)
import webbrowser

from .modules import map_tools, save_utils
from .modules.canvas_click_tool import CanvasClickTool
from .services import export_service, plot_service, settings_manager
from .view import Sidebar, pages, plotly_view
from .view.styles import STYLE_BTN_HELP, STYLE_BTN_SUBTLE, STYLE_DIALOG
from .workers import AnalysisWorker


def _tr(text):
    return QCoreApplication.translate("ClimaPlots", text)

# Header page-title shown per page (mirrors AGLgis's dynamic header title).
_PAGE_TITLES = {
    "intro": "Welcome",
    "coords": "Select coordinates",
    "trends": "Annual trends",
    "thermo": "Thermo-pluviometric diagram",
    "indices": "Climate indices",
}

# Per-page window size (w, h). Coordinates stays small so more of the map
# canvas remains visible while picking a point; plot pages open wide.
_PAGE_SIZES = {
    "intro": (820, 560),
    "coords": (470, 520),
    "trends": (1020, 620),
    "thermo": (1020, 620),
    "indices": (1020, 620),
}

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

def _loading_html():
    return (
        "<html><body style='font-family:sans-serif;color:#555;text-align:center;"
        "margin-top:40px'><h3>" + _tr("Fetching climate data...") + "</h3></body></html>"
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
        self._coords_visited = False        # auto-enable pick on first visit

        self._connect_ui_signals()
        self._update_var_desc()
        self._update_index_desc()
        self.language = QgsApplication.instance().locale()[:2]
        self._goto("intro")

    # ----------------------------------------------------------------- build UI
    def _build_ui(self):
        """Sidebar + QStackedWidget of pages, built by the view/pages builders."""
        self.setWindowTitle("ClimaPlots")
        self.setStyleSheet(STYLE_DIALOG)

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
            # Ignored size policy so the QStackedWidget sizes to the *current*
            # page only; otherwise the small coordinates page could not shrink
            # below the wide plot pages. The active page is restored to
            # Expanding in _goto().
            p.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self._page_for = {
            "intro": self.intro_page, "coords": self.coords_page,
            "trends": self.trends_page, "thermo": self.thermo_page,
            "indices": self.indices_page,
        }

        # Top header bar (brand | page title ............ help), then the body
        # (sidebar + stacked pages) below it.
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        body.addWidget(self.sidebar)
        body.addWidget(self.stack, 1)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self._build_header())
        root.addLayout(body, 1)

    def _build_header(self):
        """Fixed-height top bar: brand + dynamic page title + help button."""
        header = QWidget()
        header.setFixedHeight(40)
        header.setObjectName("climaHeader")
        header.setStyleSheet(
            "QWidget#climaHeader { background-color: #ffffff; "
            "border-bottom: 1px solid #e3e9ef; }"
        )
        lay = QHBoxLayout(header)
        lay.setContentsMargins(20, 0, 16, 0)
        lay.setSpacing(0)

        brand = QLabel("ClimaPlots")
        brand.setStyleSheet("color: #1c3d5a; font-size: 13px; font-weight: bold; letter-spacing: 0.5px;")
        lay.addWidget(brand)

        sep = QLabel("  |")
        sep.setStyleSheet("color: #d0d9e2; font-size: 16px;")
        lay.addWidget(sep)

        self._header_title = QLabel(_tr(_PAGE_TITLES["intro"]))
        self._header_title.setStyleSheet("color: #5b6b7b; font-size: 13px; margin-left: 6px;")
        lay.addWidget(self._header_title)

        lay.addStretch()

        # Proxy settings tucked into the top-right corner (subtle link style).
        self.proxy = QPushButton(_tr("Proxy settings"))
        self.proxy.setCursor(Qt.CursorShape.PointingHandCursor)
        self.proxy.setStyleSheet(STYLE_BTN_SUBTLE)
        self.proxy.setToolTip(_tr("Proxy setting (only if required by your network provider)"))
        lay.addWidget(self.proxy)

        help_btn = QPushButton("?")
        help_btn.setFixedSize(28, 28)
        help_btn.setToolTip(_tr("Learn more about this plugin"))
        help_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        help_btn.setStyleSheet(STYLE_BTN_HELP)
        help_btn.clicked.connect(self.open_learn_dialog)
        lay.addWidget(help_btn)
        return header

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
        self.atributo.currentTextChanged.connect(self._update_var_desc)
        self.atributo_2.currentTextChanged.connect(self.plots3)
        self.atributo_2.currentTextChanged.connect(self._update_index_desc)
        self.googlemaps.clicked.connect(map_tools.hybrid_function)
        self.proxy.clicked.connect(self.open_proxy_dialog)
        self.clear_mark.clicked.connect(self._clear_marker)
        self.save_img.clicked.connect(lambda: self._save_png(1))
        self.save_img2.clicked.connect(lambda: self._save_png(2))
        self.save_img3.clicked.connect(lambda: self._save_png(3))
        self.export_all.clicked.connect(self._export_all)

        if self.click_tool is not None:
            self.pick_point.toggled.connect(self._toggle_pick)
            self.pick_point_b.toggled.connect(self._toggle_pick_b)
            self.click_tool.point_picked.connect(self._on_point_picked)
        else:
            self.pick_point.setEnabled(False)
            self.pick_point_b.setEnabled(False)

    # --------------------------------------------------------------- navigation
    def _goto(self, page_key):
        """Switch the stack + sidebar highlight to ``page_key``."""
        page = self._page_for[page_key]
        for p in self._page_for.values():
            p.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stack.setCurrentWidget(page)
        self.sidebar.set_active_page(page_key)
        self._header_title.setText(_tr(_PAGE_TITLES.get(page_key, "")))
        self.proxy.setVisible(page_key == "intro")
        if page_key in _PAGE_SIZES:
            self.resize(*_PAGE_SIZES[page_key])
        # Auto-enable map-click capture the first time the user opens the
        # coordinates page, so they can pick a point straight away.
        if (page_key == "coords" and self.click_tool is not None
                and not self._coords_visited):
            self._coords_visited = True
            self.pick_point.setChecked(True)  # triggers _toggle_pick -> enable

    def _on_get_started(self):
        self._goto("coords")

    def on_input_page(self):
        """True when the coordinate-input page is showing (gates map markers)."""
        return self.stack.currentWidget() is self.coords_page

    # ----------------------------------------------------------- clicking mode
    def _save_png(self, tab):
        """Grab the rendered chart from its web view and save as PNG."""
        if self._figs.get(tab) is None:
            return
        name = {1: "annual_trends", 2: "thermo_pluviometric", 3: "climate_index"}[tab]
        path, _ = QFileDialog.getSaveFileName(
            self, _tr("Save image"), name + ".png", "PNG (*.png)")
        if path:
            self._web_view(tab).grab().save(path)

    def _export_all(self):
        """Export raw data, annual/thermo tables and all indices to one file."""
        if self.climate_data is None:
            QMessageBox.warning(self, "ClimaPlots", _tr("Run an analysis first."))
            return
        path, _ = QFileDialog.getSaveFileName(
            self, _tr("Export all"), "climaplots.xlsx", "Excel (*.xlsx)")
        if not path:
            return
        try:
            out = export_service.export(path, self.climate_data, self._save_data)
            QMessageBox.information(self, "ClimaPlots", _tr("Saved:") + " " + out)
        except Exception as e:  # noqa: BLE001
            QMessageBox.warning(self, "ClimaPlots", _tr("Export failed.") + "\n" + str(e))

    def _clear_marker(self):
        if self.click_tool is not None:
            self.click_tool.clear_marker()

    def _update_var_desc(self):
        self.var_desc.setText(_tr(pages.variable_description(self.atributo.currentText())))

    def _update_index_desc(self):
        self.index_desc.setText(_tr(pages.index_description(self.atributo_2.currentText())))

    def _toggle_pick(self, enabled):
        """Enter/leave map-click capture mode for point A."""
        self.pick_point.setText(_tr(pages.PICK_TEXT_ON if enabled else pages.PICK_TEXT_OFF))
        if self.click_tool is None:
            return
        if enabled:
            if self.pick_point_b.isChecked():
                self.pick_point_b.setChecked(False)
            self.click_tool.enable("A")
        else:
            self.click_tool.disable()

    def _toggle_pick_b(self, enabled):
        """Enter/leave map-click capture mode for the comparison point B."""
        self.pick_point_b.setText(_tr(pages.PICK_B_ON if enabled else pages.PICK_B_OFF))
        if self.click_tool is None:
            return
        if enabled:
            if self.pick_point.isChecked():
                self.pick_point.setChecked(False)
            self.click_tool.enable("B")
        else:
            self.click_tool.disable()

    def _on_point_picked(self, longitude, latitude, slot="A"):
        """A point was clicked: fill the matching fields; capture mode stays on."""
        if slot == "B":
            self.LongEditB.setText(str(longitude))
            self.LatEditB.setText(str(latitude))
        else:
            self.LongEdit.setText(str(longitude))
            self.LatEdit.setText(str(latitude))

    # -------------------------------------------------------------- data flow
    def request_api(self):
        """Start the background analysis for the entered coordinates."""
        if self._worker is not None and self._worker.isRunning():
            return  # re-entrancy guard

        if not self.LongEdit.text().strip() or not self.LatEdit.text().strip():
            QMessageBox.warning(self, _tr("Missing coordinates"),
                                _tr("Click a point on the map (or enter Longitude/Latitude) first."))
            return

        self._reset_results()
        QApplication.setOverrideCursor(Qt.WaitCursor)
        for view in (self.webView_1, self.webView_2, self.webView_3):
            try:
                view.setHtml(_loading_html())
            except Exception:
                pass

        self._worker = AnalysisWorker(
            self.LongEdit.text(), self.LatEdit.text(), settings_manager.get_proxy(),
            start_year=self.start_year.value(), end_year=self.end_year.value(),
            longitude_b=self.LongEditB.text().strip() or None,
            latitude_b=self.LatEditB.text().strip() or None,
            source=self.source_combo.currentData() or "power",
            source_b=self.source_combo_b.currentData(),
            parent=self,
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
        # The map marker is intentionally kept across runs (use "Clear marker").

    # ----------------------------------------------------------- plot rendering
    def plots1(self):
        self._render(1, self.webView_1,
                     lambda d: plot_service.annual_trends(
                         d.df, self.atributo.currentText(), d.longitude, d.latitude,
                         df_b=d.df_b, longitude_b=d.longitude_b, latitude_b=d.latitude_b,
                         source=d.source, source_b=d.source_b))

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
            QMessageBox.warning(self, _tr("Data not available"), str(e))
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
        dialog.setWindowTitle(_tr("Proxy Settings"))
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel(_tr("Enter proxy (e.g. http://user:pass@host:port):")))
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
