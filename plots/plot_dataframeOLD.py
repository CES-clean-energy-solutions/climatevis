import plotly.graph_objects as go
import pandas as pd
from util import util_general
from util import util_plotly

def plot_dataframe(df: pd.DataFrame, template_name='base', paper_size='A5_LANDSCAPE'):
    """
    Takes a df with any number of columns. Columns MUST have "Column Name (units)" format as the name. If there are 2 units detected, there will be a secondary y-axis. Maximum 2.
    """
    unit_map = {col: util_general.get_units(col) for col in df.columns}

    # Get unique units in dataset
    unique_units = set(unit_map.values())

    # Ensure 1 or 2 unique units exist
    if len(unique_units) > 2:
        raise ValueError(f"More than two distinct units detected: {unique_units}")
    if len(unique_units) == 0:
        raise ValueError("No valid units found in column names. Ensure format: 'Column Name (Unit)'")

    fig = go.Figure()

    # Assign traces based on unit type
    first_unit = list(unique_units)[0]
    second_unit = list(unique_units)[1] if len(unique_units) == 2 else None

    for col in df.columns:
        unit = unit_map[col]
        trace = go.Scatter(
            x=df.index,
            y=df[col],
            mode='lines',
            name=col,
            yaxis="y2" if unit == second_unit else "y1"
        )
        fig.add_trace(trace)

    layout = {
        "xaxis_title": "Index",
        "yaxis": {
            "title": first_unit,
            "side": "left",
            "showgrid": True
        },
    }

    if second_unit:
        layout["yaxis2"] = {
            "title": second_unit,
            "overlaying": "y",
            "side": "right",
            "showgrid": False
        }

    fig.update_layout(layout)

    fig = util_plotly.apply_template_to_figure(fig, template_name=template_name, paper_size=paper_size)

    return fig