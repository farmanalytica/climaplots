# -*- coding: utf-8 -*-
"""Thin wrapper around QSettings for ClimaPlots, with prefixed keys.

Mirrors the settings_manager convention used by the sibling plugins
(qgis-EasyDEM, terra_valora) so persistence lives in one place instead of being
scattered through the dialog.
"""
from qgis.PyQt.QtCore import QSettings

_PREFIX = "climaplots/"


def get_proxy():
    """Return the configured proxy URL (empty string if unset)."""
    return QSettings().value(_PREFIX + "proxy", "") or ""


def set_proxy(proxy):
    """Persist the proxy URL (pass an empty string to clear it)."""
    QSettings().setValue(_PREFIX + "proxy", (proxy or "").strip())
