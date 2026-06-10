#!/usr/bin/env python3
"""Build a distributable ClimaPlots plugin zip.

The plugin ships its heavy scientific dependencies as a runtime download
(tagged ``extlibs-<cpXY>-<platform>.zip`` bundles fetched on first load by
``extlibs_manager.py``), so the distribution zip deliberately EXCLUDES the
unpacked ``extlibs/`` folder and the ``extlibs-*.zip`` artifacts, keeping it
small.

The file list is taken from git (tracked files) so anything gitignored
(``extlibs/``, ``__pycache__/``, ``CLAUDE.md``, dev rasters, ...) is excluded
automatically. A small extra skip-list drops dev-only tooling.

Usage (from the plugin directory):
    python build_plugin.py          # plain Python is fine, no QGIS needed
Output:
    dist/climaplots.zip   (unpacks to a top-level ``climaplots/`` folder)
"""
from __future__ import annotations

import os
import subprocess
import sys
import zipfile
from pathlib import Path

PLUGIN_NAME = "climaplots"
ROOT = Path(__file__).parent.resolve()
DIST_DIR = ROOT / "dist"
ZIP_PATH = DIST_DIR / f"{PLUGIN_NAME}.zip"

# Tracked files excluded from the distribution zip (posix paths).
SKIP_FILES = {
    "build_plugin.py",    # dev tooling
    "build_extlibs_zip.py",  # dev tooling (tagged per-interpreter build)
    ".gitignore",
    ".gitattributes",
    # Docs / dev artifacts, not needed at runtime
    "README.md",
    "index.html",
    "dev.ipynb",
    "resources.qrc",
    # Large demo / source assets the plugin never loads at runtime
    "medias/climateplots.gif",   # ~12 MB demo GIF
    "medias/translation.xlsx",
    "medias/preview.png",
    "assets/farm_icon.png",      # superseded by farm_analytica_logo.svg
}
# Any tracked file whose path contains one of these parts is skipped.
SKIP_DIR_PARTS = {
    "__pycache__", "dev", ".github", ".claude", ".codex", ".vscode",
    "dist", "help", "scripts",
}


def tracked_files() -> list[str]:
    """Return repo-tracked files (posix paths), or fall back to a dir walk."""
    try:
        out = subprocess.run(
            ["git", "ls-files"], cwd=ROOT, check=True,
            capture_output=True, text=True,
        ).stdout
        return [line.strip() for line in out.splitlines() if line.strip()]
    except Exception:
        files = []
        for p in ROOT.rglob("*"):
            if p.is_file():
                files.append(p.relative_to(ROOT).as_posix())
        return files


def _skip(rel: str) -> bool:
    if rel in SKIP_FILES:
        return True
    # Tagged extlibs bundles (extlibs-cp312-win_amd64.zip, ...) are fetched at
    # runtime by extlibs_manager, never bundled into the plugin distribution.
    name = Path(rel).name
    if name.startswith("extlibs-") and name.endswith(".zip"):
        return True
    return any(part in SKIP_DIR_PARTS for part in Path(rel).parts)


def build_zip() -> None:
    DIST_DIR.mkdir(exist_ok=True)
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()

    included = 0
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for rel in sorted(tracked_files()):
            if _skip(rel):
                continue
            src = ROOT / rel
            if not src.is_file():
                continue
            # Unpacks to a top-level climaplots/ folder (QGIS plugin convention).
            zf.write(src, f"{PLUGIN_NAME}/{rel}")
            included += 1

    size_mb = ZIP_PATH.stat().st_size / 1_048_576
    print(f"Built dist/{PLUGIN_NAME}.zip  ({included} files, {size_mb:.2f} MB)")
    print("extlibs are downloaded on first run; rebuild the tagged bundles with "
          "build_extlibs_zip.py (or the 'Build extlibs' GitHub Actions workflow).")


if __name__ == "__main__":
    if not (ROOT / "metadata.txt").exists():
        sys.exit("metadata.txt not found - run this from the plugin directory.")
    build_zip()
