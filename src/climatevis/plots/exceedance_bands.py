import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.colors as pc
from climatevis.util import util_plotly

def exceedance_bands(series_list: list, template_name: str, paper_size: str, x_title="Exceedance Probability", y_title="", selected_percentile=None):
    """
    Plots exceedance probability curves for multiple series using Plotly.

    Parameters:
    - series_list: list of pd.Series objects to plot. Each series should have a name for labeling.
    - x_title: str, label for the x-axis (Exceedance Probability)
    - y_title: str, label for the y-axis (Sorted Values)
    - selected_percentile: float (0-100), percentile to highlight with a marker and annotation.

    Returns:
    - Plotly Figure
    """
    fig = go.Figure()

    for series in series_list:
        series_label = series.name if series.name else "Unnamed Series"
        print(series.name)
        sorted_values = np.sort(series)[::-1]  # Sort values in descending order
        exceedance_probs = np.linspace(1, 0, len(series), endpoint=False)  # Probabilities from 1 to 0

        fig.add_trace(go.Scatter(
            x=exceedance_probs,
            y=sorted_values,
            mode='lines',
            name=series_label
        ))

        # Add marker if selected_percentile is specified
        if selected_percentile is not None:
            index = int(len(series) * (1 - (selected_percentile / 100)))
            index = max(0, min(index, len(series) - 1))
            selected_x = exceedance_probs[index]
            selected_y = sorted_values[index]

            fig.add_trace(go.Scatter(
                x=[selected_x],
                y=[selected_y],
                mode='markers',
                marker=dict(size=8, color='red'),
                name=f"{selected_percentile}th Percentile ({series_label})"
            ))

    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
        showlegend=True,
        legend=dict(
            x=0.99,
            y=0.99,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(255, 255, 255, 0.8)',  # Semi-transparent background
            bordercolor='black',
            borderwidth=1
        ),
        xaxis=dict(
            autorange="reversed",
            tickformat=".0%",
            title_standoff=5
        )
    )

    # Apply your custom plotly template
    fig = util_plotly.apply_template_to_figure(fig, template_name=template_name, paper_size=paper_size)

    return fig