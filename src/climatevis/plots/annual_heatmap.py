import plotly.express as px
import pandas as pd
import numpy as np
from climatevis.util import util_plotly

def annual_heatmap(series: pd.Series, template_name: str, paper_size: str, color_scale='Viridis', max_scale=0, scale_factor=0.6, show_legend=True):
    """
    Generates a heatmap displaying hourly values across the year.
    - X-axis: Months centered instead of day numbers
    - Y-axis: Hours of the day (1-24) (with 1 at the bottom, 24 at the top, but labeled as 0-23)
    - Color: Metric values with optional max scale for consistent comparison across charts
    - Scale factor adjusts the overall figure height to optimize layout.

    Parameters:
    - series: pd.Series with a DatetimeIndex containing the metric to be plotted.
    - template_name: str, for applying custom styling.
    - paper_size: str, format specification, now scaled with scale_factor.
    - color_scale: str, Plotly color scale name (default: 'Viridis').
    - max_scale: float, maximum value for the color scale. If 0, scale is auto-applied (default: 0).
    - scale_factor: float, factor to scale the paper size dynamically (default: 0.6).

    Returns:
    - Plotly Figure
    """
    if not isinstance(series.index, pd.DatetimeIndex):
        raise ValueError("Series index must be a DatetimeIndex.")

    # Create DataFrame with required information
    df = series.to_frame(name="metric")
    df["day_of_year"] = df.index.dayofyear
    df["hour"] = df.index.hour + 1  # Increment hour values to start at 1

    # Pivot for heatmap structure (ensure 1 is at the bottom, 24 at the top)
    heatmap_data = df.pivot_table(index="hour", columns="day_of_year", values="metric", aggfunc='mean')
    heatmap_data = heatmap_data.sort_index(ascending=True)  # Ensure correct order with 1 at bottom

    # Set color scale limits
    zmax = max_scale if max_scale > 0 else None

    # Generate heatmap
    fig = px.imshow(
        heatmap_data,
        # labels=dict(x="Month", y="Hour of Day", color=series.name or "Value"),
        labels=dict(y="Hour of Day", color=series.name or "Value"),
        aspect='auto',
        color_continuous_scale=color_scale,
        origin='lower',  # Ensure 1 is at the bottom
        zmax=zmax  # Apply max scale if specified
    )

    # Compute month positions centered within each month
    months = pd.date_range("2023-01-01", "2023-12-31", freq="MS")  # Month Start
    month_positions = {date.strftime("%b"): (date + pd.Timedelta(days=14)).dayofyear for date in months}
    month_boundaries = [date.dayofyear for date in months] + [365]  # Add year-end as last boundary

    # Update x-axis ticks to show month labels without ticks
    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=list(month_positions.values()),  # Centered positions of each month
            ticktext=list(month_positions.keys()),  # Month names
            showgrid=True,
            gridcolor='gray',  # Fainter grid lines
            gridwidth=0.8,
            zeroline=False,
            showticklabels=True,  # Ensure labels are visible
            ticks='',  # Hide actual tick marks,
            title=None  # Completely remove x-axis title

        ),
        yaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 25, 6)) + [24],  # Ensure 24 appears at the top
            ticktext=[str(h - 1) for h in list(range(1, 25, 6)) + [24]],  # Decrement labels to show 0-23
            showgrid=True,
            gridcolor='lightgrey',
            range=[1, 24]  # Set range from 1 to 24
        ),
        shapes=[
            dict(
                type="line",
                x0=day - 0.5, x1=day - 0.5,  # Shift lines by -0.5 to align with start of day
                y0=0.5, y1=24.5,  # Extend lines slightly to touch the axis
                line=dict(color="gray", width=1)
            ) for day in month_boundaries
        ],
        # title=f"Annual Heatmap of {series.name or 'Metric'}",
        # xaxis_title="Month",
        yaxis_title="Hour of Day",
        # coloraxis_colorbar=dict(title=series.name or "Value", visible=show_legend)
        coloraxis=dict(colorbar=dict(title=series.name or "Value")) if show_legend else dict(showscale=False)

        # coloraxis_colorbar=dict(title=series.name or "Value")
    )

    # Apply template with paper size
    fig = util_plotly.apply_template_to_figure(fig, template_name=template_name, paper_size=paper_size)

    # Adjust the figure size based on scale factor
    fig.update_layout(height=fig.layout.height * scale_factor if fig.layout.height else 800 * scale_factor)

    return fig
