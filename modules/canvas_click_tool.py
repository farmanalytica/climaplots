# -*- coding: utf-8 -*-
"""Map-click coordinate capture for ClimaPlots ("clicking mode").

Inspired by the fieldguide plugin's ``CanvasMarkerTool``: instead of
permanently hijacking the QGIS map tool, this is an explicit, toggleable
capture mode. ``enable()`` remembers the user's current map tool and switches
to a point-emitter; ``disable()`` restores it. ClimaPlots needs a single point,
so a click captures one coordinate, draws one marker, emits ``point_picked``
and auto-disables.
"""
from qgis.PyQt.QtCore import QObject, Qt, pyqtSignal
from qgis.PyQt.QtGui import QColor
from qgis.core import (
    Qgis,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
)
from qgis.gui import QgsMapToolEmitPoint, QgsVertexMarker


def _left_button():
    scoped = getattr(Qt, "MouseButton", None)
    return scoped.LeftButton if scoped is not None else Qt.LeftButton


class CanvasClickTool(QObject):
    """Toggleable single-point capture with marker + previous-tool restore."""

    point_picked = pyqtSignal(float, float)  # longitude, latitude (WGS84)

    def __init__(self, iface, parent=None):
        super().__init__(parent)
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self._tool = None
        self._previous_tool = None
        self._marker = None
        self._wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")

    def _ensure_tool(self):
        if self._tool is None:
            self._tool = QgsMapToolEmitPoint(self.canvas)
            self._tool.canvasClicked.connect(self._on_clicked)

    def is_active(self):
        return self._tool is not None and self.canvas.mapTool() is self._tool

    def enable(self):
        """Activate capture mode, remembering the current map tool."""
        self._ensure_tool()
        if self.canvas.mapTool() is not self._tool:
            self._previous_tool = self.canvas.mapTool()
        self.canvas.setMapTool(self._tool)
        try:
            self.iface.messageBar().pushMessage(
                "ClimaPlots", "Click a point on the map to set the coordinate.",
                level=Qgis.Info, duration=3,
            )
        except Exception:
            pass

    def disable(self):
        """Deactivate capture mode and restore the previous map tool."""
        if self._tool is not None and self.canvas.mapTool() is self._tool:
            if self._previous_tool is not None:
                self.canvas.setMapTool(self._previous_tool)
            else:
                self.canvas.unsetMapTool(self._tool)
        self._previous_tool = None

    def _on_clicked(self, point, button):
        if button != _left_button():
            return
        source_crs = self.canvas.mapSettings().destinationCrs()
        transform = QgsCoordinateTransform(source_crs, self._wgs84, QgsProject.instance())
        wgs = transform.transform(point)
        self._draw_marker(point)
        self.point_picked.emit(round(wgs.x(), 4), round(wgs.y(), 4))
        # Capture mode stays active until the user toggles it off; each click
        # just moves the captured point and marker.

    def _draw_marker(self, map_point):
        self.clear_marker()
        marker = QgsVertexMarker(self.canvas)
        marker.setCenter(map_point)
        marker.setColor(QColor(255, 0, 0))
        marker.setIconType(QgsVertexMarker.ICON_X)
        marker.setIconSize(12)
        marker.setPenWidth(4)
        self._marker = marker

    def clear_marker(self):
        if self._marker is not None:
            try:
                self.canvas.scene().removeItem(self._marker)
            except Exception:
                pass
            self._marker = None
