# -*- coding: utf-8 -*-
"""Provision third-party Python deps not bundled with QGIS, matching the
running interpreter.

ClimaPlots needs xarray, pymannkendall, pyhomogeneity, climdex and their
compiled dependencies (e.g. bottleneck). Those are NOT shipped with QGIS and
the compiled ones are ABI-locked to the Python version, so a single bundle
breaks when QGIS ships a different Python. numpy/pandas/scipy/requests/plotly
DO come with QGIS and must never be shadowed from extlibs/.

Strategy, in order:
  1. Download a prebuilt zip tagged for this Python+platform
     (``extlibs-<cpXY>-<platform>.zip``).
  2. Fall back to running the QGIS Python's pip to install into ``extlibs/``.
  3. Otherwise report failure (the dialog shows manual instructions).

The active build is recorded in ``extlibs/.ready`` together with its tag, so a
QGIS Python upgrade (different tag) re-provisions automatically.

ClimaPlots imports its dependencies eagerly at module load, so ``ensure_ready()``
blocks (with a progress dialog) until the libraries are on disk before
``classFactory`` imports them.
"""
import importlib
import os
import shutil
import subprocess
import sys
import sysconfig
import urllib.request
import zipfile

from qgis.PyQt.QtCore import QThread, pyqtSignal

BASE_URL = "https://github.com/farmanalytica/climaplots/raw/main/"
_PLUGIN_DIR = os.path.dirname(__file__)
EXTLIBS_PATH = os.path.join(_PLUGIN_DIR, "extlibs")
_SENTINEL = os.path.join(EXTLIBS_PATH, ".ready")
_REQUIREMENTS = os.path.join(_PLUGIN_DIR, "requirements.txt")

# Deps shipped with QGIS itself — never keep them in extlibs/ (ABI shadowing).
_QGIS_PROVIDED = (
    "numpy", "pandas", "scipy", "matplotlib", "requests", "certifi",
    "urllib3", "idna", "charset_normalizer", "plotly",
)

_downloader = None


def current_tag() -> str:
    """e.g. 'cp312-win_amd64' for the running interpreter."""
    plat = sysconfig.get_platform().replace("-", "_").replace(".", "_")
    return f"cp{sys.version_info.major}{sys.version_info.minor}-{plat}"


def _read_ready_tag():
    try:
        with open(_SENTINEL, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return None


def is_ready() -> bool:
    """Provisioned for THIS interpreter (tag matches)."""
    if not os.path.isdir(EXTLIBS_PATH):
        return False
    tag = _read_ready_tag()
    if tag is not None:
        # Legacy sentinels were empty; treat empty as ready (old single-target build).
        return tag in ("", current_tag())
    # No sentinel — accept a pre-existing populated extlibs dir (e.g. an install
    # that still ships the unzipped libraries). xarray is a reliable marker.
    return os.path.isdir(os.path.join(EXTLIBS_PATH, "xarray"))


def ensure_on_path():
    if EXTLIBS_PATH not in sys.path:
        sys.path.insert(0, EXTLIBS_PATH)
    # __init__.py may have inserted EXTLIBS_PATH while the dir was still empty
    # (pre-provision), poisoning Python's path-finder cache for that directory.
    importlib.invalidate_caches()


def _python_executable():
    """Best-effort path to the QGIS Python interpreter (not the GUI binary)."""
    cands = []
    base_exe = getattr(sys, "_base_executable", None)
    if base_exe:
        cands.append(base_exe)
    if os.name == "nt":
        cands.append(os.path.join(sys.base_exec_prefix, "python.exe"))
        cands.append(os.path.join(sys.exec_prefix, "python.exe"))
    else:
        cands.append(os.path.join(sys.base_exec_prefix, "bin", "python3"))
        cands.append(os.path.join(sys.exec_prefix, "bin", "python3"))
    for name in ("python3", "python"):
        w = shutil.which(name)
        if w:
            cands.append(w)
    for c in cands:
        if c and os.path.basename(c).lower().startswith("python") and os.path.exists(c):
            return c
    return None


def _strip_qgis_provided(target):
    """Remove QGIS-provided packages from a target dir (avoid ABI shadowing)."""
    try:
        for entry in os.listdir(target):
            low = entry.lower()
            if any(low == p or low.startswith(p + "-") or low.startswith(p + ".")
                   for p in _QGIS_PROVIDED):
                path = os.path.join(target, entry)
                shutil.rmtree(path, ignore_errors=True) if os.path.isdir(path) else os.remove(path)
    except Exception:
        pass


def _patch_climdex():
    """climdex uses the deprecated '1M' offset; pandas 3.x rejects it and 9 of
    17 indices fail silently. Replace with 'ME'. Idempotent. Applied after a
    pip fallback, which pulls the UNPATCHED climdex (the prebuilt zips are
    already patched by build_extlibs_zip.py)."""
    base = os.path.join(EXTLIBS_PATH, "climdex")
    for name in ("precipitation.py", "temperature.py"):
        f = os.path.join(base, name)
        if not os.path.isfile(f):
            continue
        try:
            with open(f, "r", encoding="utf-8") as fh:
                c = fh.read()
            if "'1M'" in c:
                with open(f, "w", encoding="utf-8") as fh:
                    fh.write(c.replace("'1M'", "'ME'"))
        except Exception:
            pass


# -- provisioning steps (shared by blocking + async paths) --------------------
def _try_tagged_zip() -> bool:
    url = BASE_URL + f"extlibs-{current_tag()}.zip"
    if not url.startswith("https://"):
        return False
    zip_path = os.path.join(_PLUGIN_DIR, "_extlibs_dl.zip")
    try:
        with urllib.request.urlopen(url) as resp, open(zip_path, "wb") as f:  # nosec B310
            f.write(resp.read())
        with zipfile.ZipFile(zip_path, "r") as zf:
            names = zf.namelist()
            if names and names[0].startswith("extlibs/"):
                zf.extractall(_PLUGIN_DIR)
            else:
                os.makedirs(EXTLIBS_PATH, exist_ok=True)
                zf.extractall(EXTLIBS_PATH)
        return True
    except Exception:
        return False
    finally:
        if os.path.exists(zip_path):
            try:
                os.remove(zip_path)
            except OSError:
                pass


def _try_pip() -> bool:
    py = _python_executable()
    if not py or not os.path.exists(_REQUIREMENTS):
        return False
    os.makedirs(EXTLIBS_PATH, exist_ok=True)
    try:
        subprocess.run(
            [py, "-m", "pip", "install", "--target", EXTLIBS_PATH,
             "-r", _REQUIREMENTS, "--no-warn-script-location"],
            check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except Exception:
        return False
    _strip_qgis_provided(EXTLIBS_PATH)
    _patch_climdex()
    return True


def _finish_ok():
    os.makedirs(EXTLIBS_PATH, exist_ok=True)
    with open(_SENTINEL, "w", encoding="utf-8") as f:
        f.write(current_tag())
    ensure_on_path()


def _provision() -> bool:
    """Run the provisioning strategy. Returns True on success. Blocking."""
    if _try_tagged_zip():
        _finish_ok()
        return True
    if _try_pip():
        _finish_ok()
        return True
    return False


def ensure_ready(parent=None):
    """Make sure extlibs are present, downloading them if needed.

    Blocks until the libraries are available so the caller can import them
    immediately. Returns True on success, False on failure (a message box is
    shown to the user on failure). Safe to call every load; it is a no-op once
    provisioned for this interpreter.
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
        if _provision():
            return True
        QMessageBox.critical(
            parent, "ClimaPlots",
            "Não foi possível baixar as dependências externas automaticamente "
            f"para {current_tag()}.\n\nInstale os pacotes de requirements.txt no "
            "ambiente Python do QGIS manualmente e recarregue o plugin.",
        )
        return False
    except Exception as e:  # noqa: BLE001 - surface any failure to the user
        QMessageBox.critical(
            parent, "ClimaPlots",
            f"Falha ao baixar as dependências externas.\n\nErro: {e}",
        )
        return False
    finally:
        dlg.close()


# --- Async parity (kept for callers that prefer it) --------------------------
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
    download_done = pyqtSignal(bool, str)  # success, message

    def run(self):
        try:
            if _provision():
                self.download_done.emit(True, "")
                return
            self.download_done.emit(
                False,
                "Could not provision dependencies automatically for "
                f"{current_tag()}. Install the packages from requirements.txt "
                "in the QGIS Python environment manually.")
        except Exception as e:
            self.download_done.emit(False, str(e))
