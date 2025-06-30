import pandas as pd
import plotly.express as px
from util import util_plotly

def histogram(series: pd.Series, template_name: str, paper_size: str, num_bins=None, x_title: str = "Value", y_title: str = "Count"):
    """
    Plots a histogram using Plotly and adds an annotation displaying mean, mode, and standard deviation.

    Parameters:
    - series: pd.Series containing the values to plot
    - num_bins: int, number of bins (optional, defaults to range-based heuristic)
    - x_title: str, label for the x-axis
    - y_title: str, label for the y-axis (default: "Count")

    Returns:
    - Plotly Figure
    """
    if num_bins is None:
        num_bins = int(max(series) - min(series) + 1)  # Auto binning heuristic

    # Compute statistics
    mean_value = series.mean()
    mode_value = series.mode()[0] if not series.mode().empty else None  # Handle empty mode case
    std_dev = series.std()

    # Create histogram
    fig = px.histogram(series,
                       x=series,
                       nbins=num_bins,
                       labels={x_title: x_title})

    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
        bargap=0.0
    )

    # Annotation text
    annotation_text = (
        f"<b>Statistics</b><br>"
        f"Mean: {mean_value:.2f}<br>"
        f"Mode: {mode_value:.2f}<br>"
        f"Std Dev: {std_dev:.2f}"
    )

    # Add annotation at top-left (0.1, 0.9 in figure space)
    fig.add_annotation(
        x=0.1, y=0.9,
        xref="paper", yref="paper",  # Fixed to figure space
        text=annotation_text,
        showarrow=False,
        bgcolor="white",
        bordercolor="black",
        font=dict(size=12)
    )

    # Apply custom template
    fig = util_plotly.apply_template_to_figure(fig, template_name=template_name, paper_size=paper_size)

    return fig
# fig_temp_histogram = plot_histogram(df["Dry Bulb Temperature (°C)"], False, "Dry Bulb Temperature (°C)")
# fig = histogram(df["Dry Bulb Temperature (°C)"], 20, "Dry Bulb Temperature (°C)")