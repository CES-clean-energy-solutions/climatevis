import plotly.graph_objects as go
import pandas as pd
from util import util_plotly

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
import plotly.graph_objects as go
import pandas as pd
from util import util_plotly

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def plot_timeseries_df(df, **kwargs):
    """
    Wrapper function for plot_series that accepts a DataFrame and passes its columns as Series.

    Parameters:
    - df (pd.DataFrame): DataFrame with DatetimeIndex and one or more columns.
    - kwargs: Additional keyword arguments passed to plot_series.

    Returns:
    - fig (plotly.graph_objects.Figure): The generated Plotly figure.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a Pandas DataFrame.")
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("DataFrame must have a DatetimeIndex.")
    series_list = [df[col].rename(col) for col in df.columns]
    return plot_series(series_list, **kwargs)

def plot_series(series_list, template_name='base-auto', paper_size='A4_LANDSCAPE', y1_axis_title="", mode="line", show_days=False):
    """
    Plots a time series using Plotly with customizable display options.

    Parameters:
    - series_list (list of pd.Series): List of Pandas Series with a DatetimeIndex.
    - template_name (str): Name of the Plotly template to apply.
    - paper_size (tuple): Tuple specifying the paper size for the plot.
    - y1_axis_title (str, optional): Title for the primary y-axis.
    - mode (str, optional): Type of plot ('line', 'area', 'bar', 'markers'). Default is 'line'.
    - show_days (bool, optional): If True, adds vertical grid lines at daily intervals. Default is False.

    Returns:
    - fig (plotly.graph_objects.Figure): The generated Plotly figure.

    Raises:
    - ValueError: If the input series list is invalid, or series indices do not match.
    """
    if not isinstance(series_list, list) or len(series_list) < 1:
        raise ValueError("Input must be a list of at least one Pandas Series.")

    index_ref = series_list[0].index
    if not isinstance(index_ref, pd.DatetimeIndex):
        raise ValueError("All series must have a DatetimeIndex.")

    for series in series_list:
        if not isinstance(series, pd.Series):
            raise ValueError("Each item in series_list must be a Pandas Series.")
        if not isinstance(series.index, pd.DatetimeIndex):
            raise ValueError("Each series must have a DatetimeIndex.")
        if not series.index.equals(index_ref):
            raise ValueError("All series must have the same DatetimeIndex.")

    units = set()
    series_data = []
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

    for i, series in enumerate(series_list):
        name = getattr(series, 'name', 'Unnamed')
        unit = series.attrs.get("unit", None)
        units.add(unit)
        series_data.append({'series': series, 'name': name, 'unit': unit, 'color': colors[i % len(colors)]})

    if len(units) > 2:
        raise ValueError("More than two unique units detected. Only up to two units are supported.")

    y1_label = "{} ({})".format(y1_axis_title, list(units)[0]) if len(units) > 0 else y1_axis_title
    y2_label = "{} ({})".format(y1_axis_title, list(units)[1]) if len(units) == 2 else None

    fig = go.Figure()

    for data in series_data:
        y_axis = "y2" if y2_label and data['unit'] == list(units)[1] else "y1"
        trace_kwargs = {
            "x": data['series'].index,
            "y": data['series'].values,
            "name": data['name'],
            "yaxis": y_axis,
            "marker": {"color": data['color']}
        }

        if mode == "line":
            trace = go.Scatter(mode="lines", **trace_kwargs)
        elif mode == "area":
            trace = go.Scatter(mode="lines", fill="tozeroy", **trace_kwargs)
        elif mode == "bar":
            trace = go.Bar(**trace_kwargs)
        elif mode == "markers":
            trace = go.Scatter(mode="markers", **trace_kwargs)
        else:
            raise ValueError("Invalid mode. Choose from 'line', 'area', 'bar', or 'markers'.")

        fig.add_trace(trace)

    layout = {
        "xaxis_title": "Time",
        "yaxis": {
            "title": y1_label,
            "side": "left",
            "showgrid": True
        },
        "barmode": "overlay" if mode == "bar" else None
    }

    if y2_label:
        layout["yaxis2"] = {
            "title": y2_label,
            "overlaying": "y",
            "side": "right",
            "showgrid": False
        }

    if show_days:
        min_time = index_ref.min()
        max_time = index_ref.max()
        day_ticks = pd.date_range(start=min_time, end=max_time, freq='D')
        layout["xaxis"] = {
            "tickmode": "array",
            "tickvals": day_ticks,
            "tickformat": "%Y-%m-%d",
            "showgrid": True,
            "gridcolor": "lightgray"
        }

    fig.update_layout(layout)
    fig = util_plotly.apply_template_to_figure(fig, template_name=template_name, paper_size=paper_size)
    return fig
