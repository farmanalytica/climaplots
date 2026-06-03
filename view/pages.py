# -*- coding: utf-8 -*-
"""Page builders for the ClimaPlots dialog.

Each ``setup_*_page(dialog, page)`` populates a QWidget and attaches the
interactive widgets onto ``dialog`` under the names the handlers expect
(``LongEdit``, ``atributo``, ``webView_1`` ...), so the controller logic in
climaplots_dialog.py stays UI-agnostic. Mirrors the ``setup_*_page`` convention
of the sibling plugins (terra_valora, qgis-EasyDEM).
"""
import os

from qgis.PyQt.QtCore import Qt, QUrl, QSize
from qgis.PyQt.QtGui import QDesktopServices, QIcon, QPixmap
from qgis.PyQt.QtWebKitWidgets import QWebPage, QWebView
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

from .styles import STYLE_BTN, STYLE_BTN_PRIMARY, STYLE_PICK_TOGGLE

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

# Labels for the checkable "pick point" toggle (idle / capturing).
PICK_TEXT_OFF = "📍  Pick a point on the map"
PICK_TEXT_ON = "📍  Click the map…  (click here to cancel)"

_ICON_SIZE = QSize(16, 16)
_BTN_HEIGHT = 30


def _icon(name):
    path = os.path.join(_MEDIAS, name)
    return QIcon(path) if os.path.exists(path) else QIcon()


def _button(text, icon=None, tooltip="", style=STYLE_BTN, height=_BTN_HEIGHT):
    """Create a styled button with a consistent icon size, height and cursor."""
    btn = QPushButton(_icon(icon), text) if icon else QPushButton(text)
    btn.setStyleSheet(style)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    if icon:
        btn.setIconSize(_ICON_SIZE)
    if tooltip:
        btn.setToolTip(tooltip)
    if height:
        btn.setMinimumHeight(height)
    return btn


def _combo(items, tooltip="", min_width=220):
    """Create a dropdown with a consistent size and cursor."""
    cb = QComboBox()
    cb.addItems(items)
    if tooltip:
        cb.setToolTip(tooltip)
    cb.setMinimumWidth(min_width)
    cb.setMinimumHeight(28)
    cb.setCursor(Qt.CursorShape.PointingHandCursor)
    return cb


def _make_webview():
    view = QWebView()
    view.setFocusPolicy(Qt.NoFocus)
    view.setContextMenuPolicy(Qt.NoContextMenu)
    view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    return view


# --------------------------------------------------------------------- intro
def setup_intro_page(dialog, page):
    page.setObjectName("pageIntro")
    page.setStyleSheet("QWidget#pageIntro { background-color: #f5f7fa; }")

    outer = QVBoxLayout(page)
    outer.setContentsMargins(0, 0, 0, 0)
    outer.setSpacing(0)

    # Explainer / usage guide / citation rendered from assets/intro.html.
    view = _make_webview()
    view.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
    view.linkClicked.connect(QDesktopServices.openUrl)  # open DOI etc. externally
    view.load(QUrl.fromLocalFile(os.path.join(_ASSETS, "intro.html")))
    outer.addWidget(view, 1)

    btn_row = QHBoxLayout()
    btn_row.setContentsMargins(0, 10, 0, 8)
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

    outer.addWidget(_build_sponsor())

    dialog.intro_start_btn = start_btn


def _build_sponsor():
    """Sponsor footer (same as AGLgis): FARM logo + attribution with a link."""
    footer = QWidget()
    footer.setMinimumHeight(36)
    footer.setStyleSheet(
        "background-color: transparent;"
        "QLabel { border: none; background: transparent; }"
    )
    lay = QHBoxLayout(footer)
    lay.setContentsMargins(28, 4, 28, 4)
    lay.setSpacing(8)

    # FARM Analytica logo — falls back to plain text if the SVG is missing.
    farm_icon = QLabel()
    farm_icon.setFixedHeight(16)
    farm_icon.setStyleSheet("background: transparent;")
    pix = QPixmap(os.path.join(_ASSETS, "farm_analytica_logo.svg")).scaledToHeight(
        16, Qt.TransformationMode.SmoothTransformation
    )
    if not pix.isNull():
        farm_icon.setPixmap(pix)
        farm_icon.setFixedWidth(pix.width())
    else:
        farm_icon.setText("FARM ANALYTICA")
        farm_icon.setStyleSheet("color: #1c3d5a; font-size: 9px; font-weight: bold;")
    farm_icon.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
    lay.addWidget(farm_icon)

    # Attribution copy with an external link to the FARM Analytica website.
    farm_text = QLabel()
    farm_text.setTextFormat(Qt.TextFormat.RichText)
    farm_text.setOpenExternalLinks(True)
    farm_text.setWordWrap(True)
    farm_text.setText(
        "This is a free and open project, supported by "
        '<a href="https://farmanalytica.com.br" style="color:#2c6cab;'
        'text-decoration:none;font-weight:bold;">FARM Analytica</a>. '
        "Get in touch for exclusive and personalized commercial solutions."
    )
    farm_text.setStyleSheet("color: #9e9e9e; font-size: 9px;")
    farm_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    lay.addWidget(farm_text)
    return footer


# ----------------------------------------------------------------- coordinates
def setup_coordinates_page(dialog, page):
    layout = QVBoxLayout(page)
    layout.setContentsMargins(14, 10, 14, 10)
    layout.setSpacing(6)

    group = QGroupBox("Location")
    grid = QGridLayout(group)
    grid.setVerticalSpacing(3)
    grid.setContentsMargins(10, 6, 10, 8)
    dialog.LongEdit = QLineEdit()
    dialog.LongEdit.setPlaceholderText("e.g. -47.06")
    dialog.LongEdit.setToolTip("Longitude in decimal degrees (WGS84)")
    dialog.LatEdit = QLineEdit()
    dialog.LatEdit.setPlaceholderText("e.g. -22.90")
    dialog.LatEdit.setToolTip("Latitude in decimal degrees (WGS84)")
    grid.addWidget(QLabel("Longitude"), 0, 0)
    grid.addWidget(QLabel("Latitude"), 0, 1)
    grid.addWidget(dialog.LongEdit, 1, 0)
    grid.addWidget(dialog.LatEdit, 1, 1)
    dialog.pick_point = QPushButton(PICK_TEXT_OFF)
    dialog.pick_point.setCheckable(True)
    dialog.pick_point.setStyleSheet(STYLE_PICK_TOGGLE)
    dialog.pick_point.setCursor(Qt.CursorShape.PointingHandCursor)
    dialog.pick_point.setMinimumHeight(32)
    dialog.pick_point.setToolTip("Capture a coordinate by clicking on the map canvas")
    grid.addWidget(dialog.pick_point, 2, 0, 1, 2)
    layout.addWidget(group)

    # Satellite-layer + Run on a single row to keep the page short.
    row = QHBoxLayout()
    row.setSpacing(6)
    dialog.googlemaps = _button(
        "Satellite layer", "download.svg",
        "Add a Google satellite basemap to help locate your point", height=34)
    dialog.gerar_req = _button(
        "Run analysis", "icons8-reproduzir-50.png",
        "Download NASA POWER data for this point and build the charts",
        style=STYLE_BTN_PRIMARY, height=34)
    row.addWidget(dialog.googlemaps)
    row.addWidget(dialog.gerar_req, 1)
    layout.addLayout(row)
    layout.addStretch(1)


# -------------------------------------------------------------------- plots
def _plot_page(dialog, page):
    """Common skeleton: a top toolbar row + an expanding web view below."""
    layout = QVBoxLayout(page)
    layout.setContentsMargins(8, 6, 8, 6)
    layout.setSpacing(6)
    row = QHBoxLayout()
    row.setSpacing(6)
    layout.addLayout(row)
    web = _make_webview()
    layout.addWidget(web, 1)
    return row, web


def _toolbar_label(text):
    lbl = QLabel(text)
    lbl.setStyleSheet("color: #5b6b7b; font-size: 12px; font-weight: bold; background: transparent;")
    return lbl


def setup_trends_page(dialog, page):
    row, web = _plot_page(dialog, page)
    dialog.atributo = _combo(_VARIABLES, "Choose the climate variable to plot")
    dialog.save_raw = _button("Save daily data", "diskette.png",
                              "Export the full daily NASA POWER series as CSV")
    dialog.navegador = _button("Open in browser", "open-in-browser.svg",
                               "Open this chart full-screen in your web browser")
    dialog.save_plot = _button("Save chart data", "diskette.png",
                               "Export the plotted annual series as CSV")
    row.addWidget(_toolbar_label("Variable:"))
    row.addWidget(dialog.atributo)
    row.addStretch(1)
    row.addWidget(dialog.save_raw)
    row.addWidget(dialog.navegador)
    row.addWidget(dialog.save_plot)
    dialog.webView_1 = web


def setup_thermo_page(dialog, page):
    row, web = _plot_page(dialog, page)
    dialog.navegador_2 = _button("Open in browser", "open-in-browser.svg",
                                 "Open this chart full-screen in your web browser")
    dialog.save_plot2 = _button("Save chart data", "diskette.png",
                                "Export the monthly climate normals as CSV")
    row.addWidget(_toolbar_label("Mean monthly precipitation and temperature"))
    row.addStretch(1)
    row.addWidget(dialog.navegador_2)
    row.addWidget(dialog.save_plot2)
    dialog.webView_2 = web


def setup_indices_page(dialog, page):
    row, web = _plot_page(dialog, page)
    dialog.atributo_2 = _combo(_INDICES, "Choose the ETCCDI climate index to plot", min_width=300)
    dialog.atributo_2.setCurrentIndex(0)
    dialog.navegador_3 = _button("Open in browser", "open-in-browser.svg",
                                 "Open this chart full-screen in your web browser")
    dialog.save_plot3 = _button("Save chart data", "diskette.png",
                                "Export the selected index series as CSV")
    row.addWidget(_toolbar_label("Index:"))
    row.addWidget(dialog.atributo_2, 1)
    row.addWidget(dialog.navegador_3)
    row.addWidget(dialog.save_plot3)
    dialog.webView_3 = web
