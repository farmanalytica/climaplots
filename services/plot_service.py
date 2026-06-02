# -*- coding: utf-8 -*-
"""Figure building. Pure logic, no Qt.

Each builder returns a :class:`PlotResult` (a plotly figure + the dataframe
behind it for CSV export). Figure building is cheap and reacts to dropdown
changes, so it stays on the GUI thread; the expensive fetch/compute lives in the
worker. A :class:`PlotDataError` is raised when the requested variable is not
available, so the dialog can show a friendly warning.
"""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from . import stats_service
from .types import PlotResult


class PlotDataError(Exception):
    """Raised when the requested variable/index cannot be plotted."""


_YAXIS_TITLES = {
    "Precipitation": "Precipitation (mm) - Annual Total",
    "Min Temperature": "Min Temperature (ºC) - Annual Mean",
    "Max Temperature": "Max Temperature (ºC) - Annual Mean",
    "Irradiation": "Irradiation (kWh/m²/day) - Annual Mean",
    "Relative Humidity": "Relative Humidity (%) - Annual Mean",
}


def annual_trends(df, atributo, longitude, latitude):
    """Annual trend line for one variable, titled with MK + Pettitt results."""
    df = df.copy()
    df["Year"] = df["Date"].dt.year
    df_aux = df.groupby("Year")[["Precipitation"]].sum()

    mean_candidates = ["Min Temperature", "Max Temperature", "Relative Humidity", "Irradiation"]
    mean_cols = [c for c in mean_candidates if c in df.columns]
    if mean_cols:
        df_mean = df.groupby("Year").mean()[mean_cols]
    else:
        df_mean = pd.DataFrame(index=df_aux.index)

    df_mean["Precipitation"] = df_aux["Precipitation"]
    df_mean.reset_index(inplace=True)
    df_mean["Date"] = pd.to_datetime(df_mean["Year"].astype(str) + "-01-01")

    if atributo not in df_mean.columns:
        raise PlotDataError(
            f"Attribute '{atributo}' is not available for the selected location."
        )

    df_plot = df_mean[["Date", atributo]].copy()
    df_plot.index = df_plot["Date"]
    df_plot = df_plot[[atributo]].astype(float)

    title = stats_service.stats_title(df_plot)
    fig = px.line(
        df_mean, x="Date", y=[atributo],
        title=f"<b>{atributo}</b> (Long: {longitude} Lat: {latitude}) <br>{title}",
    )
    fig.update_layout(showlegend=False)
    if atributo in _YAXIS_TITLES:
        fig.update_yaxes(title_text=_YAXIS_TITLES[atributo])

    if "Year" not in df_mean.columns:
        df_mean["Year"] = pd.to_datetime(df_mean["Date"]).dt.year
    return PlotResult(figure=fig, data=df_mean)


def thermopluviometric(df, longitude, latitude):
    """Monthly precipitation bars + temperature lines (dual-axis)."""
    df = df.copy()
    df_aux = df.groupby([df.Date.dt.year, df.Date.dt.month]).sum(numeric_only=True)[["Precipitation"]]
    df = df.groupby([df.Date.dt.year, df.Date.dt.month]).mean(numeric_only=True)[["Min Temperature", "Max Temperature"]]
    df["Precipitation"] = df_aux["Precipitation"]
    df.reset_index(level=1, inplace=True)
    df = df.groupby(df.Date).mean()
    df.reset_index(inplace=True)
    df.rename(columns={"Date": "Month"}, inplace=True)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=df["Month"], y=df["Precipitation"], name="Precipitation", marker_color="#3498db"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=df["Month"], y=df["Max Temperature"], mode="lines+markers",
                   name="Max Temperature", line=dict(color="#e67e22"), marker=dict(color="#e67e22")),
        secondary_y=True,
    )
    if "Min Temperature" in df.columns:
        fig.add_trace(
            go.Scatter(x=df["Month"], y=df["Min Temperature"], mode="lines+markers",
                       name="Min Temperature", line=dict(color="#2ecc71", dash="dot"), marker=dict(color="#2ecc71")),
            secondary_y=True,
        )

    fig.update_layout(
        title_text=f"<b>Thermo-pluviometric diagram</b> (Long: {longitude} Lat: {latitude})",
        xaxis=dict(tickmode="linear"),
    )
    fig.update_xaxes(title_text="Month")
    fig.update_yaxes(title_text="Temperature (ºC)", secondary_y=True)
    fig.update_yaxes(title_text="Precipitation (mm)", secondary_y=False)

    try:
        dt = pd.to_datetime(df["Month"], errors="coerce")
        if not dt.isna().all():
            df["Year"] = dt.dt.year
    except Exception:
        pass
    return PlotResult(figure=fig, data=df)


def index_plot(indices, selected, longitude, latitude):
    """Line plot for one computed climate index, titled with MK + Pettitt."""
    if selected not in indices:
        raise PlotDataError(f"No computed data available for '{selected}'")

    df_plot = indices[selected].copy()
    ycol = _pick_y_column(df_plot, selected)

    if "Date" in df_plot.columns:
        df_test = df_plot[[ycol]].copy()
        df_test.index = pd.to_datetime(df_plot["Date"])
    else:
        df_test = df_plot[[ycol]].copy()
    test_title = stats_service.stats_title(df_test, index=df_test.index)

    full_title = f"<b>{selected}</b> (Long: {longitude} Lat: {latitude})<br>{test_title}"
    if "Date" in df_plot.columns:
        fig = px.line(df_plot, x="Date", y=ycol, title=full_title)
    else:
        fig = px.line(df_plot, y=ycol, title=full_title)
    fig.update_layout(showlegend=False)

    _add_year_column(df_plot)
    return PlotResult(figure=fig, data=df_plot)


def _pick_y_column(df_plot, selected):
    """Choose which column to plot: exact match, sole column, or first numeric."""
    if selected in df_plot.columns:
        return selected
    if df_plot.shape[1] == 1:
        return df_plot.columns[0]
    numeric_cols = df_plot.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_cols:
        return numeric_cols[0]
    raise PlotDataError(f"No numeric column found for '{selected}'")


def _add_year_column(df_plot):
    """Attach a Year column for export, from a Date column or the index."""
    if "Date" in df_plot.columns:
        df_plot["Year"] = pd.to_datetime(df_plot["Date"]).dt.year
        return
    try:
        idx = df_plot.index
        if pd.api.types.is_datetime64_any_dtype(idx) or pd.api.types.is_datetime64_any_dtype(
            pd.to_datetime(idx, errors="coerce")
        ):
            df_plot["Year"] = pd.to_datetime(idx).year
        elif pd.api.types.is_integer_dtype(idx):
            vals = np.array(idx, dtype="int")
            if vals.size and vals.min() >= 1800 and vals.max() <= 2100:
                df_plot["Year"] = vals
    except Exception:
        pass
