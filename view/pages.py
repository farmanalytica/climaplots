# -*- coding: utf-8 -*-
"""Page builders for the ClimaPlots dialog.

Each ``setup_*_page(dialog, page)`` populates a QWidget and attaches the
interactive widgets onto ``dialog`` under the names the handlers expect
(``LongEdit``, ``atributo``, ``webView_1`` ...), so the controller logic in
climaplots_dialog.py stays UI-agnostic. Mirrors the ``setup_*_page`` convention
of the sibling plugins (terra_valora, qgis-EasyDEM).
"""
import os

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon, QPixmap
from qgis.PyQt.QtWebKitWidgets import QWebView
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from .styles import STYLE_BTN, STYLE_BTN_PRIMARY

_PLUGIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MEDIAS = os.path.join(_PLUGIN_DIR, "medias")
_ASSETS = os.path.join(_PLUGIN_DIR, "assets")

_VARIABLES = [
    "Max Temperature", "Min Temperature", "Precipitation",
    "Relative Humidity", "Irradiation",
]
_INDICES = [
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

_INTRO_TEXT = (
    "ClimaPlots fetches 40+ years of daily climate data from NASA POWER for any "
    "point on the map and builds interactive visualizations: annual trends with "
    "Mann-Kendall / Pettitt tests, a thermo-pluviometric diagram, and ETCCDI "
    "climate indices. Click a point on the canvas, run the analysis, and explore "
    "the charts."
)


def _icon(name):
    path = os.path.join(_MEDIAS, name)
    return QIcon(path) if os.path.exists(path) else QIcon()


def _make_webview():
    view = QWebView()
    view.setFocusPolicy(Qt.NoFocus)
    view.setContextMenuPolicy(Qt.NoContextMenu)
    view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    return view


def _load_logo(width=210):
    """Load the FARM Analytica logo (svg, png fallback) scaled to ``width``."""
    for name in ("farm_analytica_logo.svg", "farm_icon.png"):
        pix = QPixmap(os.path.join(_ASSETS, name))
        if not pix.isNull():
            return pix.scaledToWidth(width, Qt.TransformationMode.SmoothTransformation)
    return None


# --------------------------------------------------------------------- intro
def setup_intro_page(dialog, page):
    page.setObjectName("pageIntro")
    page.setStyleSheet("QWidget#pageIntro { background-color: #f5f7fa; }")

    outer = QVBoxLayout(page)
    outer.setContentsMargins(48, 28, 48, 20)
    outer.addStretch(1)

    title = QLabel("ClimaPlots")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setStyleSheet("color: #1c3d5a; font-size: 26px; font-weight: bold; background: transparent;")
    outer.addWidget(title)

    subtitle = QLabel("Climate analysis from NASA POWER")
    subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
    subtitle.setStyleSheet("color: #2c6cab; font-size: 13px; background: transparent;")
    outer.addWidget(subtitle)

    outer.addSpacing(18)

    desc = QLabel(_INTRO_TEXT)
    desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
    desc.setWordWrap(True)
    desc.setStyleSheet("color: #5b6b7b; font-size: 13px; background: transparent;")
    desc.setMaximumWidth(560)
    desc_row = QHBoxLayout()
    desc_row.addStretch(1)
    desc_row.addWidget(desc)
    desc_row.addStretch(1)
    outer.addLayout(desc_row)

    outer.addSpacing(26)

    btn_row = QHBoxLayout()
    btn_row.addStretch(1)
    start_btn = QPushButton("Get Started")
    start_btn.setStyleSheet(STYLE_BTN_PRIMARY)
    start_btn.setFixedHeight(40)
    start_btn.setMinimumWidth(180)
    start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
    start_btn.clicked.connect(dialog._on_get_started)
    btn_row.addWidget(start_btn)
    btn_row.addStretch(1)
    outer.addLayout(btn_row)

    outer.addStretch(2)
    outer.addWidget(_build_sponsor())
    dialog.intro_start_btn = start_btn


def _build_sponsor():
    """Sponsor footer: 'Sponsored by' + FARM Analytica logo."""
    wrap = QWidget()
    wrap.setStyleSheet("background: transparent;")
    lay = QVBoxLayout(wrap)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(6)

    label = QLabel("Sponsored by")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet("color: #90a0b0; font-size: 11px; background: transparent;")
    lay.addWidget(label)

    logo = QLabel()
    logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
    logo.setStyleSheet("background: transparent;")
    pix = _load_logo(200)
    if pix is not None:
        logo.setPixmap(pix)
    else:
        logo.setText("FARM Analytica")
        logo.setStyleSheet("color: #1c3d5a; font-size: 14px; font-weight: bold; background: transparent;")
    logo.setCursor(Qt.CursorShape.PointingHandCursor)
    lay.addWidget(logo)
    return wrap


# ----------------------------------------------------------------- coordinates
def setup_coordinates_page(dialog, page):
    layout = QVBoxLayout(page)
    layout.setContentsMargins(16, 14, 16, 14)

    group = QGroupBox("Select coordinate (click on canvas or type it)")
    grid = QGridLayout(group)
    dialog.LongEdit = QLineEdit()
    dialog.LatEdit = QLineEdit()
    grid.addWidget(QLabel("Longitude:"), 0, 0)
    grid.addWidget(QLabel("Latitude:"), 0, 1)
    grid.addWidget(dialog.LongEdit, 1, 0)
    grid.addWidget(dialog.LatEdit, 1, 1)
    dialog.pick_point = QPushButton("📍  Pick point on map")
    dialog.pick_point.setCheckable(True)
    dialog.pick_point.setStyleSheet(STYLE_BTN)
    dialog.pick_point.setCursor(Qt.CursorShape.PointingHandCursor)
    grid.addWidget(dialog.pick_point, 2, 0, 1, 2)
    layout.addWidget(group)

    dialog.learn = QPushButton(_icon("open-in-browser.svg"), "Learn more about this plugin")
    dialog.learn.setStyleSheet(STYLE_BTN)
    layout.addWidget(dialog.learn)

    row = QHBoxLayout()
    dialog.googlemaps = QPushButton("Load Google Maps Layer")
    dialog.googlemaps.setStyleSheet(STYLE_BTN)
    dialog.gerar_req = QPushButton(_icon("icons8-reproduzir-50.png"), "Run Analysis")
    dialog.gerar_req.setStyleSheet(STYLE_BTN_PRIMARY)
    row.addWidget(dialog.googlemaps)
    row.addWidget(dialog.gerar_req)
    layout.addLayout(row)

    dialog.proxy = QPushButton(
        _icon("network-settings-2-32.png"),
        "Proxy setting (only if required by your network provider)",
    )
    dialog.proxy.setStyleSheet(STYLE_BTN)
    layout.addWidget(dialog.proxy)
    layout.addStretch(1)


# -------------------------------------------------------------------- plots
def _plot_page(dialog, page):
    """Common skeleton: a top button row + an expanding web view below."""
    layout = QVBoxLayout(page)
    layout.setContentsMargins(8, 8, 8, 8)
    row = QHBoxLayout()
    layout.addLayout(row)
    web = _make_webview()
    layout.addWidget(web, 1)
    return row, web


def setup_trends_page(dialog, page):
    row, web = _plot_page(dialog, page)
    dialog.atributo = QComboBox()
    dialog.atributo.addItems(_VARIABLES)
    dialog.save_raw = QPushButton(_icon("diskette.png"), "Save raw data")
    dialog.navegador = QPushButton(_icon("open-in-browser.svg"), "Open in the browser")
    dialog.save_plot = QPushButton(_icon("diskette.png"), "Save data")
    for b in (dialog.save_raw, dialog.navegador, dialog.save_plot):
        b.setStyleSheet(STYLE_BTN)
    row.addWidget(dialog.atributo)
    row.addStretch(1)
    row.addWidget(dialog.save_raw)
    row.addWidget(dialog.navegador)
    row.addWidget(dialog.save_plot)
    dialog.webView_1 = web


def setup_thermo_page(dialog, page):
    row, web = _plot_page(dialog, page)
    dialog.navegador_2 = QPushButton(_icon("open-in-browser.svg"), "Open in the browser")
    dialog.save_plot2 = QPushButton(_icon("diskette.png"), "Save data")
    for b in (dialog.navegador_2, dialog.save_plot2):
        b.setStyleSheet(STYLE_BTN)
    row.addStretch(1)
    row.addWidget(dialog.navegador_2)
    row.addWidget(dialog.save_plot2)
    dialog.webView_2 = web


def setup_indices_page(dialog, page):
    row, web = _plot_page(dialog, page)
    dialog.atributo_2 = QComboBox()
    dialog.atributo_2.addItems(_INDICES)
    dialog.atributo_2.setCurrentIndex(0)
    dialog.navegador_3 = QPushButton(_icon("open-in-browser.svg"), "Open in the browser")
    dialog.save_plot3 = QPushButton(_icon("diskette.png"), "Save data")
    for b in (dialog.navegador_3, dialog.save_plot3):
        b.setStyleSheet(STYLE_BTN)
    row.addWidget(dialog.atributo_2, 1)
    row.addWidget(dialog.navegador_3)
    row.addWidget(dialog.save_plot3)
    dialog.webView_3 = web
