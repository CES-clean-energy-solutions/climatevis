import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.colors as pc
from climatevis.util import util_plotly
from climatevis.util.validation import validate_plot_parameters

def exceedance(series: pd.Series, template_name: str, paper_size: str, x_title="Exceedance Probability", y_title="", selected_percentile=None):
    """
    Plots an exceedance probability curve using Plotly.

    Parameters:
    - series: pd.Series containing the values to plot
    - template_name: str, name of the Plotly template to apply
    - paper_size: str, paper size specification
    - x_title: str, label for the x-axis (Exceedance Probability)
    - y_title: str, label for the y-axis (Sorted Values)
    - selected_percentile: float (0-100), percentile to highlight with a marker and annotation.

    Returns:
    - Plotly Figure
    """
    # Validate inputs using the validation utility
    validate_plot_parameters(
        series,
        template_name,
        paper_size,
        function_name="exceedance"
    )

    sorted_values = np.sort(series)[::-1]  # Sort values in descending order
    exceedance_probs = np.linspace(1, 0, len(series), endpoint=False)  # Probabilities from 1 to 0

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=exceedance_probs, y=sorted_values, mode='lines'))  # X-axis: 1 (left) → 0 (right)

    # Add marker if selected_percentile is specified
    if selected_percentile is not None:
        # Compute the correct index in the exceedance probabilities array
        index = int(len(series) * (1 - (selected_percentile / 100)))
        index = max(0, min(index, len(series) - 1))  # Ensure index is within range

        selected_x = exceedance_probs[index]  # Corrected exceedance probability reference
        selected_y = sorted_values[index]  # Corrected sorted value reference

        # Add marker at the correct exceedance probability
        fig.add_trace(go.Scatter(
            x=[selected_x],
            y=[selected_y],
            mode='markers',
            marker=dict(size=8, color='red'),
            name=f"{selected_percentile}th Percentile"
        ))

        if 0:
            # Fixed annotation at (0.1, 0.9) in axis space (top-left)
            annotation_text = (
                f"<b>{selected_percentile}th Percentile</b><br>"
                f"Value: {selected_y:.2f}"
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
        xaxis=dict(
            autorange="reversed",  # Ensure 1 (100%) is on the left
            tickformat=".0%",  # Display exceedance probability in percentage format
            title_standoff=5
        )
    )

    # Apply your custom plotly template
    fig = util_plotly.apply_template_to_figure(fig, template_name=template_name, paper_size=paper_size)

    return fig



import plotly.graph_objects as go
import numpy as np
import plotly.colors as pc

def add_exceedance_bands(fig, data, bands, colorscale="Viridis"):
    """
    Adds exceedance bands to a Plotly figure with automatically generated colors.
    Does NOT return a summary DataFrame—use `calculate_exceedance_summary()` separately.

    Parameters:
        fig (plotly.graph_objects.Figure): The existing Plotly figure.
        data (list or numpy array): The dataset (Y-values) to calculate exceedances.
        bands (list of tuples): List of (from_percentage, to_percentage) defining exceedance bands.
        colorscale (str, optional): The Plotly color scale to use for automatic band colors (default: "Viridis").

    Returns:
        plotly.graph_objects.Figure: Updated figure with exceedance bands.
    """
    if not bands:
        raise ValueError("Bands list cannot be empty.")

    if not isinstance(fig, go.Figure):
        raise TypeError("fig must be a plotly.graph_objects.Figure instance.")

    data_sorted = sorted(data, reverse=True)  # Sort descending (high values first)
    total_points = len(data_sorted)

    # Get x-axis range from first trace in figure
    if fig.data and len(fig.data) > 0:
        x_values = fig.data[0].x
        x_range_min = min(x_values)
        x_range_max = max(x_values)
    else:
        x_range_min, x_range_max = 0, 1  # Default fallback

    # Generate colors from the selected colorscale
    colors = pc.get_colorscale(colorscale)
    colors_rgb = [pc.hex_to_rgb(color[1]) for color in colors]  # Convert hex colors to RGB tuples

    num_bands = len(bands)
    band_colors = [pc.find_intermediate_color(colors_rgb[0], colors_rgb[-1], i / max(num_bands - 1, 1)) for i in range(num_bands)]

    for i, (from_perc, to_perc) in enumerate(bands):
        from_idx = int((1 - from_perc) * total_points)  # Inverted
        to_idx = int((1 - to_perc) * total_points)      # Inverted

        if from_idx >= total_points:
            from_idx = total_points - 1
        if to_idx >= total_points:
            to_idx = total_points - 1

        # Get actual Y-value range from sorted data
        from_value = data_sorted[to_idx]
        to_value = data_sorted[from_idx]

        # Convert RGB color to rgba with transparency
        band_color = band_colors[i]
        band_color_rgba = f"rgba({band_color[0]},{band_color[1]},{band_color[2]},0.2)"  # 20% opacity

        # Add transparent shaded box to highlight the band
        fig.add_shape(
            type="rect",
            x0=x_range_min,
            x1=x_range_max,
            y0=from_value,
            y1=to_value,
            fillcolor=band_color_rgba,
            line=dict(width=0),
            layer="below",
        )

        # Add annotation for exceedance percentage
        fig.add_annotation(
            x=(x_range_max - x_range_min)/2,
            y=(from_value + to_value) / 2,
            text=f"{from_perc*100:.1f}% - {to_perc*100:.1f}%",
            showarrow=False,
            # bgcolor=f"rgba({band_color[0]},{band_color[1]},{band_color[2]},0.5)",  # Slightly more visible
            # bordercolor="black",
        )

    return fig


def calculate_exceedance_summary(data, bands):
    """
    Calculates exceedance statistics for given bands.

    Parameters:
        data (list or numpy array): The dataset (Y-values) to analyze.
        bands (list of tuples): List of (from_percentage, to_percentage) defining exceedance bands.

    Returns:
        pandas.DataFrame: Summary table with exceedance band statistics (min, max, mean).
    """
    if not bands:
        raise ValueError("Bands list cannot be empty.")

    data_sorted = sorted(data, reverse=True)  # Sort descending (high values first)
    total_points = len(data_sorted)

    summary_data = []

    for from_perc, to_perc in bands:
        from_idx = int((1 - from_perc) * total_points)  # Inverted
        to_idx = int((1 - to_perc) * total_points)      # Inverted

        if from_idx >= total_points:
            from_idx = total_points - 1
        if to_idx >= total_points:
            to_idx = total_points - 1

        # Get values in the exceedance range
        band_values = data_sorted[to_idx:from_idx+1]

        # Compute statistics
        count_in_band = len(band_values)
        percent_in_band = (count_in_band / total_points) * 100
        min_value = min(band_values) if band_values else None
        max_value = max(band_values) if band_values else None
        mean_value = sum(band_values) / count_in_band if count_in_band > 0 else None

        summary_data.append({
            "From %": from_perc * 100,
            "To %": to_perc * 100,
            "Count": count_in_band,
            "Percentage": percent_in_band,
            "Min": min_value,
            "Mean": mean_value,
            "Max": max_value,
        })

    return pd.DataFrame(summary_data)


def calculate_value_range_summary(data, value_bands):
    """
    Calculates statistics for given value-based bands, including open-ended bands (> or <).

    Parameters:
        data (list or numpy array): The dataset (Y-values) to analyze.
        value_bands (list of tuples): List of (min_value, max_value) or ("> value", "< value") for open-ended bands.

    Returns:
        pandas.DataFrame: Summary table with statistics (min, max, mean, count, percentage).
    """
    if not value_bands:
        raise ValueError("Value bands list cannot be empty.")

    total_points = len(data)

    # Handle case where dataset is empty
    if total_points == 0:
        return pd.DataFrame(columns=["Band", "Count", "Percentage", "Min", "Max", "Mean"])

    data_min, data_max = min(data), max(data)  # Find data range
    summary_data = []

    for band in value_bands:
        # Detect open-ended bands
        if isinstance(band, tuple) and len(band) == 2:
            min_val, max_val = band
            is_upper_band = max_val is None  # e.g., (50, None) means y > 50
            is_lower_band = min_val is None  # e.g., (None, 10) means y < 10
        else:
            raise ValueError("Bands must be tuples (min_value, max_value) or (None, value) for open-ended bands.")

        # Select data based on band conditions
        if is_upper_band:
            band_values = [x for x in data if x >= min_val]
            band_label = f"> {min_val}"
        elif is_lower_band:
            band_values = [x for x in data if x < max_val]
            band_label = f"< {max_val}"
        else:
            band_values = [x for x in data if min_val <= x < max_val]
            band_label = f"{min_val} - {max_val}"

        count_in_band = len(band_values)
        percent_in_band = (count_in_band / total_points) * 100 if total_points > 0 else 0
        min_value = min(band_values) if band_values else None
        max_value = max(band_values) if band_values else None
        mean_value = sum(band_values) / count_in_band if count_in_band > 0 else None

        summary_data.append({
            "Band": band_label,
            "Count": count_in_band,
            "Percentage": percent_in_band,
            "Min": min_value,
            "Max": max_value,
            "Mean": mean_value
        })

    return pd.DataFrame(summary_data).fillna("-")





def add_value_range_bands(fig, data, value_bands, colorscale="Viridis"):
    """
    Adds vertical bands to a Plotly figure based on specific value ranges,
    including open-ended bands (> or <). Skips plotting bands with no data.

    Parameters:
        fig (plotly.graph_objects.Figure): The existing Plotly figure.
        data (list or numpy array): The dataset (Y-values) to calculate exceedances.
        value_bands (list of tuples): List of (min_value, max_value) or ("> value", "< value") for open-ended bands.
        colorscale (str, optional): The Plotly color scale to use for automatic band colors (default: "Viridis").

    Returns:
        plotly.graph_objects.Figure: Updated figure with vertical exceedance bands.
    """
    if not value_bands:
        raise ValueError("Value bands list cannot be empty.")

    if not isinstance(fig, go.Figure):
        raise TypeError("fig must be a plotly.graph_objects.Figure instance.")

    # Get x-axis range from first trace in figure
    if fig.data and len(fig.data) > 0:
        x_values = fig.data[0].x
        x_range_min = min(x_values)
        x_range_max = max(x_values)
    else:
        x_range_min, x_range_max = 0, 1  # Default fallback

    data_min, data_max = min(data), max(data)  # Get actual data range

    # Generate colors from the selected colorscale
    colors = pc.get_colorscale(colorscale)
    colors_rgb = [pc.hex_to_rgb(color[1]) for color in colors]  # Convert hex colors to RGB tuples

    num_bands = len(value_bands)
    band_colors = [pc.find_intermediate_color(colors_rgb[0], colors_rgb[-1], i / max(num_bands - 1, 1)) for i in range(num_bands)]

    for i, band in enumerate(value_bands):
        # Detect open-ended bands
        if isinstance(band, tuple) and len(band) == 2:
            min_val, max_val = band
            is_upper_band = max_val is None  # e.g., (50, None) means y > 50
            is_lower_band = min_val is None  # e.g., (None, 10) means y < 10
        else:
            raise ValueError("Bands must be tuples (min_value, max_value) or (None, value) for open-ended bands.")

        # Select data points inside this band
        if is_upper_band:
            band_values = [x for x in data if x >= min_val]
            y0, y1 = min_val, data_max  # Top band snaps to data_max
        elif is_lower_band:
            band_values = [x for x in data if x < max_val]
            y0, y1 = data_min, max_val  # Bottom band snaps to data_min
        else:
            band_values = [x for x in data if min_val <= x < max_val]
            y0, y1 = min_val, max_val  # Normal case

        # **Skip plotting if the band has no data**
        if not band_values:
            continue  # Skip this band

        # Convert RGB color to rgba with transparency
        band_color = band_colors[i]
        band_color_rgba = f"rgba({band_color[0]},{band_color[1]},{band_color[2]},0.2)"  # 20% opacity

        # Add vertical shaded box to highlight the band
        fig.add_shape(
            type="rect",
            x0=x_range_min,
            x1=x_range_max,
            y0=y0,
            y1=y1,
            fillcolor=band_color_rgba,
            line=dict(width=0),
            layer="below",
        )

        # Add annotation for the band
        fig.add_annotation(
            x=(x_range_max-x_range_min)/2,
            y=(y0 + y1) / 2,
            text=f"{y0} to {y1}" if not is_upper_band and not is_lower_band else (f"> {y0}" if is_upper_band else f"< {y1}"),
            showarrow=False,
            # bgcolor=f"rgba({band_color[0]},{band_color[1]},{band_color[2]},0.5)",  # Slightly more visible
            # bordercolor="black",
        )

    return fig




def add_value_range_bands_OLD2(fig, data, value_bands, colorscale="Viridis"):
    """
    Adds vertical bands to a Plotly figure based on specific value ranges,
    including open-ended bands (> or <).

    Parameters:
        fig (plotly.graph_objects.Figure): The existing Plotly figure.
        data (list or numpy array): The dataset (Y-values) to calculate exceedances.
        value_bands (list of tuples): List of (min_value, max_value) or ("> value", "< value") for open-ended bands.
        colorscale (str, optional): The Plotly color scale to use for automatic band colors (default: "Viridis").

    Returns:
        plotly.graph_objects.Figure: Updated figure with vertical exceedance bands.
    """
    if not value_bands:
        raise ValueError("Value bands list cannot be empty.")

    if not isinstance(fig, go.Figure):
        raise TypeError("fig must be a plotly.graph_objects.Figure instance.")

    # Get x-axis range from first trace in figure
    if fig.data and len(fig.data) > 0:
        x_values = fig.data[0].x
        x_range_min = min(x_values)
        x_range_max = max(x_values)
    else:
        x_range_min, x_range_max = 0, 1  # Default fallback

    data_min, data_max = min(data), max(data)  # Get actual data range

    # Generate colors from the selected colorscale
    colors = pc.get_colorscale(colorscale)
    colors_rgb = [pc.hex_to_rgb(color[1]) for color in colors]  # Convert hex colors to RGB tuples

    num_bands = len(value_bands)
    band_colors = [pc.find_intermediate_color(colors_rgb[0], colors_rgb[-1], i / max(num_bands - 1, 1)) for i in range(num_bands)]

    for i, band in enumerate(value_bands):
        # Detect open-ended bands
        if isinstance(band, tuple) and len(band) == 2:
            min_val, max_val = band
            is_upper_band = max_val is None  # e.g., (50, None) means y > 50
            is_lower_band = min_val is None  # e.g., (None, 10) means y < 10
        else:
            raise ValueError("Bands must be tuples (min_value, max_value) or (None, value) for open-ended bands.")

        # Adjust y0, y1 for open-ended bands
        if is_upper_band:
            y0, y1 = min_val, data_max  # Top band snaps to data_max
        elif is_lower_band:
            y0, y1 = data_min, max_val  # Bottom band snaps to data_min
        else:
            y0, y1 = min_val, max_val  # Normal case

        if not band_values:
            continue # Skip empty bands

        # Convert RGB color to rgba with transparency
        band_color = band_colors[i]
        band_color_rgba = f"rgba({band_color[0]},{band_color[1]},{band_color[2]},0.2)"  # 20% opacity

        # Add vertical shaded box to highlight the band
        fig.add_shape(
            type="rect",
            x0=x_range_min,
            x1=x_range_max,
            y0=y0,
            y1=y1,
            fillcolor=band_color_rgba,
            line=dict(width=0),
            layer="below",
        )

        # Add annotation for the band
        fig.add_annotation(
            x=(x_range_max-x_range_min)/2,
            y=(y0 + y1) / 2,
            text=f"{y0} to {y1}" if not is_upper_band and not is_lower_band else (f"> {y0}" if is_upper_band else f"< {y1}"),
            showarrow=False,
            # bgcolor=f"rgba({band_color[0]},{band_color[1]},{band_color[2]},0.5)",  # Slightly more visible
            # bordercolor="black",
        )

    return fig
