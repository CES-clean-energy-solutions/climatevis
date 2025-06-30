"""
Marimo UI components for interactive weather data selection.
"""

try:
    from .weather import weather_selection
    __all__ = ['weather_selection']
except ImportError:
    # Marimo not available, graceful degradation
    __all__ = []