"""
ClimateVis - Professional Weather Data Visualization Library

A comprehensive Python package for creating professional weather and climate
data visualizations using Plotly.
"""

__version__ = "0.1.0"
__author__ = "Benjamin Marcus Jones"

# Import utility functions first (needed for template loading)
from .util import util_plotly

# Auto-load all built-in templates upon import
try:
    util_plotly.load_all_builtin_templates()
except Exception as e:
    import logging
    logging.warning(f"Failed to auto-load some templates: {e}")

# Import key functions at package level for easy access
from .plots import (
    wind_rose,
    exceedance,
    exceedance_bands,
    annual_heatmap,
    annual_profile_daily,
    annual_profile_multiple,
    plot_series,
    plot_timeseries_df,
    plot_rotated_box,
    histogram,
    cumulative_probability,
    monthly_profiles,
    monthly_profiles_bands
)

# Import components (with optional marimo dependency)
try:
    from .components import (
        weather_selection,
        create_template_dropdown,
        create_paper_size_dropdown,
        get_template_options,
        get_paper_size_options
    )
    _HAS_MARIMO = True
except ImportError:
    _HAS_MARIMO = False

# Import template management functions
from .util.util_plotly import (
    get_available_templates,
    get_builtin_template_names,
    get_loaded_template_names,
    load_all_builtin_templates
)

__all__ = [
    'wind_rose',
    'exceedance',
    'exceedance_bands',
    'annual_heatmap',
    'annual_profile_daily',
    'annual_profile_multiple',
    'plot_series',
    'plot_timeseries_df',
    'plot_rotated_box',
    'histogram',
    'cumulative_probability',
    'monthly_profiles',
    'monthly_profiles_bands',
    'util_plotly',
    'get_available_templates',
    'get_builtin_template_names',
    'get_loaded_template_names',
    'load_all_builtin_templates'
]

if _HAS_MARIMO:
    __all__.extend([
        'weather_selection',
        'create_template_dropdown',
        'create_paper_size_dropdown',
        'get_template_options',
        'get_paper_size_options'
    ])