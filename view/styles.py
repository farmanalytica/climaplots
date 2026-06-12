# -*- coding: utf-8 -*-
"""Shared UI styles for the ClimaPlots dialog (blue palette)."""

# Sidebar palette
SIDEBAR_COLLAPSED_WIDTH = 64
SIDEBAR_EXPANDED_WIDTH = 196
SIDEBAR_BLUE = "#1c3d5a"
SIDEBAR_BLUE_DARK = "#142c41"
SIDEBAR_INDICATOR = "#8ec5ff"
SIDEBAR_TEXT = "rgba(255, 255, 255, 218)"
SIDEBAR_MUTED = "rgba(255, 255, 255, 160)"

STYLE_DIALOG = """
QDialog { background-color: #f5f7fa; color: #212121; }
QWidget { color: #212121; }
QLineEdit {
    background-color: #ffffff; color: #212121;
    border: 1px solid #d6dee8; border-radius: 6px;
    padding: 6px 10px; font-size: 12px;
}
QLineEdit:focus { border-color: #2c6cab; }
QComboBox {
    background-color: #ffffff; color: #212121;
    border: 1px solid #d6dee8; border-radius: 6px;
    padding: 4px 8px; font-size: 12px; min-height: 24px;
}
QComboBox:focus { border-color: #2c6cab; }
QGroupBox {
    font-size: 13px; font-weight: bold; color: #1c3d5a;
    border: 1px solid #d6dee8; border-radius: 8px;
    margin-top: 10px; padding-top: 8px;
}
QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 4px; }
"""

STYLE_BTN_PRIMARY = """
QPushButton {
    background-color: #2c6cab; color: #ffffff; border: none;
    border-radius: 8px; font-size: 13px; font-weight: bold; padding: 0 16px;
}
QPushButton:hover { background-color: #3279bf; }
QPushButton:pressed { background-color: #245a8f; }
QPushButton:disabled { background-color: #bdc8d4; color: #f5f5f5; }
"""

STYLE_BTN = """
QPushButton {
    background-color: #2c6cab; color: #ffffff; border: none;
    border-radius: 8px; font-size: 12px; font-weight: bold; padding: 4px 10px;
}
QPushButton:hover { background-color: #3279bf; }
QPushButton:pressed { background-color: #245a8f; }
QPushButton:disabled { background-color: #bdc8d4; color: #f5f5f5; }
"""

# Checkable "Pick point on map" toggle: idle (blue) vs capturing (green, with a
# clear active border) so the on/off state is obvious at a glance.
STYLE_PICK_TOGGLE = """
QPushButton {
    background-color: #2c6cab; color: #ffffff;
    border: none; border-radius: 6px;
    padding: 7px; font-weight: bold;
}
QPushButton:hover { background-color: #3279bf; }
QPushButton:checked {
    background-color: #1e9e57; color: #ffffff;
    border: 2px solid #14753f;
}
QPushButton:checked:hover { background-color: #21ad5f; }
QPushButton:disabled { background-color: #bdc8d4; color: #f5f5f5; }
"""

# Round "?" help button in the header.
STYLE_BTN_HELP = """
QPushButton {
    background-color: transparent; color: #9aa7b4;
    border: 1.5px solid #d0d9e2; border-radius: 14px;
    font-size: 13px; font-weight: bold;
}
QPushButton:hover { background-color: #eef3f8; color: #2c6cab; border-color: #2c6cab; }
"""

# Subtle flat link-style button (e.g. the corner "Proxy settings" entry).
STYLE_BTN_SUBTLE = """
QPushButton {
    background: transparent; color: #8a98a6;
    border: none; font-size: 11px; padding: 4px 8px;
}
QPushButton:hover { color: #2c6cab; }
"""
