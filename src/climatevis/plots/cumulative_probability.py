import numpy as np
import pandas as pd
import plotly.graph_objects as go
from climatevis.util import util_plotly
from climatevis.util.validation import validate_plot_parameters
from typing import Union, List

def cumulative_probability(series_list: Union[List[pd.Series], pd.Series], template_name: str, paper_size: str, x_title="Value", y_title="Cumulative Probability", selected_percentile=None, y_grid_spacing: int = 10):
    """
    Plots cumulative probability curves (CDF) for multiple series using Plotly.

    Parameters:
    - series_list: list of pd.Series or a single pd.Series containing the values to plot
    - x_title: str, label for the x-axis (Sorted Values)
    - y_title: str, label for the y-axis (Cumulative Probability)
    - selected_percentile: float (0-100), percentile to highlight with a marker and annotation.
    - y_grid_spacing: int, interval for y-axis grid lines in percentage (e.g., 10, 20, 100).

    Returns:
    - Plotly Figure
    """
    # Validate inputs using the validation utility
    validated_series = validate_plot_parameters(
        series_list,
        template_name,
        paper_size,
        function_name="cumulative_probability"
    )

    # Validate y_grid_spacing parameter
    if not isinstance(y_grid_spacing, int) or y_grid_spacing <= 0 or y_grid_spacing > 100:
        raise ValueError("cumulative_probability: y_grid_spacing must be an integer between 1 and 100")

    fig = go.Figure()

    for idx, series in enumerate(validated_series):
        sorted_values = np.sort(series)  # Sort values in ascending order
        cumulative_probs = np.linspace(0, 1, len(series), endpoint=True)  # Probabilities from 0 to 1

        series_name = series.name if series.name else f"Series {idx+1}"
        fig.add_trace(go.Scatter(x=sorted_values, y=cumulative_probs, mode='lines', name=series_name))

        # Add marker if selected_percentile is specified
        if selected_percentile is not None:
            index = int(len(series) * (selected_percentile / 100))
            index = max(0, min(index, len(series) - 1))

            selected_x = sorted_values[index]
            selected_y = cumulative_probs[index]

            fig.add_trace(go.Scatter(
                x=[selected_x],
                y=[selected_y],
                mode='markers',
                marker=dict(size=8, color='red'),
                name=f"{selected_percentile}th Percentile ({series_name})"
            ))

            annotation_text = (
                f"<b>{selected_percentile}th Percentile ({series_name})</b><br>"
                f"Value: {selected_x:.2f}"
            )

            fig.add_annotation(
                x=0.1, y=0.9 - (idx * 0.05),  # Adjust y position for multiple annotations
                xref="paper", yref="paper",
                text=annotation_text,
                showarrow=False,
                bgcolor="white",
                bordercolor="black",
                font=dict(size=12)
            )

    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
        showlegend=True,
        yaxis=dict(
            tickformat=".0%",  # Display cumulative probability in percentage format
            title_standoff=5,
            tickmode="array",
            tickvals=[i / 100 for i in range(0, 101, y_grid_spacing)],  # Grid lines based on y_grid_spacing
        )
    )

    # Apply your custom plotly template
    fig = util_plotly.apply_template_to_figure(fig, template_name=template_name, paper_size=paper_size)

    return fig



def cumulative_probabilityOLD(series: pd.Series, template_name: str, paper_size: str, x_title="Value", y_title="Cumulative Probability", selected_percentile=None):
    """
    Plots a normal cumulative probability curve (CDF) using Plotly.

    Parameters:
    - series: pd.Series containing the values to plot
    - x_title: str, label for the x-axis (Sorted Values)
    - y_title: str, label for the y-axis (Cumulative Probability)
    - selected_percentile: float (0-100), percentile to highlight with a marker and annotation.

    Returns:
    - Plotly Figure
    """
    sorted_values = np.sort(series)  # Sort values in ascending order
    cumulative_probs = np.linspace(0, 1, len(series), endpoint=True)  # Probabilities from 0 to 1

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sorted_values, y=cumulative_probs, mode='lines'))  # X-axis: sorted values, Y-axis: CDF

    # Add marker if selected_percentile is specified
    if selected_percentile is not None:
        index = int(len(series) * (selected_percentile / 100))  # Convert percentile to index
        index = max(0, min(index, len(series) - 1))  # Ensure index is within range

        selected_x = sorted_values[index]  # Corrected value reference
        selected_y = cumulative_probs[index]  # Corrected cumulative probability reference

        # Add marker at the correct cumulative probability
        fig.add_trace(go.Scatter(
            x=[selected_x],
            y=[selected_y],
            mode='markers',
            marker=dict(size=8, color='red'),
            name=f"{selected_percentile}th Percentile"
        ))

        # Fixed annotation at (0.1, 0.9) in axis space (top-left)
        annotation_text = (
            f"<b>{selected_percentile}th Percentile</b><br>"
            f"Value: {selected_x:.2f}"
        )

        fig.add_annotation(
            x=0.1, y=0.9,  # Fixed position in figure space (top-left)
            xref="paper", yref="paper",  # Use figure space instead of data space
            text=annotation_text,
            showarrow=False,
            bgcolor="white",
            bordercolor="black",
            font=dict(size=12)
        )

    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
        showlegend=False,
        yaxis=dict(
            tickformat=".0%",  # Display cumulative probability in percentage format
            title_standoff=5
        )
    )

    # Apply your custom plotly template
    fig = util_plotly.apply_template_to_figure(fig, template_name=template_name, paper_size=paper_size)

    return fig