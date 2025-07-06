import plotly.graph_objects as go
import pandas as pd
import numpy as np
from climatevis.util import util_plotly
from climatevis.util.validation import validate_plot_parameters

def monthly_profiles(series: pd.Series, template_name: str, paper_size: str, x_title="Hour of Day", y_title="Value"):
    """
    Plots a daily profile for each month, where each month has a separate 24-hour day.
    Each hour in the day aggregates data from all days within that month (Min, Mean, Max).

    Parameters:
    - series: pd.Series with a DatetimeIndex containing the metric to be plotted.
    - x_title: str, label for the x-axis (default: "Hour of Day").
    - y_title: str, label for the y-axis (custom, depends on the metric being plotted).

    Returns:
    - Plotly Figure
    """
    # Validate inputs using the validation utility
    validate_plot_parameters(
        series,
        template_name,
        paper_size,
        function_name="monthly_profiles"
    )

    # Convert series to DataFrame and extract month + hour
    df = series.to_frame(name="metric")
    df["month"] = df.index.month
    df["hour"] = df.index.hour

    # Group by month and hour to compute min, mean, and max
    hourly_stats = df.groupby(["month", "hour"])["metric"].agg(["min", "mean", "max"]).reset_index()

    fig = go.Figure()

    # Define month names (to align with x-axis)
    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Shift x-axis positions so that each month gets its own 24-hour "day"
    for i, month in enumerate(range(1, 13)):  # Loop through months 1-12
        month_data = hourly_stats[hourly_stats["month"] == month]
        shifted_x = month_data["hour"] + (i * 24)  # Offset each month's data on x-axis

        # Add Min Line
        fig.add_trace(go.Scatter(
            x=shifted_x,
            y=month_data["min"],
            mode='lines',
            name=f"{month_labels[i]} Min",
            line=dict(color="blue"),
            showlegend=(i == 0)  # Show legend only once
        ))

        # Add Mean Line
        fig.add_trace(go.Scatter(
            x=shifted_x,
            y=month_data["mean"],
            mode='lines',
            name=f"{month_labels[i]} Mean",
            line=dict(color="black", dash="dot"),
            showlegend=(i == 0)  # Show legend only once
        ))

        # Add Max Line
        fig.add_trace(go.Scatter(
            x=shifted_x,
            y=month_data["max"],
            mode='lines',
            name=f"{month_labels[i]} Max",
            line=dict(color="red"),
            showlegend=(i == 0)  # Show legend only once
        ))

    # Add month labels centered at each day's position
    for i, month in enumerate(month_labels):
        fig.add_annotation(
            x=(i * 24) + 12, y=min(series),  # Centered in each month's 24-hour block
            text=f"<b>{month}</b>",
            showarrow=False,
            xanchor="center",
            yanchor="top",
            font=dict(size=12),
            bgcolor="white",
            # bordercolor="black",
            # borderwidth=1
        )

    # Update layout
    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
        # showlegend=True,
        # xaxis=dict(
        #     tickmode="array",
        #     tickvals=[i * 24 for i in range(12)],
        #     # ticktext=[f"{month} 00:00" for month in month_labels]
        #     ticktext=[f"" for month in month_labels]
        # ),
        xaxis=dict(
            tickmode="array",
            tickvals=[i * 24 for i in range(12)],
            # ticktext=[f"{month} 00:00" for month in month_labels]
            # ticktext=[f"" for month in month_labels]
            showticklabels=False,
        ),
        showlegend=False

    )

    # Apply custom template
    fig = util_plotly.apply_template_to_figure(fig, template_name=template_name, paper_size=paper_size)

    return fig