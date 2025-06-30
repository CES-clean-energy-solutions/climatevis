import plotly.graph_objects as go
import pandas as pd
import numpy as np
from util import util_plotly
import matplotlib.colors as mcolors
# import plotly.colors as pc

def monthly_profiles_bands(series_list: list, template_name: str, paper_size: str, x_title="Hour of Day", y_title="Value"):
    """
    Plots daily profiles for each month for multiple series.
    Each hour in the day aggregates data from all days within that month (Min, Mean, Max).
    If gaps are detected in a series, it splits them into multiple traces to visualize the gaps.
    Additionally, a shaded area between Min and Max is added for better visual interpretation.

    Parameters:
    - series_list: list of pd.Series with DatetimeIndex to be plotted.
                   Each series should have a .name for labeling and optionally .attrs['color'] for custom colors.
    - x_title: str, label for the x-axis (default: "Hour of Day").
    - y_title: str, label for the y-axis (custom, depends on the metric being plotted).

    Returns:
    - Plotly Figure
    """

    def adjust_alpha(color: str, alpha=0.1):
        rgb = mcolors.to_rgb(color)
        rgba = rgb + (alpha,)
        rgba_str = f"rgba({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)}, {alpha})"
        return rgba_str

    fig = go.Figure()
    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    default_colors = {
        "min": "rgba(0, 123, 255, 1.0)",  # Solid Blue
        "mean": "rgba(0, 0, 0, 1.0)",     # Solid Black
        "max": "rgba(255, 0, 0, 1.0)"     # Solid Red
    }

    for series in series_list:
        if not isinstance(series.index, pd.DatetimeIndex):
            raise ValueError("All series indices must be DatetimeIndex.")

        series_label = series.name if series.name else "Unnamed Series"
        color = series.attrs.get('color', None)
        # print(color)

        # print(f"{color}, {color.strip('rgba()').split(',')}")
        # rgb_value = pc.convert_to_RGB_255(color)
        # print(f"{color}, {color.strip('rgba()').split(',')}, {rgb_value}")

        # Determine fill color based on the line color
        fill_color = adjust_alpha(color if color else default_colors["min"], alpha=0.2)

        print(fill_color)
        # Convert series to DataFrame and extract month + hour
        df = series.to_frame(name="metric")
        df["month"] = df.index.month
        df["hour"] = df.index.hour

        # Group by month and hour to compute min, mean, and max
        hourly_stats = df.groupby(["month", "hour"])["metric"].agg(["min", "mean", "max"]).reset_index()

        # Function to split data by gaps
        def split_series_by_gaps(data, time_col, value_col):
            split_data = []
            current_segment = []

            for i in range(len(data)):
                if i > 0 and (data[time_col].iloc[i] - data[time_col].iloc[i-1]) > 1:
                    split_data.append(current_segment)
                    current_segment = []
                current_segment.append((data[time_col].iloc[i], data[value_col].iloc[i]))

            if current_segment:
                split_data.append(current_segment)

            return split_data

        # Shift x-axis positions so that each month gets its own 24-hour "day"
        for i, month in enumerate(range(1, 13)):  # Loop through months 1-12
            month_data = hourly_stats[hourly_stats["month"] == month]
            shifted_x = month_data["hour"] + (i * 24)  # Offset each month's data on x-axis

            # Split Min and Max Series by gaps for shaded area
            min_splits = split_series_by_gaps(month_data, "hour", "min")
            max_splits = split_series_by_gaps(month_data, "hour", "max")

            for min_segment, max_segment in zip(min_splits, max_splits):
                min_x, min_y = zip(*min_segment)
                max_x, max_y = zip(*max_segment)
                min_x = np.array(min_x) + (i * 24)
                max_x = np.array(max_x) + (i * 24)

                # Fill area between Min and Max with dynamic transparency
                fig.add_trace(go.Scatter(
                    x=np.concatenate([min_x, max_x[::-1]]),
                    y=np.concatenate([min_y, max_y[::-1]]),
                    fill='toself',
                    mode='lines',
                    fillcolor=fill_color,
                    line=dict(color='rgba(255,255,255,0)'),  # No line
                    name=f"{month_labels[i]} Range ({series_label})",
                    showlegend=(i == 0)
                ))

            # Plot Min Series
            for segment in min_splits:
                seg_x, seg_y = zip(*segment)
                seg_x = np.array(seg_x) + (i * 24)

                fig.add_trace(go.Scatter(
                    x=seg_x,
                    y=seg_y,
                    mode='lines',
                    name=f"{month_labels[i]} Min ({series_label})",
                    line=dict(color=color if color else default_colors["min"], dash="dash"),
                    showlegend=(i == 0)
                ))

            # Plot Mean Series
            mean_splits = split_series_by_gaps(month_data, "hour", "mean")
            for segment in mean_splits:
                seg_x, seg_y = zip(*segment)
                seg_x = np.array(seg_x) + (i * 24)

                fig.add_trace(go.Scatter(
                    x=seg_x,
                    y=seg_y,
                    mode='lines',
                    name=f"{month_labels[i]} Mean ({series_label})",
                    line=dict(color=color if color else default_colors["mean"], dash="dot"),
                    showlegend=(i == 0)
                ))

            # Plot Max Series
            for segment in max_splits:
                seg_x, seg_y = zip(*segment)
                seg_x = np.array(seg_x) + (i * 24)

                fig.add_trace(go.Scatter(
                    x=seg_x,
                    y=seg_y,
                    mode='lines',
                    name=f"{month_labels[i]} Max ({series_label})",
                    line=dict(color=color if color else default_colors["max"]),
                    showlegend=(i == 0)
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

    # Update layout with legend at the top right
    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
        showlegend=False,
        legend=dict(
            x=0.99,
            y=0.99,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='black',
            borderwidth=1
        ),

        xaxis=dict(
            tickmode="array",
            tickvals=[i * 24 for i in range(12)],
            showticklabels=False,
        )
    )

    # Apply custom template
    fig = util_plotly.apply_template_to_figure(fig, template_name=template_name, paper_size=paper_size)

    return fig
