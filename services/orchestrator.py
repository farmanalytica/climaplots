# -*- coding: utf-8 -*-
"""Facade that sequences the heavy analysis pipeline. Pure logic, no Qt.

This is the single entry point the background worker calls: fetch the raw data
from NASA POWER, compute the climate indices, and return one typed
:class:`ClimateData` object. Cheap figure building is done separately on the GUI
thread via :mod:`plot_service`.
"""
from . import indices_service, nasa_power_service
from .types import ClimateData


def run_analysis(longitude, latitude, proxy="", warn=None):
    """Fetch climate data and compute indices for a coordinate.

    Args:
        longitude / latitude: queried point.
        proxy: optional proxy URL.
        warn: optional callable(str) for per-index failure messages.

    Returns:
        ClimateData with the raw dataframe and the computed indices.
    """
    df = nasa_power_service.fetch(longitude, latitude, proxy)
    indices = indices_service.compute(df, warn=warn or (lambda _m: None))
    return ClimateData(
        df=df, indices=indices, longitude=str(longitude), latitude=str(latitude)
    )
