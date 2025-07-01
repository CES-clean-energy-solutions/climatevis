"""
Marimo UI components for interactive weather data selection and plotting.
"""

try:
    from .weather import weather_selection
    from .templates import (
        create_template_dropdown,
        create_paper_size_dropdown,
        get_template_options,
        get_paper_size_options
    )
    __all__ = [
        'weather_selection',
        'create_template_dropdown',
        'create_paper_size_dropdown',
        'get_template_options',
        'get_paper_size_options'
    ]
except ImportError:
    # Marimo not available, graceful degradation
    __all__ = []