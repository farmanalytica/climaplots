# -*- coding: utf-8 -*-
"""Facade that sequences the heavy analysis pipeline. Pure logic, no Qt.

This is the single entry point the background worker calls: fetch the raw data
from NASA POWER, compute the climate indices, and return one typed
:class:`ClimateData` object. Cheap figure building is done separately on the GUI
thread via :mod:`plot_service`.
"""
from . import indices_service, nasa_power_service
from .types import ClimateData


def run_analysis(longitude, latitude, proxy="", warn=None, start_year=None, end_year=None,
                 longitude_b=None, latitude_b=None):
    """Fetch climate data and compute indices for a coordinate.

    Args:
        longitude / latitude: queried point.
        proxy: optional proxy URL.
        warn: optional callable(str) for per-index failure messages.
        start_year / end_year: inclusive year range (None -> service defaults).

    Returns:
        ClimateData with the raw dataframe and the computed indices.
    """
    sy = start_year or nasa_power_service.MIN_YEAR
    df = nasa_power_service.fetch(longitude, latitude, proxy, start_year=sy, end_year=end_year)
    indices = indices_service.compute(df, warn=warn or (lambda _m: None))

    df_b = None
    if longitude_b not in (None, "") and latitude_b not in (None, ""):
        # Comparison point: raw series only (no indices), for the trends overlay.
        df_b = nasa_power_service.fetch(longitude_b, latitude_b, proxy, start_year=sy, end_year=end_year)

    return ClimateData(
        df=df, indices=indices, longitude=str(longitude), latitude=str(latitude),
        df_b=df_b, longitude_b=str(longitude_b or ""), latitude_b=str(latitude_b or ""),
    )
