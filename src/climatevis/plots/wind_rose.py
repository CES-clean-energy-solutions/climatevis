import plotly.graph_objects as go
import pandas as pd
import numpy as np

from climatevis.util import util_plotly
from climatevis.util.validation import validate_plot_parameters

def wind_rose(windspeed: pd.Series, sector: pd.Series, template_name: str, paper_size: str):
    """
    Create a wind rose plot showing wind speed and direction frequency distribution.

    Parameters:
    - windspeed (pd.Series): Wind speed data with DatetimeIndex
    - sector (pd.Series): Wind direction sector data with DatetimeIndex
    - template_name (str): Name of the Plotly template to apply
    - paper_size (str): Paper size specification

    Returns:
    - fig (plotly.graph_objects.Figure): The generated wind rose figure
    """
    # Validate inputs using the validation utility
    validate_plot_parameters(
        [windspeed],
        template_name,
        paper_size,
        function_name="wind_rose"
    )

    # Validate sector data
    if not isinstance(sector, pd.Series):
        raise ValueError("wind_rose: sector must be a pandas Series")
    if not isinstance(sector.index, pd.DatetimeIndex):
        raise ValueError("wind_rose: sector must have DatetimeIndex")
    if not windspeed.index.equals(sector.index):
        raise ValueError("wind_rose: windspeed and sector must have the same DatetimeIndex")

    # Define wind speed bins
    bins = [0, 2, 5, 10, 15, 20]
    labels = [f'{bins[i]}-{bins[i+1]} m/s' for i in range(len(bins)-1)]

    # Assign colors from cool (blue) to hot (red)
    colors = ['blue', 'dodgerblue', 'deepskyblue', 'orange', 'red']

    # Convert wind speed values into bins
    speed_bin = pd.cut(windspeed, bins=bins, labels=labels, right=False)

    # Define sector mapping to degrees
    sector_degrees = {
        'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5,
        'E': 90, 'ESE': 112.5, 'SE': 135, 'SSE': 157.5,
        'S': 180, 'SSW': 202.5, 'SW': 225, 'WSW': 247.5,
        'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5
    }
    full_sectors = list(sector_degrees.keys())
    full_sector_angles = list(sector_degrees.values())

    # Create a DataFrame for grouping
    df = pd.DataFrame({'Sector': sector, 'Speed Bin': speed_bin})

    # Compute sector-speed frequency distribution
    sector_speed_counts = df.groupby(['Sector', 'Speed Bin'], observed=True).size().unstack(fill_value=0)
    sector_speed_counts = sector_speed_counts.reindex(columns=labels, fill_value=0)
    sector_frequencies = sector_speed_counts.div(sector_speed_counts.sum(axis=1), axis=0) * 100  # Convert to percentage

    # Create wind rose plot
    fig = go.Figure()
    for label, color in zip(labels, colors):
        r_values = sector_frequencies[label].reindex(full_sectors).fillna(0).values
        fig.add_trace(go.Barpolar(
            r=r_values,
            theta=full_sector_angles,
            name=label,
            marker_color=color,
            marker_line_color='white',
            opacity=0.7
        ))

    # Layout customization
    fig.update_layout(
        polar=dict(
            angularaxis=dict(
                direction='clockwise',
                tickmode='array',
                tickvals=full_sector_angles,
                ticktext=full_sectors,
                rotation=90
            ),
            radialaxis=dict(
                tickvals=np.arange(0, 110, 10),
                ticktext=[f'{i}%' for i in np.arange(0, 110, 10)],
                range=[0, 100],
                angle=67,
                gridcolor='lightgray',
                gridwidth=0.5
            )
        ),
        showlegend=True,
    )

    # Apply template and return figure
    # template='plotly_white'
    fig = util_plotly.apply_template_to_figure(fig, template_name=template_name, paper_size=paper_size)

    return fig