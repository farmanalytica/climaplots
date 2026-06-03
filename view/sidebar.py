# -*- coding: utf-8 -*-
"""Permanent, hover-expanding navigation sidebar for the ClimaPlots dialog.

Replaces the old QTabWidget. Emits one signal per page; the dialog connects
them to switch the QStackedWidget. Mirrors the sidebar used by the sibling
plugins (qgis-EasyDEM, terra_valora).
"""
import os

from qgis.PyQt.QtCore import QCoreApplication, QEasingCurve, QRectF, Qt, QSize, QVariantAnimation, pyqtSignal
from qgis.PyQt.QtGui import QColor, QIcon, QPainter, QPen, QPixmap
from qgis.PyQt.QtWidgets import (
    QButtonGroup,
    QFrame,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)

from .styles import (
    SIDEBAR_BLUE,
    SIDEBAR_BLUE_DARK,
    SIDEBAR_COLLAPSED_WIDTH,
    SIDEBAR_EXPANDED_WIDTH,
    SIDEBAR_INDICATOR,
    SIDEBAR_MUTED,
    SIDEBAR_TEXT,
)

def _tr(text):
    return QCoreApplication.translate("ClimaPlots", text)


# (page key, label, icon kind)
_PAGES = [
    ("intro", "Intro", "intro"),
    ("coords", "Coordinates", "coords"),
    ("trends", "Trends", "trends"),
    ("thermo", "Thermo-pluviometric", "thermo"),
    ("indices", "Indices", "indices"),
]


class _NavButton(QPushButton):
    """Navigation button with a rounded active indicator on the left edge."""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._indicator_color = QColor(SIDEBAR_INDICATOR)

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.isChecked():
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._indicator_color)
        height = 28 if self.width() > 80 else 22
        y = (self.height() - height) / 2
        painter.drawRoundedRect(QRectF(0, y, 3.5, height), 1.75, 1.75)
        painter.end()


class Sidebar(QFrame):
    """Collapsible left navigation with one checkable button per page."""

    intro_requested = pyqtSignal()
    coords_requested = pyqtSignal()
    trends_requested = pyqtSignal()
    thermo_requested = pyqtSignal()
    indices_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self._expanded = False
        self._buttons = {}
        self.setFixedWidth(SIDEBAR_COLLAPSED_WIDTH)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self._width_animation = QVariantAnimation(self)
        self._width_animation.setDuration(160)
        self._width_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._width_animation.valueChanged.connect(self._set_animated_width)

        self._build()
        self._apply_expanded_state(False)
        self.set_active_page("intro")

    def _build(self):
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(10, 14, 10, 18)
        self._layout.setSpacing(8)

        # Plugin logo at the top.
        self.logo = QLabel()
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo.setStyleSheet("background: transparent; border: none;")
        logo_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icon.png"
        )
        self._logo_pix = QPixmap(logo_path)
        self.logo.setFixedHeight(40)
        self._layout.addWidget(self.logo)
        self._layout.addSpacing(6)

        self._group = QButtonGroup(self)
        self._group.setExclusive(True)

        signal_for = {
            "intro": self.intro_requested,
            "coords": self.coords_requested,
            "trends": self.trends_requested,
            "thermo": self.thermo_requested,
            "indices": self.indices_requested,
        }
        for key, label, kind in _PAGES:
            btn = self._make_button(_tr(label), kind)
            btn.clicked.connect(signal_for[key].emit)
            self._buttons[key] = btn
            self._group.addButton(btn)
            self._layout.addWidget(btn)

        self._layout.addStretch()

        self.version_label = QLabel("v2.0")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.version_label.setStyleSheet(
            f"color: {SIDEBAR_MUTED}; font-size: 9px; background: transparent; border: none;"
        )
        self._layout.addWidget(self.version_label)

    def _make_button(self, text, kind):
        btn = _NavButton(text)
        btn.setObjectName("sidebarNavButton")
        btn.setProperty("navText", text)
        btn.setCheckable(True)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedHeight(42)
        btn.setIcon(self._make_icon(kind))
        btn.setIconSize(QSize(20, 20))
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn.setToolTip(text)
        return btn

    def set_active_page(self, page):
        for key, btn in self._buttons.items():
            btn.setChecked(key == page)

    # ---- hover expand / collapse ----
    def enterEvent(self, event):
        self._apply_expanded_state(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._apply_expanded_state(False)
        super().leaveEvent(event)

    def _apply_expanded_state(self, expanded):
        self._expanded = expanded
        margin = 14 if expanded else 11
        self._layout.setContentsMargins(margin, 14, margin, 18)
        if self._logo_pix is not None and not self._logo_pix.isNull():
            self.logo.setPixmap(self._logo_pix.scaledToHeight(
                36 if expanded else 30, Qt.TransformationMode.SmoothTransformation))
        for btn in self._buttons.values():
            btn.setText(btn.property("navText") if expanded else "")
            btn.setToolTip("" if expanded else btn.property("navText"))
            btn.setFixedWidth(168 if expanded else 42)
        self.setStyleSheet(self._stylesheet(expanded))
        self._animate_width(SIDEBAR_EXPANDED_WIDTH if expanded else SIDEBAR_COLLAPSED_WIDTH)

    def _animate_width(self, target):
        if self.width() == target:
            return
        self._width_animation.stop()
        self._width_animation.setStartValue(self.width())
        self._width_animation.setEndValue(target)
        self._width_animation.start()

    def _set_animated_width(self, width):
        self.setFixedWidth(int(width))

    def _stylesheet(self, expanded):
        align = "left" if expanded else "center"
        padding = "0 12px 0 10px" if expanded else "0"
        width = "168px" if expanded else "42px"
        return f"""
        QFrame#Sidebar {{
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {SIDEBAR_BLUE}, stop:1 {SIDEBAR_BLUE_DARK});
            border: none;
        }}
        QPushButton#sidebarNavButton {{
            background-color: transparent; color: {SIDEBAR_TEXT};
            border: none; border-radius: 8px;
            font-size: 12px; font-weight: bold; text-align: {align};
            padding: {padding}; min-width: {width}; max-width: {width};
            min-height: 42px; max-height: 42px;
        }}
        QPushButton#sidebarNavButton:hover {{
            background-color: rgba(255,255,255,22); color: #ffffff;
        }}
        QPushButton#sidebarNavButton:checked {{
            background-color: transparent; color: #ffffff;
        }}
        """

    def _make_icon(self, kind):
        icon = QIcon()
        icon.addPixmap(self._draw_icon(kind, "#DCEBFA"), QIcon.Mode.Normal, QIcon.State.Off)
        icon.addPixmap(self._draw_icon(kind, "#FFFFFF"), QIcon.Mode.Normal, QIcon.State.On)
        return icon

    def _draw_icon(self, kind, color):
        pix = QPixmap(20, 20)
        pix.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pix)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(QColor(color), 1.8)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)

        if kind == "intro":
            painter.drawEllipse(QRectF(4, 4, 12, 12))
            painter.drawLine(10, 9, 10, 14)
            painter.drawPoint(10, 6)
        elif kind == "coords":
            painter.drawEllipse(QRectF(7, 3, 6, 6))
            painter.drawLine(10, 9, 10, 17)
        elif kind == "trends":
            painter.drawLine(3, 15, 8, 9)
            painter.drawLine(8, 9, 12, 12)
            painter.drawLine(12, 12, 17, 5)
        elif kind == "thermo":
            painter.drawRect(QRectF(3, 12, 3, 5))
            painter.drawRect(QRectF(8, 8, 3, 9))
            painter.drawRect(QRectF(13, 5, 3, 12))
        else:  # indices
            painter.drawLine(3, 5, 17, 5)
            painter.drawLine(3, 10, 17, 10)
            painter.drawLine(3, 15, 17, 15)
        painter.end()
        return pix
