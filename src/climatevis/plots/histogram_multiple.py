import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from climatevis.util import util_plotly
from climatevis.util.validation import validate_plot_parameters

def multiple_histograms(series_list, template_name: str, paper_size: str, num_bins=None, x_title: str = "Value", y_title: str = "Count"):
    """
    Plots multiple histograms on the same figure using Plotly, with annotations showing mean, mode, and std deviation.

    Parameters:
    - series_list: List of pd.Series containing the values to plot
    - template_name: str, name of the Plotly template to use
    - paper_size: str, size of the paper (used for template styling)
    - num_bins: int, number of bins (optional, defaults to range-based heuristic)
    - x_title: str, label for the x-axis
    - y_title: str, label for the y-axis (default: "Count")

    Returns:
    - Plotly Figure
    """
    # Validate inputs using the validation utility
    validated_series = validate_plot_parameters(
        series_list,
        template_name,
        paper_size,
        function_name="multiple_histograms"
    )

    fig = go.Figure()

    # Iterate over each series to add as a histogram
    for i, series in enumerate(validated_series):
        # Auto binning heuristic if not specified
        if num_bins is None:
            num_bins = int(series.max() - series.min() + 1)

        # Compute statistics
        mean_value = series.mean()
        mode_series = series.mode()
        mode_value = mode_series.iloc[0] if len(mode_series) > 0 else None
        std_dev = series.std()

        # Add histogram trace
        fig.add_trace(go.Histogram(
            x=series,
            name=series.name,
            nbinsx=num_bins,
            opacity=0.75,
            histnorm='probability',  # Normalized to probability
            marker=dict(line=dict(width=1))
        ))

        # Annotation text
        annotation_text = (
            f"<b>{series.name} Statistics</b><br>"
            f"Mean: {mean_value:.2f}<br>"
            f"Mode: {mode_value:.2f}<br>"
            f"Std Dev: {std_dev:.2f}"
        )

        # Add annotation to the plot (top-right corner)
        fig.add_annotation(
            x=0.95, y=0.95 - 0.1 * i,  # Adjust y position for each series
            xref="paper", yref="paper",
            text=annotation_text,
            showarrow=False,
            bgcolor="white",
            bordercolor="black",
            font=dict(size=12)
        )

    # Update layout for better visualization
    fig.update_layout(
        # title="Multiple Histograms with Statistics",
        xaxis_title=x_title,
        yaxis_title=y_title,
        barmode='overlay',
        template=template_name,
        legend=dict(title="Series", orientation="h", x=0.5, xanchor='center'),
    )

    fig = util_plotly.apply_template_to_figure(fig, template_name=template_name, paper_size=paper_size)

    return fig
