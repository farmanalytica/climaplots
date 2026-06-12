# -*- coding: utf-8 -*-
"""Page builders for the ClimaPlots dialog.

Each ``setup_*_page(dialog, page)`` populates a QWidget and attaches the
interactive widgets onto ``dialog`` under the names the handlers expect
(``LongEdit``, ``atributo``, ``webView_1`` ...), so the controller logic in
climaplots_dialog.py stays UI-agnostic. Mirrors the ``setup_*_page`` convention
of the sibling plugins (terra_valora, qgis-EasyDEM).
"""
import datetime
import os

from qgis.PyQt.QtCore import QCoreApplication, Qt, QUrl, QSize
from qgis.PyQt.QtGui import QDesktopServices, QIcon, QPixmap
from qgis.PyQt.QtWebKitWidgets import QWebPage, QWebView
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

_MIN_YEAR = 1981
_MAX_YEAR = datetime.date.today().year - 1

from .styles import STYLE_BTN, STYLE_BTN_PRIMARY, STYLE_PICK_TOGGLE


def _tr(text):
    return QCoreApplication.translate("ClimaPlots", text)

_PLUGIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MEDIAS = os.path.join(_PLUGIN_DIR, "medias")
_ASSETS = os.path.join(_PLUGIN_DIR, "assets")

_VARIABLES = [
    "Max Temperature", "Min Temperature", "Precipitation",
    "Relative Humidity", "Irradiation", "Wind Speed",
    "Reference ET0", "Growing Degree Days",
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

# Short, one-line explanations shown under the dropdown when an item is picked.
VARIABLE_DESC = {
    "Max Temperature": "Daily maximum air temperature at 2 m (°C).",
    "Min Temperature": "Daily minimum air temperature at 2 m (°C).",
    "Precipitation": "Daily total precipitation (mm).",
    "Relative Humidity": "Mean relative humidity at 2 m (%).",
    "Irradiation": "All-sky surface shortwave irradiation (kWh/m²/day).",
    "Wind Speed": "Mean wind speed at 2 m (m/s).",
    "Reference ET0": "Reference evapotranspiration, Hargreaves method (mm).",
    "Growing Degree Days": "Heat accumulation above a 10 °C base (°C·day).",
}
INDEX_DESC = {
    "Annual Summer Days": "Annual count of days with Tmax > 25 °C.",
    "Annual Frost Days": "Annual count of days with Tmin < 0 °C.",
    "Annual Tropical Nights": "Annual count of nights with Tmin > 20 °C.",
    "Annual Icing Days": "Annual count of days with Tmax < 0 °C.",
    "Monthly Maximum Temperature": "Monthly highest daily maximum temperature (TXx).",
    "Monthly Minimum Temperature of Maximum Temperatures": "Monthly lowest daily maximum temperature (TXn).",
    "Monthly Maximum Temperature of Minimum Temperatures": "Monthly highest daily minimum temperature (TNx).",
    "Monthly Minimum Temperature": "Monthly lowest daily minimum temperature (TNn).",
    "Daily Temperature Range": "Mean difference between daily max and min (DTR).",
    "Monthly Maximum 1-day Precipitation": "Highest 1-day precipitation each month (Rx1day).",
    "Monthly Maximum 5-day Precipitation": "Highest 5-day precipitation total each month (Rx5day).",
    "Annual Count of Days when Precipitation Exceeds 10mm": "Annual count of days with ≥ 10 mm (R10mm).",
    "Annual Count of Days when Precipitation Exceeds 20mm": "Annual count of days with ≥ 20 mm (R20mm).",
    "Simple Precipitation Intensity Index": "Mean precipitation on wet days (SDII).",
    "Number of Consecutive Dry Days in a Month": "Longest dry spell each month (CDD).",
    "Number of Consecutive Wet Days in a Month": "Longest wet spell each month (CWD).",
    "The Standardized Precipitation Index (SPI)": "90-day standardized precipitation anomaly (SPI).",
}


def variable_description(name):
    return VARIABLE_DESC.get(name, "")


def index_description(name):
    return INDEX_DESC.get(name, "")

# Labels for the checkable "pick point" toggles (idle / capturing).
PICK_TEXT_OFF = "📍  Pick a point on the map"
PICK_TEXT_ON = "📍  Click the map…  (click here to cancel)"
PICK_B_OFF = "📍  Pick comparison point B"
PICK_B_ON = "📍  Click the map for B…  (click here to cancel)"

_ICON_SIZE = QSize(16, 16)
_BTN_HEIGHT = 30


_ICONS = os.path.join(_ASSETS, "icons")


def _icon(name):
    """Resolve an icon name against assets/icons (vector set) then medias."""
    for base in (_ICONS, _MEDIAS):
        path = os.path.join(base, name)
        if os.path.exists(path):
            return QIcon(path)
    return QIcon()



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
    btn.setMinimumWidth(0)
    btn.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
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
    cb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    return cb


def _make_webview():
    view = QWebView()
    view.setFocusPolicy(Qt.NoFocus)
    view.setContextMenuPolicy(Qt.NoContextMenu)
    view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    view.setMinimumHeight(200)
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
    start_btn = QPushButton(_tr("Get Started"))
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
        _tr("This is a free and open project, supported by ")
        + '<a href="https://farmanalytica.com.br" style="color:#2c6cab;'
        'text-decoration:none;font-weight:bold;">FARM Analytica</a>. '
        + _tr("Get in touch for exclusive and personalized commercial solutions.")
    )
    farm_text.setStyleSheet("color: #9e9e9e; font-size: 9px;")
    farm_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    lay.addWidget(farm_text)
    return footer


# ----------------------------------------------------------------- coordinates
def setup_coordinates_page(dialog, page):
    # Outer layout: scroll area fills available height, run button pinned at bottom.
    outer = QVBoxLayout(page)
    outer.setContentsMargins(0, 0, 0, 10)
    outer.setSpacing(0)

    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.Shape.NoFrame)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll.setStyleSheet("QScrollArea { background-color: #f5f7fa; border: none; }")

    inner = QWidget()
    inner.setStyleSheet("background-color: #f5f7fa;")
    layout = QVBoxLayout(inner)
    layout.setContentsMargins(14, 10, 14, 8)
    layout.setSpacing(8)

    # Data source selector (English values are the source keys).
    src_row = QHBoxLayout()
    src_row.setSpacing(8)
    dialog.source_combo = QComboBox()
    dialog.source_combo.addItem("NASA POWER", "power")
    dialog.source_combo.addItem("Open-Meteo (ERA5)", "openmeteo")
    dialog.source_combo.setToolTip(_tr("Climate data provider"))
    dialog.source_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    src_row.addWidget(QLabel(_tr("Data source")))
    src_row.addWidget(dialog.source_combo, 1)
    layout.addLayout(src_row)

    group = QGroupBox(_tr("Location"))
    grid = QGridLayout(group)
    grid.setVerticalSpacing(4)
    grid.setHorizontalSpacing(8)
    grid.setContentsMargins(10, 6, 10, 10)
    dialog.LongEdit = QLineEdit()
    dialog.LongEdit.setPlaceholderText("e.g. -47.06")
    dialog.LongEdit.setToolTip(_tr("Longitude in decimal degrees (WGS84)"))
    dialog.LatEdit = QLineEdit()
    dialog.LatEdit.setPlaceholderText("e.g. -22.90")
    dialog.LatEdit.setToolTip(_tr("Latitude in decimal degrees (WGS84)"))
    grid.addWidget(QLabel(_tr("Longitude")), 0, 0)
    grid.addWidget(QLabel(_tr("Latitude")), 0, 1)
    grid.addWidget(dialog.LongEdit, 1, 0)
    grid.addWidget(dialog.LatEdit, 1, 1)
    dialog.pick_point = QPushButton(_tr(PICK_TEXT_OFF))
    dialog.pick_point.setCheckable(True)
    dialog.pick_point.setStyleSheet(STYLE_PICK_TOGGLE)
    dialog.pick_point.setCursor(Qt.CursorShape.PointingHandCursor)
    dialog.pick_point.setMinimumHeight(34)
    dialog.pick_point.setMinimumWidth(0)
    dialog.pick_point.setToolTip(_tr("Capture a coordinate by clicking on the map canvas"))
    grid.addWidget(dialog.pick_point, 2, 0, 1, 2)

    # Year range (NASA POWER daily data starts in 1981).
    dialog.start_year = QSpinBox()
    dialog.start_year.setRange(_MIN_YEAR, _MAX_YEAR)
    dialog.start_year.setValue(_MIN_YEAR)
    dialog.start_year.setToolTip(_tr("First year to download"))
    dialog.end_year = QSpinBox()
    dialog.end_year.setRange(_MIN_YEAR, _MAX_YEAR)
    dialog.end_year.setValue(_MAX_YEAR)
    dialog.end_year.setToolTip(_tr("Last year to download"))
    years = QHBoxLayout()
    years.setSpacing(6)
    years.addStretch(1)
    years.addWidget(QLabel(_tr("Years")))
    years.addWidget(dialog.start_year)
    years.addWidget(QLabel(_tr("to")))
    years.addWidget(dialog.end_year)
    years.addStretch(1)
    grid.addLayout(years, 3, 0, 1, 2)
    layout.addWidget(group)

    # Optional comparison point B (overlaid on the Trends chart).
    group_b = QGroupBox(_tr("Comparison point B (optional)"))
    grid_b = QGridLayout(group_b)
    grid_b.setVerticalSpacing(4)
    grid_b.setHorizontalSpacing(8)
    grid_b.setContentsMargins(10, 6, 10, 10)
    dialog.LongEditB = QLineEdit()
    dialog.LongEditB.setPlaceholderText("e.g. -44.00")
    dialog.LatEditB = QLineEdit()
    dialog.LatEditB.setPlaceholderText("e.g. -20.00")
    grid_b.addWidget(QLabel(_tr("Longitude")), 0, 0)
    grid_b.addWidget(QLabel(_tr("Latitude")), 0, 1)
    grid_b.addWidget(dialog.LongEditB, 1, 0)
    grid_b.addWidget(dialog.LatEditB, 1, 1)
    dialog.pick_point_b = QPushButton(_tr(PICK_B_OFF))
    dialog.pick_point_b.setCheckable(True)
    dialog.pick_point_b.setStyleSheet(STYLE_PICK_TOGGLE)
    dialog.pick_point_b.setCursor(Qt.CursorShape.PointingHandCursor)
    dialog.pick_point_b.setMinimumHeight(34)
    dialog.pick_point_b.setMinimumWidth(0)
    dialog.pick_point_b.setToolTip(_tr("Leave empty for a single-point analysis"))
    grid_b.addWidget(dialog.pick_point_b, 2, 0, 1, 2)

    # Replicate point A into B, so the same location can be compared across
    # sources without re-clicking the map.
    dialog.copy_a_to_b = _button(
        _tr("⧉  Copy coordinates from A"),
        tooltip=_tr("Copy point A's coordinates here (e.g. to compare data sources)"),
        height=34,
    )
    grid_b.addWidget(dialog.copy_a_to_b, 3, 0, 1, 2)

    # B may use its own source, so the same point can be compared across sources.
    dialog.source_combo_b = QComboBox()
    dialog.source_combo_b.addItem(_tr("(same source as A)"), None)
    dialog.source_combo_b.addItem("NASA POWER", "power")
    dialog.source_combo_b.addItem("Open-Meteo (ERA5)", "openmeteo")
    dialog.source_combo_b.setToolTip(_tr("Data source for the comparison point"))
    dialog.source_combo_b.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    src_b = QHBoxLayout()
    src_b.setSpacing(8)
    src_b.addWidget(QLabel(_tr("Source")))
    src_b.addWidget(dialog.source_combo_b, 1)
    grid_b.addLayout(src_b, 4, 0, 1, 2)
    layout.addWidget(group_b)

    # Side-by-side auxiliary buttons.
    aux = QHBoxLayout()
    aux.setSpacing(8)
    dialog.googlemaps = _button(
        _tr("Satellite layer"), "satellite.svg",
        _tr("Add a Google satellite basemap to help locate your point"), height=34)
    dialog.clear_mark = _button(
        _tr("Clear marker"), None,
        _tr("Remove the point marker from the map"), height=34)
    aux.addWidget(dialog.googlemaps)
    aux.addWidget(dialog.clear_mark)
    layout.addLayout(aux)

    layout.addStretch(1)
    scroll.setWidget(inner)
    outer.addWidget(scroll, 1)

    # Run analysis pinned outside the scroll area — always visible at the bottom.
    run_row = QHBoxLayout()
    run_row.setContentsMargins(14, 6, 14, 0)
    dialog.gerar_req = _button(
        _tr("Run analysis"), "run.svg",
        _tr("Download NASA POWER data for this point and build the charts"),
        style=STYLE_BTN_PRIMARY, height=40)
    run_row.addWidget(dialog.gerar_req)
    outer.addLayout(run_row)


# -------------------------------------------------------------------- plots
def _plot_page(dialog, page):
    """Common skeleton: a top toolbar row + an expanding web view below."""
    layout = QVBoxLayout(page)
    layout.setContentsMargins(8, 6, 8, 6)
    layout.setSpacing(6)
    row = QHBoxLayout()
    row.setContentsMargins(0, 0, 0, 0)
    row.setSpacing(6)
    layout.addLayout(row)
    desc = QLabel()
    desc.setWordWrap(False)
    desc.setStyleSheet("color:#6b7b8b;font-size:11px;font-style:italic;background:transparent;")
    desc.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    layout.addWidget(desc)
    web = _make_webview()
    layout.addWidget(web, 1)
    return row, web, desc


def _toolbar_label(text):
    lbl = QLabel(text)
    lbl.setStyleSheet("color: #5b6b7b; font-size: 12px; font-weight: bold; background: transparent;")
    lbl.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
    return lbl


def _nav_footer(dialog, back_key=None, next_key=None):
    """Back / Next footer linking sequential pages; arrows omitted when None."""
    bar = QWidget()
    lay = QHBoxLayout(bar)
    lay.setContentsMargins(0, 2, 0, 0)
    lay.setSpacing(6)
    if back_key:
        back = _button(_tr("Back"), "back.svg", _tr("Go to the previous page"))
        back.clicked.connect(lambda: dialog._goto(back_key))
        lay.addWidget(back)
    lay.addStretch(1)
    if next_key:
        nxt = _button(_tr("Next"), "next.svg", _tr("Go to the next page"))
        nxt.setLayoutDirection(Qt.LayoutDirection.RightToLeft)  # icon to the right of text
        nxt.clicked.connect(lambda: dialog._goto(next_key))
        lay.addWidget(nxt)
    return bar


def setup_trends_page(dialog, page):
    row, web, dialog.var_desc = _plot_page(dialog, page)
    dialog.atributo = _combo(_VARIABLES, _tr("Choose the climate variable to plot"),
                             min_width=160)
    dialog.atributo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    dialog.save_raw = _button(_tr("Save daily data"), "save.svg",
                              _tr("Export the full daily NASA POWER series as CSV"))
    dialog.navegador = _button(_tr("Open in browser"), "browser.svg",
                               _tr("Open this chart full-screen in your web browser"))
    dialog.save_plot = _button(_tr("Save chart data"), "save.svg",
                               _tr("Export the plotted annual series as CSV"))
    dialog.save_img = _button(_tr("Image"), "browser.svg",
                              _tr("Save the chart as a PNG image"))
    dialog.export_all = _button(_tr("Export all"), "save.svg",
                                _tr("Export every table to one Excel file"))

    # Row 1: variable selector — label + expanding combo.
    row.addWidget(_toolbar_label(_tr("Variable:")))
    row.addWidget(dialog.atributo, 1)

    # Row 2: action buttons, right-aligned.  Inserted between the variable row
    # (index 0) and the desc label (index 1) that _plot_page already placed.
    btn_row = QHBoxLayout()
    btn_row.setContentsMargins(0, 0, 0, 0)
    btn_row.setSpacing(6)
    btn_row.addStretch(1)
    btn_row.addWidget(dialog.save_raw)
    btn_row.addWidget(dialog.navegador)
    btn_row.addWidget(dialog.save_plot)
    btn_row.addWidget(dialog.save_img)
    btn_row.addWidget(dialog.export_all)
    page.layout().insertLayout(1, btn_row)

    dialog.webView_1 = web
    page.layout().addWidget(_nav_footer(dialog, back_key="coords", next_key="thermo"))


def setup_thermo_page(dialog, page):
    row, web, _thermo_desc = _plot_page(dialog, page)
    _thermo_desc.setText(_tr("Mean monthly precipitation (bars) and mean temperatures (lines) across the year."))
    dialog.navegador_2 = _button(_tr("Open in browser"), "browser.svg",
                                 _tr("Open this chart full-screen in your web browser"))
    dialog.save_plot2 = _button(_tr("Save chart data"), "save.svg",
                                _tr("Export the monthly climate normals as CSV"))
    dialog.save_img2 = _button(_tr("Image"), "browser.svg",
                               _tr("Save the chart as a PNG image"))
    row.addWidget(_toolbar_label(_tr("Mean monthly precipitation and temperature")))
    row.addStretch(1)
    row.addWidget(dialog.navegador_2)
    row.addWidget(dialog.save_plot2)
    row.addWidget(dialog.save_img2)
    dialog.webView_2 = web
    page.layout().addWidget(_nav_footer(dialog, back_key="trends", next_key="indices"))


def setup_indices_page(dialog, page):
    row, web, dialog.index_desc = _plot_page(dialog, page)
    dialog.atributo_2 = _combo(_INDICES, _tr("Choose the ETCCDI climate index to plot"), min_width=220)
    dialog.atributo_2.setCurrentIndex(0)
    dialog.navegador_3 = _button(_tr("Open in browser"), "browser.svg",
                                 _tr("Open this chart full-screen in your web browser"))
    dialog.save_plot3 = _button(_tr("Save chart data"), "save.svg",
                                _tr("Export the selected index series as CSV"))
    dialog.save_img3 = _button(_tr("Image"), "browser.svg",
                               _tr("Save the chart as a PNG image"))
    row.addWidget(_toolbar_label(_tr("Index:")))
    row.addWidget(dialog.atributo_2, 1)
    row.addWidget(dialog.navegador_3)
    row.addWidget(dialog.save_plot3)
    row.addWidget(dialog.save_img3)
    dialog.webView_3 = web
    page.layout().addWidget(_nav_footer(dialog, back_key="thermo"))
