# -*- coding: utf-8 -*-
"""Background worker for the ClimaPlots analysis pipeline.

Runs the NASA POWER fetch + climate-index computation off the GUI thread so QGIS
stays responsive. Mirrors the worker convention used by the sibling plugins
(terra_valora / AGLgis): uniform ``finished_ok`` / ``failed`` / ``progress``
signals, with the whole ``run`` body wrapped so any failure is surfaced to the UI
instead of crashing the thread.
"""
import traceback

from qgis.PyQt.QtCore import QThread, pyqtSignal

from ..services import orchestrator


class AnalysisWorker(QThread):
    """Fetch climate data and compute indices for one coordinate."""

    finished_ok = pyqtSignal(object)   # ClimateData
    failed = pyqtSignal(str)           # error message
    progress = pyqtSignal(str)         # human-readable status / per-index warning

    def __init__(self, longitude, latitude, proxy="", parent=None):
        super().__init__(parent)
        self._longitude = longitude
        self._latitude = latitude
        self._proxy = proxy

    def run(self):
        try:
            self.progress.emit("Fetching climate data from NASA POWER...")
            data = orchestrator.run_analysis(
                self._longitude, self._latitude, self._proxy,
                warn=lambda msg: self.progress.emit(msg),
            )
            self.finished_ok.emit(data)
        except Exception:  # noqa: BLE001 - surface any failure to the UI
            self.failed.emit(traceback.format_exc())
