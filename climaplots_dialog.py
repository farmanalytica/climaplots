# -*- coding: utf-8 -*-
"""
ClimaPlots dialog shell.

This module owns the dialog window and UI behaviour only: widget setup, signal
wiring, navigation and rendering. The heavy work is delegated:

  * ``services/``  - NASA POWER fetch, climate indices, stats, figure building.
  * ``workers/``   - the QThread that runs fetch + indices off the GUI thread.
  * ``view/plotly_view`` - renders plotly figures into the QtWebKit web views.

Keeping logic out of here mirrors the sibling plugins (qgis-EasyDEM,
terra_valora) and the QtWebKit/plotly fix mirrors qgis-AGLgis.
"""
import os

import qgis
from qgis.core import QgsApplication, QgsMessageLog, Qgis
from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt, QSettings, QTimer
from qgis.PyQt.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)
import webbrowser

from .modules import map_tools, save_utils
from .mouse_events import Delete_Marker
from .services import plot_service, settings_manager
from .view import plotly_view
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

# Load the UI matching the user locale.
_language = QSettings().value("locale/userLocale", "en")[0:2]
_ui_name = "climaplots_dialog_base_pt.ui" if _language == "pt" else "climaplots_dialog_base.ui"
FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), "ui", _ui_name))


class ClimaPlotsDialog(QDialog, FORM_CLASS):
    """Main dialog: input on tab 0, three plotly visualizations on tabs 1+."""

    def __init__(self, parent=None, iface=None):
        super(ClimaPlotsDialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface

        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowCloseButtonHint
            | Qt.WindowType.WindowMinimizeButtonHint
            | Qt.WindowType.WindowMaximizeButtonHint
        )
        self.setModal(False)

        self.focus_timer = QTimer()
        self.focus_timer.timeout.connect(self.check_focus)
        QTimer.singleShot(0, lambda: self.resizeEvent("small"))

        self._populate_variable_dropdown()
        self._setup_climate_indices()

        # State
        self.climate_data = None            # services.types.ClimateData
        self._worker = None                 # AnalysisWorker
        self._figs = {1: None, 2: None, 3: None}      # for "open in browser"
        self._save_data = {1: None, 2: None, 3: None}  # DataFrames for CSV export
        self._tmp_paths = {1: None, 2: None, 3: None}  # temp html per web view

        self._connect_ui_signals()
        self.language = QgsApplication.instance().locale()[:2]
        self.tabWidget.setCurrentIndex(0)

    # ------------------------------------------------------------------ setup
    def _connect_ui_signals(self):
        self.tabWidget.currentChanged.connect(self.on_tab_changed)
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

    def _populate_variable_dropdown(self):
        for name in ["Max Temperature", "Min Temperature", "Precipitation",
                     "Relative Humidity", "Irradiation"]:
            self.atributo.addItem(name)

    def _setup_climate_indices(self):
        sheet_names = [
            "Annual Summer Days", "Annual Frost Days", "Annual Tropical Nights",
            "Annual Icing Days", "Monthly Maximum Temperature",
            "Monthly Minimum Temperature of Maximum Temperatures",
            "Monthly Maximum Temperature of Minimum Temperatures",
            "Monthly Minimum Temperature", "Daily Temperature Range",
            "Monthly Maximum 1-day Precipitation", "Monthly Maximum 5-day Precipitation",
            "Annual Count of Days when Precipitation Exceeds 10mm",
            "Annual Count of Days when Precipitation Exceeds 20mm",
            "Simple Precipitation Intensity Index",
            "Number of Consecutive Dry Days in a Month",
            "Number of Consecutive Wet Days in a Month",
            "The Standardized Precipitation Index (SPI)",
        ]
        for name in sheet_names:
            self.atributo_2.addItem(name)
        self.atributo_2.setCurrentIndex(0)

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
        self.tabWidget.setCurrentIndex(1)

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
        try:
            canvas = getattr(self, "canvas", None) or (self.iface.mapCanvas() if self.iface else None)
            markers = getattr(self, "Markers", None)
            if canvas and markers:
                Delete_Marker(canvas, markers)
        except Exception:
            pass

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
        if not hasattr(self, "_size_locked"):
            self.resizeEvent("small")
            self._size_locked = True
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

    def on_tab_changed(self, index):
        self.resizeEvent("big" if index != 0 else "small")

    def resizeEvent(self, event):
        self.setMinimumSize(0, 0)
        self.setMaximumSize(16777215, 16777215)
        if event == "small":
            self.resize(402, 210)
            self.setFixedSize(self.width(), self.height())
        elif event == "big":
            self.resize(945, 535)
            self.setFixedSize(self.width(), self.height())

    def fun_fechou(self):
        self.LongEdit.clear()
        self.LatEdit.clear()
        self.tabWidget.setCurrentIndex(0)
        qgis.utils.iface.actionPan().trigger()
        self._remove_markers()

    def _remove_markers(self):
        try:
            canvas = getattr(self, "canvas", None) or (self.iface.mapCanvas() if hasattr(self, "iface") and self.iface else None)
            markers = getattr(self, "Markers", None)
            if canvas and markers:
                Delete_Marker(canvas, markers)
        except Exception:
            pass
