# -*- coding: utf-8 -*-
"""External dependency manager for ClimaPlots.

The plugin's scientific stack (xarray, pymannkendall, pyhomogeneity, climdex
and their compiled dependencies) is not shipped inside the repository. Instead
it is downloaded once as ``extlibs.zip`` and unpacked into ``extlibs/`` next to
this file, mirroring the qgis-EasyDEM plugin.

Unlike EasyDEM, ClimaPlots imports its dependencies eagerly at module load, so
``ensure_ready()`` blocks (with a progress dialog) until the libraries are on
disk before ``classFactory`` imports them.
"""
import os
import sys
import zipfile
import urllib.request

from qgis.PyQt.QtCore import QThread, pyqtSignal

EXTLIBS_URL = "https://github.com/farmanalytica/climaplots/raw/main/extlibs.zip"
_PLUGIN_DIR = os.path.dirname(__file__)
EXTLIBS_PATH = os.path.join(_PLUGIN_DIR, "extlibs")
_SENTINEL = os.path.join(EXTLIBS_PATH, ".ready")

_downloader = None


def is_ready():
    # Sentinel from a download, OR a pre-existing populated extlibs dir
    # (e.g. an install that still ships the unzipped libraries). The xarray
    # package is one of the required dependencies and a reliable marker.
    if os.path.isfile(_SENTINEL):
        return True
    return os.path.isdir(os.path.join(EXTLIBS_PATH, "xarray"))


def ensure_on_path():
    if EXTLIBS_PATH not in sys.path:
        sys.path.insert(0, EXTLIBS_PATH)


def _download_and_extract():
    """Fetch extlibs.zip and unpack it into EXTLIBS_PATH. Blocking."""
    zip_path = os.path.join(_PLUGIN_DIR, "extlibs.zip")
    try:
        if not EXTLIBS_URL.startswith("https://"):
            raise ValueError(f"Unexpected URL scheme: {EXTLIBS_URL}")
        with urllib.request.urlopen(EXTLIBS_URL) as resp, open(zip_path, "wb") as f:  # nosec B310
            f.write(resp.read())
        with zipfile.ZipFile(zip_path, "r") as zf:
            names = zf.namelist()
            if names and names[0].startswith("extlibs/"):
                zf.extractall(_PLUGIN_DIR)
            else:
                os.makedirs(EXTLIBS_PATH, exist_ok=True)
                zf.extractall(EXTLIBS_PATH)
        open(_SENTINEL, "w").close()
        ensure_on_path()
    finally:
        if os.path.exists(zip_path):
            try:
                os.remove(zip_path)
            except OSError:
                pass


def ensure_ready(parent=None):
    """Make sure extlibs are present, downloading them if needed.

    Blocks until the libraries are available so the caller can import them
    immediately. Returns True on success, False on failure (a message box is
    shown to the user on failure). Safe to call every load; it is a no-op once
    the ``.ready`` sentinel exists.
    """
    ensure_on_path()
    if is_ready():
        return True

    from qgis.PyQt.QtWidgets import QApplication, QMessageBox, QProgressDialog
    from qgis.PyQt.QtCore import Qt

    dlg = QProgressDialog(
        "Baixando dependências do ClimaPlots...\n(apenas na primeira execução)",
        None, 0, 0, parent,
    )
    dlg.setWindowTitle("ClimaPlots")
    dlg.setWindowModality(Qt.WindowModal)
    dlg.setMinimumDuration(0)
    dlg.setCancelButton(None)
    dlg.show()
    QApplication.processEvents()
    try:
        _download_and_extract()
        return True
    except Exception as e:  # noqa: BLE001 - surface any failure to the user
        QMessageBox.critical(
            parent, "ClimaPlots",
            "Falha ao baixar as dependências externas.\n\n"
            f"Erro: {e}\n\nURL: {EXTLIBS_URL}",
        )
        return False
    finally:
        dlg.close()


# --- Async parity with qgis-EasyDEM (kept for callers that prefer it) ---------
def get_downloader():
    return _downloader


def start_download():
    global _downloader
    if _downloader is not None and _downloader.isRunning():
        return _downloader
    _downloader = ExtlibsDownloader()
    _downloader.start()
    return _downloader


class ExtlibsDownloader(QThread):
    download_done = pyqtSignal(bool, str)  # success, error_msg

    def run(self):
        try:
            _download_and_extract()
            self.download_done.emit(True, "")
        except Exception as e:
            self.download_done.emit(False, str(e))
