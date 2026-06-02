# -*- coding: utf-8 -*-
"""NASA POWER data acquisition. Pure logic, no Qt.

Fetches daily climate data (max/min temperature, precipitation, relative
humidity and surface irradiation) from NASA's POWER API for a point and returns
a tidy pandas DataFrame.
"""
import datetime
import json

import numpy as np
import pandas as pd
import requests

# Request max/min temperature, corrected precipitation, 2m relative humidity and
# all-sky surface shortwave downwelling (irradiation) from the daily point API.
_BASE_URL = (
    "https://power.larc.nasa.gov/api/temporal/daily/point?"
    "parameters=T2M_MAX,PRECTOTCORR,T2M_MIN,RH2M,ALLSKY_SFC_SW_DWN&community=RE&"
    "longitude={longitude}&latitude={latitude}&"
    "start=19810101&end={end}&format=JSON"
)

_COLUMN_RENAME = {
    "index": "Date",
    "PRECTOTCORR": "Precipitation",
    "T2M_MIN": "Min Temperature",
    "T2M_MAX": "Max Temperature",
    "RH2M": "Relative Humidity",
    "ALLSKY_SFC_SW_DWN": "Irradiation",
}


def _end_date():
    """End at 31 Dec of last year to guarantee complete-year data."""
    return str(int(datetime.date.today().strftime("%Y")) - 1) + "1231"


def fetch(longitude, latitude, proxy=""):
    """Fetch daily climate data for a coordinate.

    Args:
        longitude / latitude: point coordinates (str or float).
        proxy: optional proxy URL; if it fails the request is retried directly.

    Returns:
        pandas.DataFrame with a datetime ``Date`` column and the renamed
        climate variables.
    """
    url = _BASE_URL.format(
        longitude=float(longitude), latitude=float(latitude), end=_end_date()
    )

    proxies = {"http": proxy, "https": proxy} if proxy else None
    response = _request_with_optional_proxy(url, proxies)

    content = json.loads(response.content.decode("utf-8"))
    df = pd.DataFrame.from_dict(content["properties"]["parameter"])
    df = df.reset_index().rename(columns=_COLUMN_RENAME)

    # API uses -999.0 as the irradiation fill value.
    df["Irradiation"] = df["Irradiation"].replace(-999.0, np.nan)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Irradiation"] = pd.to_numeric(df["Irradiation"], errors="coerce")
    return df


def _request_with_optional_proxy(url, proxies):
    """GET the URL, trying the proxy first then falling back to a direct call."""
    if proxies:
        try:
            return requests.get(url=url, verify=True, timeout=1000, proxies=proxies)
        except Exception:
            # Proxy failed - retry without it before giving up.
            return requests.get(url=url, verify=True, timeout=1000)
    return requests.get(url=url, verify=True, timeout=1000)
