# ClimateVis

**Professional Weather Data Visualization Library**

ClimateVis is a comprehensive Python package for creating professional weather and climate data visualizations using Plotly. It provides specialized plotting functions, marimo UI components, and template management utilities for meteorological and atmospheric science applications.

[![Development Status](https://img.shields.io/badge/Development%20Status-4%20--%20Beta-yellow.svg)](https://pypi.org/classifiers/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

## Installation

```bash
pip install climatevis
```

For marimo integration (optional):
```bash
pip install "climatevis[marimo]"
```

For development:
```bash
pip install "climatevis[dev]"
```

## Quick Start

```python
import climatevis
import pandas as pd

# Create sample time series data
dates = pd.date_range('2023-01-01', '2023-12-31', freq='H')
temperature = pd.Series(data=20 + 10*np.sin(np.arange(len(dates))/24), index=dates, name='Temperature')
temperature.attrs['unit'] = '°C'

# Create a time series plot
fig = climatevis.plot_series(
    series_list=[temperature],
    template_name='base',
    paper_size='A4_LANDSCAPE',
    y1_axis_title='Temperature'
)
fig.show()
```

## Core Plotting Functions

### `plot_series`

**Signature:**
```python
plot_series(series_list, template_name='base-auto', paper_size='A4_LANDSCAPE', y1_axis_title="", mode="line", show_days=False)
```

**Description:**
Plots time series data using Plotly with customizable display options. Supports multiple series with different units on dual y-axes.

**Parameters:**
- `series_list` (list of pd.Series): List of Pandas Series with DatetimeIndex
- `template_name` (str): Name of the Plotly template to apply (default: 'base-auto')
- `paper_size` (str): Paper size specification (default: 'A4_LANDSCAPE')
- `y1_axis_title` (str): Title for the primary y-axis
- `mode` (str): Plot type - 'line', 'area', 'bar', 'markers' (default: 'line')
- `show_days` (bool): Add vertical grid lines at daily intervals (default: False)

**Returns:**
- `plotly.graph_objects.Figure`: The generated Plotly figure

**Usage:**
```python
# Single series
fig = climatevis.plot_series([temperature_series], template_name='base', paper_size='A4_LANDSCAPE')

# Multiple series with different units
wind_series.attrs['unit'] = 'm/s'
temp_series.attrs['unit'] = '°C'
fig = climatevis.plot_series([wind_series, temp_series], y1_axis_title='Weather Data')
```

---

### `plot_timeseries_df`

**Signature:**
```python
plot_timeseries_df(df, **kwargs)
```

**Description:**
Wrapper function for `plot_series` that accepts a DataFrame and passes its columns as Series.

**Parameters:**
- `df` (pd.DataFrame): DataFrame with DatetimeIndex and one or more columns
- `**kwargs`: Additional keyword arguments passed to `plot_series`

**Returns:**
- `plotly.graph_objects.Figure`: The generated Plotly figure

**Usage:**
```python
# Plot all columns in a DataFrame
df = pd.DataFrame({'Temperature': temp_data, 'Humidity': humidity_data}, index=dates)
fig = climatevis.plot_timeseries_df(df, template_name='base', y1_axis_title='Weather')
```

---

### `annual_profile_daily`

**Signature:**
```python
annual_profile_daily(series, template_name, paper_size, x_title="Day of Year", y_title="Value", show=["max", "min", "mean"])
```

**Description:**
Plots an annual profile showing daily statistics (min, mean, max) for each day of the year with month labels.

**Parameters:**
- `series` (pd.Series): Series with DatetimeIndex containing the metric to plot
- `template_name` (str): Template name for styling
- `paper_size` (str): Paper size specification
- `x_title` (str): X-axis label (default: "Day of Year")
- `y_title` (str): Y-axis label (default: "Value")
- `show` (list): Statistics to display from ['max', 'min', 'mean'] (default: all)

**Returns:**
- `plotly.graph_objects.Figure`: The generated Plotly figure

**Usage:**
```python
fig = climatevis.annual_profile_daily(
    temperature_series,
    template_name='base',
    paper_size='A4_LANDSCAPE',
    y_title='Temperature (°C)',
    show=['max', 'mean']
)
```

---

### `annual_profile_multiple`

**Signature:**
```python
annual_profile_multiple(series_list, template_name, paper_size, x_title="Day of Year", y_title="Value", show='max')
```

**Description:**
Plots annual profiles for multiple time series showing a single selected statistic.

**Parameters:**
- `series_list` (list): List of pd.Series with DatetimeIndex
- `template_name` (str): Template name for styling
- `paper_size` (str): Paper size specification
- `x_title` (str): X-axis label (default: "Day of Year")
- `y_title` (str): Y-axis label (default: "Value")
- `show` (str): Statistic to display - 'max', 'min', or 'mean' (default: 'max')

**Returns:**
- `plotly.graph_objects.Figure`: The generated Plotly figure

**Usage:**
```python
fig = climatevis.annual_profile_multiple(
    [temp_2022, temp_2023],
    template_name='base',
    paper_size='A4_LANDSCAPE',
    y_title='Temperature (°C)',
    show='mean'
)
```

---

### `monthly_profiles`

**Signature:**
```python
monthly_profiles(series, template_name, paper_size, x_title="Hour of Day", y_title="Value")
```

**Description:**
Creates monthly profile plots showing hourly patterns for each month of the year.

**Parameters:**
- `series` (pd.Series): Series with DatetimeIndex
- `template_name` (str): Template name for styling
- `paper_size` (str): Paper size specification
- `x_title` (str): X-axis label (default: "Hour of Day")
- `y_title` (str): Y-axis label (default: "Value")

**Returns:**
- `plotly.graph_objects.Figure`: The generated Plotly figure

**Usage:**
```python
fig = climatevis.monthly_profiles(
    temperature_series,
    template_name='base',
    paper_size='A4_LANDSCAPE',
    y_title='Temperature (°C)'
)
```

---

### `monthly_profiles_bands`

**Signature:**
```python
monthly_profiles_bands(series_list, template_name, paper_size, x_title="Hour of Day", y_title="Value")
```

**Description:**
Creates monthly profile plots with confidence bands showing variation across multiple series.

**Parameters:**
- `series_list` (list): List of pd.Series with DatetimeIndex
- `template_name` (str): Template name for styling
- `paper_size` (str): Paper size specification
- `x_title` (str): X-axis label (default: "Hour of Day")
- `y_title` (str): Y-axis label (default: "Value")

**Returns:**
- `plotly.graph_objects.Figure`: The generated Plotly figure

**Usage:**
```python
fig = climatevis.monthly_profiles_bands(
    [temp_2022, temp_2023, temp_2024],
    template_name='base',
    paper_size='A4_LANDSCAPE',
    y_title='Temperature (°C)'
)
```

---

### `annual_heatmap`

**Signature:**
```python
annual_heatmap(series, template_name, paper_size, color_scale='Viridis', max_scale=0, scale_factor=0.6, show_legend=True)
```

**Description:**
Generates a heatmap displaying hourly values across the year with months on x-axis and hours on y-axis.

**Parameters:**
- `series` (pd.Series): Series with DatetimeIndex
- `template_name` (str): Template name for styling
- `paper_size` (str): Paper size specification
- `color_scale` (str): Plotly color scale name (default: 'Viridis')
- `max_scale` (float): Maximum value for color scale; 0 for auto-scale (default: 0)
- `scale_factor` (float): Factor to scale figure height (default: 0.6)
- `show_legend` (bool): Whether to show color legend (default: True)

**Returns:**
- `plotly.graph_objects.Figure`: The generated Plotly figure

**Usage:**
```python
fig = climatevis.annual_heatmap(
    temperature_series,
    template_name='base',
    paper_size='A4_LANDSCAPE',
    color_scale='RdYlBu_r',
    max_scale=40
)
```

---

### `histogram`

**Signature:**
```python
histogram(series, template_name, paper_size, num_bins=None, x_title="Value", y_title="Count")
```

**Description:**
Creates a histogram with statistical annotations (mean, mode, standard deviation).

**Parameters:**
- `series` (pd.Series): Series containing values to plot
- `template_name` (str): Template name for styling
- `paper_size` (str): Paper size specification
- `num_bins` (int): Number of bins; None for auto-calculation (default: None)
- `x_title` (str): X-axis label (default: "Value")
- `y_title` (str): Y-axis label (default: "Count")

**Returns:**
- `plotly.graph_objects.Figure`: The generated Plotly figure

**Usage:**
```python
fig = climatevis.histogram(
    temperature_series,
    template_name='base',
    paper_size='A4_LANDSCAPE',
    num_bins=30,
    x_title='Temperature (°C)'
)
```

---

### `exceedance`

**Signature:**
```python
exceedance(series, template_name, paper_size, x_title="Exceedance Probability", y_title="", selected_percentile=None)
```

**Description:**
Plots an exceedance probability curve showing probability of values exceeding given thresholds.

**Parameters:**
- `series` (pd.Series): Series containing values to plot
- `template_name` (str): Template name for styling
- `paper_size` (str): Paper size specification
- `x_title` (str): X-axis label (default: "Exceedance Probability")
- `y_title` (str): Y-axis label
- `selected_percentile` (float): Percentile (0-100) to highlight with marker

**Returns:**
- `plotly.graph_objects.Figure`: The generated Plotly figure

**Usage:**
```python
fig = climatevis.exceedance(
    wind_speed_series,
    template_name='base',
    paper_size='A4_LANDSCAPE',
    y_title='Wind Speed (m/s)',
    selected_percentile=95
)
```

---

### `exceedance_bands`

**Signature:**
```python
exceedance_bands(series_list, template_name, paper_size, x_title="Exceedance Probability", y_title="", selected_percentile=None)
```

**Description:**
Plots exceedance probability curves with confidence bands for multiple series.

**Parameters:**
- `series_list` (list): List of pd.Series to plot
- `template_name` (str): Template name for styling
- `paper_size` (str): Paper size specification
- `x_title` (str): X-axis label (default: "Exceedance Probability")
- `y_title` (str): Y-axis label
- `selected_percentile` (float): Percentile (0-100) to highlight

**Returns:**
- `plotly.graph_objects.Figure`: The generated Plotly figure

**Usage:**
```python
fig = climatevis.exceedance_bands(
    [wind_2022, wind_2023, wind_2024],
    template_name='base',
    paper_size='A4_LANDSCAPE',
    y_title='Wind Speed (m/s)'
)
```

---

### `cumulative_probability`

**Signature:**
```python
cumulative_probability(series_list, template_name, paper_size, x_title="Value", y_title="Cumulative Probability", selected_percentile=None, y_grid_spacing=10)
```

**Description:**
Plots cumulative probability curves (CDF) for multiple series.

**Parameters:**
- `series_list` (Union[List[pd.Series], pd.Series]): Series or list of series to plot
- `template_name` (str): Template name for styling
- `paper_size` (str): Paper size specification
- `x_title` (str): X-axis label (default: "Value")
- `y_title` (str): Y-axis label (default: "Cumulative Probability")
- `selected_percentile` (float): Percentile (0-100) to highlight
- `y_grid_spacing` (int): Interval for y-axis grid lines in percentage (default: 10)

**Returns:**
- `plotly.graph_objects.Figure`: The generated Plotly figure

**Usage:**
```python
fig = climatevis.cumulative_probability(
    [temperature_series],
    template_name='base',
    paper_size='A4_LANDSCAPE',
    x_title='Temperature (°C)',
    selected_percentile=50
)
```

---

### `wind_rose`

**Signature:**
```python
wind_rose(windspeed, sector, template_name, paper_size)
```

**Description:**
Creates a wind rose diagram showing wind speed and direction frequency distribution.

**Parameters:**
- `windspeed` (pd.Series): Series containing wind speed values
- `sector` (pd.Series): Series containing wind direction sectors (N, NE, E, etc.)
- `template_name` (str): Template name for styling
- `paper_size` (str): Paper size specification

**Returns:**
- `plotly.graph_objects.Figure`: The generated Plotly figure

**Usage:**
```python
fig = climatevis.wind_rose(
    wind_speed_series,
    wind_direction_series,
    template_name='base',
    paper_size='A4_LANDSCAPE'
)
```

---

### `plot_rotated_box`

**Signature:**
```python
plot_rotated_box(template_name, paper_size)
```

**Description:**
Creates a 3D rotated box visualization for demonstrating 3D plotting capabilities.

**Parameters:**
- `template_name` (str): Template name for styling
- `paper_size` (str): Paper size specification

**Returns:**
- `plotly.graph_objects.Figure`: The generated Plotly figure

**Usage:**
```python
fig = climatevis.plot_rotated_box(
    template_name='base',
    paper_size='A4_LANDSCAPE'
)
```

## Marimo UI Components

These functions provide pre-configured marimo UI components for interactive applications.

### `weather_selection`

**Signature:**
```python
weather_selection()
```

**Description:**
Creates a dropdown for selecting weather files from predefined datasets.

**Returns:**
- `marimo.ui.dropdown`: Configured dropdown with weather file options

**Usage:**
```python
import climatevis
dropdown = climatevis.weather_selection()
selected_file = dropdown.value
```

---

### `create_template_dropdown`

**Signature:**
```python
create_template_dropdown(value="base", label="Chart Template", **kwargs)
```

**Description:**
Creates a marimo dropdown pre-configured with all available templates.

**Parameters:**
- `value` (str): Default selected template (default: "base")
- `label` (str): Label for the dropdown (default: "Chart Template")
- `**kwargs`: Additional arguments passed to marimo dropdown

**Returns:**
- `marimo.ui.dropdown`: Configured dropdown with template options

**Usage:**
```python
template_dropdown = climatevis.create_template_dropdown(value="base")
```

---

### `create_paper_size_dropdown`

**Signature:**
```python
create_paper_size_dropdown(value="A4_LANDSCAPE", label="Paper Size", **kwargs)
```

**Description:**
Creates a marimo dropdown pre-configured with available paper sizes.

**Parameters:**
- `value` (str): Default selected paper size (default: "A4_LANDSCAPE")
- `label` (str): Label for the dropdown (default: "Paper Size")
- `**kwargs`: Additional arguments passed to marimo dropdown

**Returns:**
- `marimo.ui.dropdown`: Configured dropdown with paper size options

**Usage:**
```python
paper_dropdown = climatevis.create_paper_size_dropdown(value="A4_LANDSCAPE")
```

---

### `get_template_options`

**Signature:**
```python
get_template_options()
```

**Description:**
Returns the list of available template options for manual dropdown creation.

**Returns:**
- `list`: List of available template names

**Usage:**
```python
templates = climatevis.get_template_options()
```

---

### `get_paper_size_options`

**Signature:**
```python
get_paper_size_options()
```

**Description:**
Returns the list of available paper size options.

**Returns:**
- `list`: List of available paper size names

**Usage:**
```python
paper_sizes = climatevis.get_paper_size_options()
```

## Template Management Functions

### `get_available_templates`

**Signature:**
```python
get_available_templates()
```

**Description:**
Gets a list of all available template names (built-in and custom loaded).

**Returns:**
- `list`: Sorted list of available template names

**Usage:**
```python
templates = climatevis.get_available_templates()
```

---

### `get_builtin_template_names`

**Signature:**
```python
get_builtin_template_names()
```

**Description:**
Gets a list of all built-in template names.

**Returns:**
- `list`: List of built-in template names

**Usage:**
```python
builtin_templates = climatevis.get_builtin_template_names()
```

---

### `get_loaded_template_names`

**Signature:**
```python
get_loaded_template_names()
```

**Description:**
Gets a list of all currently loaded/registered template names.

**Returns:**
- `list`: List of loaded template names

**Usage:**
```python
loaded_templates = climatevis.get_loaded_template_names()
```

---

### `load_all_builtin_templates`

**Signature:**
```python
load_all_builtin_templates()
```

**Description:**
Loads all built-in templates and registers them. Called automatically on package import.

**Returns:**
- `dict`: Dictionary mapping template names to loaded template data

**Usage:**
```python
loaded = climatevis.load_all_builtin_templates()
```

## Available Templates

- `base`: Standard template for professional charts
- `base_autosize`: Auto-sizing version of base template
- `test`: Testing template with distinctive styling

## Available Paper Sizes

- `A6_LANDSCAPE` / `A6_PORTRAIT`: 559×397 / 397×559 pixels
- `A5_LANDSCAPE` / `A5_PORTRAIT`: 794×560 / 560×794 pixels
- `A4_LANDSCAPE` / `A4_PORTRAIT`: 1123×794 / 794×1123 pixels
- `A3_LANDSCAPE` / `A3_PORTRAIT`: 1587×1123 / 1123×1587 pixels
- `A2_LANDSCAPE` / `A2_PORTRAIT`: 2245×1587 / 1587×2245 pixels
- `A1_LANDSCAPE` / `A1_PORTRAIT`: 3175×2245 / 2245×3175 pixels
- `A0_LANDSCAPE` / `A0_PORTRAIT`: 4494×3175 / 3175×4494 pixels

## Series Attributes

ClimateVis uses pandas Series attributes for metadata:

```python
# Set units for automatic axis labeling
series.attrs["unit"] = "°C"
series.attrs["color"] = "red"  # Custom color

# Use with plotting functions
fig = climatevis.plot_series([series], template_name='base', paper_size='A4_LANDSCAPE')
```

## Error Handling

All functions include comprehensive error handling:

- Input validation for data types and formats
- DatetimeIndex requirements for time series functions
- Unit compatibility checks for multi-series plots
- Template and paper size validation

## License

Licensed under the Apache License 2.0. See LICENSE file for details.

## Contributing

Contributions welcome! Please read the contributing guidelines and submit pull requests to the main repository.