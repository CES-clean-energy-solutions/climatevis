import plotly.graph_objects as go
import pandas as pd
import numpy as np
from climatevis.util import util_plotly
from climatevis.util.validation import validate_plot_parameters

# def annual_profile_from_df(df: pd.DataFrame, column_name: str, paper_size='A5_LANDSCAPE'):
#     template_name = 'base'
#     x_title="Day of Year"
#     return annual_profile(df[column_name], template_name, paper_size, x_title, column_name)

def annual_profile_daily(series: pd.Series, template_name: str, paper_size: str, x_title="Day of Year", y_title="Value", show=["max", "min", "mean"]):
    """
    Plots an annual profile of a given time series with min, mean, and max values per day.
    Adds month labels at their first day positions on the x-axis.

    Parameters:
    - series: pd.Series with a DatetimeIndex containing the metric to be plotted.
    - x_title: str, label for the x-axis (default: "Day of Year").
    - y_title: str, label for the y-axis (custom, depends on the metric being plotted).
    - show: list of str, values to display among ['max', 'min', 'mean']. Defaults to all.

    Returns:
    - Plotly Figure
    """
    # Validate inputs using the validation utility
    validate_plot_parameters(
        series,
        template_name,
        paper_size,
        function_name="annual_profile_daily"
    )

    # Convert series to DataFrame and extract day-of-year
    df = series.to_frame(name="metric")
    df["day_of_year"] = df.index.dayofyear

    # Group by day-of-year and calculate min, mean, and max
    daily_stats = df.groupby("day_of_year")["metric"].agg(["min", "mean", "max"])

    fig = go.Figure()

    # Add Min Line if requested
    if "min" in show:
        fig.add_trace(go.Scatter(
            x=daily_stats.index,
            y=daily_stats["min"],
            mode='lines',
            name=f"Min {y_title}",
            line=dict(color="blue")
        ))

    # Add Mean Line if requested
    if "mean" in show:
        fig.add_trace(go.Scatter(
            x=daily_stats.index,
            y=daily_stats["mean"],
            mode='lines',
            name=f"Mean {y_title}",
            line=dict(color="grey", width=1)
        ))

    # Add Max Line if requested
    if "max" in show:
        fig.add_trace(go.Scatter(
            x=daily_stats.index,
            y=daily_stats["max"],
            mode='lines',
            name=f"Max {y_title}",
            line=dict(color="red")
        ))

    # Compute first day-of-year for each month
    months = pd.date_range("2023-01-01", "2023-12-31", freq="MS")  # MS = Month Start
    month_positions = {date.strftime("%b"): date.dayofyear + 14 for date in months}  # Adjust to 15th

    # Add month labels at their respective positions along the 0-line
    for month, day in month_positions.items():
        fig.add_annotation(
            x=day, y=min(series),  # Align to the minimum value of the series
            text=f"<b>{month}</b>",
            showarrow=False,
            xanchor="center",
            yanchor="top",
            font=dict(size=12),
            bgcolor="white",
        )

    # Update layout
    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
        showlegend=False
    )

    # Apply custom template
    fig = util_plotly.apply_template_to_figure(fig, template_name=template_name, paper_size=paper_size)

    return fig


def annual_profile_multiple(series_list: list, template_name: str, paper_size: str, x_title="Day of Year", y_title="Value", show='max'):
    """
    Plots an annual profile for multiple time series for a single selected statistic.
    Adds month labels at their first day positions on the x-axis.

    Parameters:
    - series_list: list of pd.Series, each with a DatetimeIndex containing the metric to be plotted.
    - x_title: str, label for the x-axis (default: "Day of Year").
    - y_title: str, label for the y-axis (custom, depends on the metric being plotted).
    - show: str, one of ['max', 'min', 'mean'] indicating the statistic to display (default: 'max').

    Returns:
    - Plotly Figure
    """
    allowed_stats = {'max', 'min', 'mean'}
    if show not in allowed_stats:
        raise ValueError(f"Parameter 'show' must be one of {allowed_stats}.")

    fig = go.Figure()

    # To determine a common minimum for month labels, collect all min values
    overall_mins = []

    for i, series in enumerate(series_list):
        if not isinstance(series.index, pd.DatetimeIndex):
            raise ValueError("Each series index must be a DatetimeIndex.")

        # Convert series to DataFrame and extract day-of-year
        df = series.to_frame(name="metric")
        df["day_of_year"] = df.index.dayofyear

        # Group by day-of-year and calculate the selected statistic
        daily_stats = df.groupby("day_of_year")["metric"].agg(show)

        # Add the statistic value for this series to overall_mins for later month label positioning
        overall_mins.append(series.min())

        # Determine the series label: use the series name if it exists, otherwise a default
        label = series.name if series.name is not None else f"Series {i+1}"
        label = f"{label} ({show})"

        fig.add_trace(go.Scatter(
            x=daily_stats.index,
            y=daily_stats,
            mode='lines',
            name=label
        ))

    # Compute overall minimum value for placing month labels
    overall_min = min(overall_mins) if overall_mins else 0

    # Compute first day-of-year for each month
    months = pd.date_range("2023-01-01", "2023-12-31", freq="MS")  # MS = Month Start
    month_positions = {date.strftime("%b"): date.dayofyear + 14 for date in months}  # Adjust to 15th

    # Add month labels at their respective positions along the overall minimum value line
    for month, day in month_positions.items():
        fig.add_annotation(
            x=day, y=overall_min,
            text=f"<b>{month}</b>",
            showarrow=False,
            xanchor="center",
            yanchor="top",
            font=dict(size=12),
            bgcolor="white",
        )

    # Update layout
    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
        showlegend=True
    )

    # Apply custom template
    fig = util_plotly.apply_template_to_figure(fig, template_name=template_name, paper_size=paper_size)

    return fig