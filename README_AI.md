# README_AI.md - ClimateVis

### 1. Purpose
ClimateVis is a Python library for creating professional weather and climate data visualizations using Plotly. It provides specialized plotting functions, marimo UI components, and template management for meteorological applications.

### 2. Core Concepts
- **Templates**: YAML-defined Plotly styling configurations (base, base_autosize, test)
- **Paper Sizes**: Predefined pixel dimensions (A0-A6, landscape/portrait)
- **Series Attributes**: Metadata stored in `series.attrs` (units, colors) for automatic labeling
- **Dual Y-axes**: Multi-series plots with different units use separate axes
- **DatetimeIndex**: All time series functions require pandas Series with DatetimeIndex
- **Marimo Integration**: Optional UI components for interactive applications

### 3. Entry Points (API Summary)

```python
# Core plotting functions
def plot_series(series_list, template_name='base-auto', paper_size='A4_LANDSCAPE', 
                y1_axis_title="", mode="line", show_days=False) -> Figure:
    """Plot time series data with customizable display options."""

def plot_timeseries_df(df, **kwargs) -> Figure:
    """Wrapper for plot_series that accepts DataFrame columns."""

def annual_profile_daily(series, template_name, paper_size, 
                        show=["max", "min", "mean"]) -> Figure:
    """Plot daily statistics for each day of year."""

def monthly_profiles(series, template_name, paper_size) -> Figure:
    """Create monthly profile plots showing hourly patterns."""

def annual_heatmap(series, template_name, paper_size, 
                  color_scale='Viridis') -> Figure:
    """Generate heatmap of hourly values across the year."""

def histogram(series, template_name, paper_size, num_bins=None) -> Figure:
    """Create histogram with statistical annotations."""

def exceedance(series, template_name, paper_size, 
              selected_percentile=None) -> Figure:
    """Plot exceedance probability curve."""

def wind_rose(windspeed, sector, template_name, paper_size) -> Figure:
    """Create wind rose diagram."""

# Marimo UI components (optional)
def create_template_dropdown(value="base", label="Chart Template") -> ui.dropdown:
    """Create dropdown with available templates."""

def weather_selection() -> ui.dropdown:
    """Create dropdown for weather file selection."""

# Template management
def get_available_templates() -> list[str]:
    """Get list of all available template names."""

def load_all_builtin_templates() -> dict:
    """Load and register all built-in templates."""
```

### 4. Minimal Usage Examples

```python
import climatevis
import pandas as pd
import numpy as np

# Create sample data
dates = pd.date_range('2023-01-01', '2023-12-31', freq='H')
temp = pd.Series(20 + 10*np.sin(np.arange(len(dates))/24), 
                 index=dates, name='Temperature')
temp.attrs['unit'] = '°C'

# Basic time series plot
fig = climatevis.plot_series([temp], template_name='base', 
                           paper_size='A4_LANDSCAPE')
fig.show()

# Multiple series with different units
wind = pd.Series(5 + 2*np.random.randn(len(dates)), 
                 index=dates, name='Wind Speed')
wind.attrs['unit'] = 'm/s'
fig = climatevis.plot_series([temp, wind], y1_axis_title='Weather Data')

# Annual heatmap
fig = climatevis.annual_heatmap(temp, 'base', 'A4_LANDSCAPE')
```

**Dependencies**: plotly>=5.0, pandas>=1.3, numpy>=1.20, pyyaml>=6.0, marimo (optional)