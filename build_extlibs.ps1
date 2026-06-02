# Builds extlibs.zip for ClimaPlots from the local extlibs/ folder.
#
# extlibs/ holds ONLY the libraries not provided by QGIS site-packages:
#   bottleneck, climdex, pyhomogeneity, pymannkendall, xarray
# numpy / pandas / scipy / requests come from QGIS itself and must NOT be bundled.
#
# The resulting extlibs.zip is uploaded to the repo root on `main`; the plugin
# downloads it on first run (see extlibs_manager.py).
#
# To rebuild extlibs/ from scratch (run with the QGIS Python so compiled libs
# match QGIS's numpy ABI):
#   & "C:\QGIS 3.44.10\bin\python-qgis-ltr.bat" -m pip install -r requirements.txt --target extlibs
#
# Usage:  powershell -ExecutionPolicy Bypass -File build_extlibs.ps1

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$ext  = Join-Path $root "extlibs"
$zip  = Join-Path $root "extlibs.zip"

if (-not (Test-Path $ext)) {
    throw "extlibs/ not found at $ext. Install dependencies first (see header)."
}

# Drop the old archive
if (Test-Path $zip) { Remove-Item $zip -Force }

# Strip __pycache__ so the archive stays small and clean
Get-ChildItem -Path $ext -Recurse -Directory -Filter "__pycache__" |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# Zip the contents of extlibs/ (bare, no extlibs/ prefix — extlibs_manager.py
# handles both, but bare keeps it simple)
$items = Get-ChildItem -Path $ext -Force
Compress-Archive -Path $items.FullName -DestinationPath $zip -CompressionLevel Optimal

$sizeMB = "{0:N1}" -f ((Get-Item $zip).Length / 1MB)
Write-Host "Built $zip ($sizeMB MB)"
Write-Host "Top-level packages:"
$items | Where-Object { $_.PSIsContainer } | ForEach-Object { Write-Host "  $($_.Name)" }
Write-Host ""
Write-Host "Next: commit/upload extlibs.zip to the repo root on 'main'."
