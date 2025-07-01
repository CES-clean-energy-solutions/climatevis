"""
Climate Data Plotting Test App

This marimo app demonstrates the climatevis library with auto-loaded templates
and dynamic UI components. Templates are automatically loaded when the library
is imported, and dropdowns are populated dynamically.

Features:
- Auto-loading of all built-in templates
- Dynamic template dropdown (populated from available templates)
- Dynamic paper size dropdown
- Synthetic 8760-hour climate data generation
- Multiple plot types and customization options
"""

import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def setup_imports():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import sys
    return mo, np, pd, sys


@app.cell
def setup_climatevis_imports(sys):
    """Import the climatevis plotting library"""
    try:
        # Try to import from the installed package first
        import climatevis
        plot_series = climatevis.plot_series
        util_plotly = climatevis.util_plotly
        create_template_dropdown = climatevis.create_template_dropdown
        create_paper_size_dropdown = climatevis.create_paper_size_dropdown
        success = True
        error_msg = None
    except ImportError:
        try:
            # Fallback to local imports if package not installed
            sys.path.insert(0, ".")
            from plots import plot_series
            from util import util_plotly
            # Create fallback dropdown functions
            def create_template_dropdown(value="base", label="Chart Template"):
                import marimo as mo
                return mo.ui.dropdown(
                    options=["base", "base_autosize", "test"],
                    value=value,
                    label=label
                )
            def create_paper_size_dropdown(value="A4_LANDSCAPE", label="Paper Size"):
                import marimo as mo
                return mo.ui.dropdown(
                    options=["A4_LANDSCAPE", "A4_PORTRAIT", "A5_LANDSCAPE"],
                    value=value,
                    label=label
                )
            success = True
            error_msg = None
        except ImportError as e:
            plot_series = None
            util_plotly = None
            create_template_dropdown = None
            create_paper_size_dropdown = None
            success = False
            error_msg = f"Failed to import plotting library: {str(e)}"

    return (
        create_paper_size_dropdown,
        create_template_dropdown,
        error_msg,
        plot_series,
        success,
        util_plotly,
    )


@app.cell
def generate_synthetic_climate_data(np, pd):
    """Generate synthetic 8760-hour temperature and wind speed data"""
    # Create hourly datetime index for a full year (8760 hours)
    dates = pd.date_range('2023-01-01 00:00:00', '2023-12-31 23:00:00', freq='h')

    # Verify we have exactly 8760 hours
    n_hours = len(dates)

    # Generate realistic temperature data with seasonal variation
    days_of_year = np.arange(n_hours) / 24.0

    # Seasonal temperature variation (sine wave with peak in summer)
    seasonal_component = 15 + 12 * np.sin(2 * np.pi * (days_of_year - 90) / 365.25)

    # Daily temperature variation (cooler at night, warmer during day)
    daily_component = 8 * np.sin(2 * np.pi * (np.arange(n_hours) % 24 - 6) / 24)

    # Add some realistic noise
    noise = np.random.normal(0, 3, n_hours)

    temperature = seasonal_component + daily_component + noise

    # Generate realistic wind speed data
    # Base wind speed with seasonal variation (higher in winter)
    base_wind = 8 + 4 * np.sin(2 * np.pi * (days_of_year - 270) / 365.25)

    # Daily wind pattern (often higher during day)
    daily_wind = 2 * np.sin(2 * np.pi * (np.arange(n_hours) % 24 - 12) / 24)

    # Wind speed noise (more variable than temperature)
    wind_noise = np.random.exponential(2, n_hours)

    wind_speed = np.maximum(0, base_wind + daily_wind + wind_noise)

    # Create pandas Series with proper names and units
    temp_series = pd.Series(temperature, index=dates, name="Air Temperature")
    temp_series.attrs["unit"] = "°C"

    wind_series = pd.Series(wind_speed, index=dates, name="Wind Speed")
    wind_series.attrs["unit"] = "m/s"

    return n_hours, temp_series, wind_series


@app.cell
def create_plotting_controls(create_paper_size_dropdown, create_template_dropdown, mo, success):
    """Create UI controls for plot customization"""
    if success and create_template_dropdown is not None:
        # Use dynamic template dropdown with auto-detected templates
        template_dropdown = create_template_dropdown(
            value="base",
            label="Chart Template"
        )

        # Use dynamic paper size dropdown
        paper_size_dropdown = create_paper_size_dropdown(
            value="A4_LANDSCAPE",
            label="Paper Size"
        )
    else:
        # Fallback to hardcoded dropdowns if imports failed
        template_dropdown = mo.ui.dropdown(
            options=["base", "base_autosize", "test"],
            value="base",
            label="Chart Template"
        )

        paper_size_dropdown = mo.ui.dropdown(
            options=["A4_LANDSCAPE", "A4_PORTRAIT", "A5_LANDSCAPE"],
            value="A4_LANDSCAPE",
            label="Paper Size"
        )

    # Plot mode selection
    mode_dropdown = mo.ui.dropdown(
        options=["line", "area", "markers"],
        value="line",
        label="Plot Mode"
    )

    # Variable selection
    variable_dropdown = mo.ui.dropdown(
        options=["temperature", "wind", "both"],
        value="both",
        label="Variables to Plot"
    )

    return (
        mode_dropdown,
        paper_size_dropdown,
        template_dropdown,
        variable_dropdown,
    )


@app.cell(hide_code=True)
def display_app_header_and_controls(
    mo,
    mode_dropdown,
    n_hours,
    paper_size_dropdown,
    template_dropdown,
    variable_dropdown,
):
    """Display app header and control panel"""
    header = mo.md("# Climate Data Plotting Test")
    description = mo.md(f"""
    Testing the climatevis plotting library with synthetic 8760-hour climate data.

    **Data Generated:** {n_hours:,} hourly values (1 full year)
    """)

    controls = mo.hstack([
        template_dropdown,
        paper_size_dropdown,
        mode_dropdown,
        variable_dropdown
    ])

    mo.vstack([header, description, controls])
    return


@app.cell
def create_temperature_plot(
    mode_dropdown,
    paper_size_dropdown,
    plot_series,
    success,
    temp_series,
    template_dropdown,
):
    """Create temperature time series plot"""
    if success and plot_series is not None:
        try:
            fig_temperature = plot_series(
                [temp_series],
                template_name=template_dropdown.value,
                paper_size=paper_size_dropdown.value,
                y1_axis_title="Air Temperature",
                mode=mode_dropdown.value
            )
            temp_plot_success = True
            temp_plot_error = None
        except Exception as e:
            fig_temperature = None
            temp_plot_success = False
            temp_plot_error = f"Error creating temperature plot: {str(e)}"
    else:
        fig_temperature = None
        temp_plot_success = False
        temp_plot_error = "Plotting library not available"

    return fig_temperature, temp_plot_error, temp_plot_success


@app.cell
def create_wind_plot(
    mode_dropdown,
    paper_size_dropdown,
    plot_series,
    success,
    template_dropdown,
    wind_series,
):
    """Create wind speed time series plot"""
    if success and plot_series is not None:
        try:
            fig_wind = plot_series(
                [wind_series],
                template_name=template_dropdown.value,
                paper_size=paper_size_dropdown.value,
                y1_axis_title="Wind Speed",
                mode=mode_dropdown.value
            )
            wind_plot_success = True
            wind_plot_error = None
        except Exception as e:
            fig_wind = None
            wind_plot_success = False
            wind_plot_error = f"Error creating wind plot: {str(e)}"
    else:
        fig_wind = None
        wind_plot_success = False
        wind_plot_error = "Plotting library not available"

    return fig_wind, wind_plot_error, wind_plot_success


@app.cell
def create_combined_plot(
    mode_dropdown,
    paper_size_dropdown,
    plot_series,
    success,
    temp_series,
    template_dropdown,
    wind_series,
):
    """Create combined temperature and wind plot with dual y-axes"""
    if success and plot_series is not None:
        try:
            fig_combined = plot_series(
                [temp_series, wind_series],
                template_name=template_dropdown.value,
                paper_size=paper_size_dropdown.value,
                y1_axis_title="Climate Variables",
                mode=mode_dropdown.value
            )
            combined_plot_success = True
            combined_plot_error = None
        except Exception as e:
            fig_combined = None
            combined_plot_success = False
            combined_plot_error = f"Error creating combined plot: {str(e)}"
    else:
        fig_combined = None
        combined_plot_success = False
        combined_plot_error = "Plotting library not available"

    return combined_plot_error, combined_plot_success, fig_combined


@app.cell(hide_code=True)
def display_plots(
    combined_plot_error,
    combined_plot_success,
    fig_combined,
    fig_temperature,
    fig_wind,
    mo,
    temp_plot_error,
    temp_plot_success,
    variable_dropdown,
    wind_plot_error,
    wind_plot_success,
):
    """Display the selected plots"""

    if variable_dropdown.value == "temperature":
        if temp_plot_success:
            content = mo.vstack([
                mo.md("## Temperature Time Series"),
                fig_temperature
            ])
        else:
            content = mo.md(f"**Error:** {temp_plot_error}")

    elif variable_dropdown.value == "wind":
        if wind_plot_success:
            content = mo.vstack([
                mo.md("## Wind Speed Time Series"),
                fig_wind
            ])
        else:
            content = mo.md(f"**Error:** {wind_plot_error}")

    elif variable_dropdown.value == "both":
        if combined_plot_success:
            content = mo.vstack([
                mo.md("## Combined Temperature and Wind Speed"),
                mo.md("*Dual y-axis plot with temperature (°C) and wind speed (m/s)*"),
                fig_combined
            ])
        else:
            content = mo.md(f"**Error:** {combined_plot_error}")
    else:
        content = mo.md("Please select a variable to plot")

    content
    return


@app.cell(hide_code=True)
def display_data_summary(mo, temp_series, wind_series):
    """Display summary statistics for the synthetic data"""
    summary = mo.md(f"""
    ## Data Summary

    ### Temperature Data
    - **Range:** {temp_series.min():.1f}°C to {temp_series.max():.1f}°C
    - **Mean:** {temp_series.mean():.1f}°C
    - **Standard Deviation:** {temp_series.std():.1f}°C

    ### Wind Speed Data
    - **Range:** {wind_series.min():.1f} to {wind_series.max():.1f} m/s
    - **Mean:** {wind_series.mean():.1f} m/s
    - **Standard Deviation:** {wind_series.std():.1f} m/s

    ### Time Period
    - **Start:** {temp_series.index.min().strftime('%Y-%m-%d %H:%M')}
    - **End:** {temp_series.index.max().strftime('%Y-%m-%d %H:%M')}
    - **Total Hours:** {len(temp_series):,} (exactly 1 year)
    """)

    summary
    return


# @app.cell(hide_code=True)
# def display_import_status(error_msg, mo, success, util_plotly):
#     """Display import status, template loading info, and any errors"""
#     if success:
#         try:
#             # Get template information
#             available_templates = util_plotly.get_available_templates() if util_plotly else []
#             loaded_templates = util_plotly.get_loaded_template_names() if util_plotly else []

#             status_text = f"""
# ✅ **Status:** ClimateVis library imported successfully

# **Templates Auto-loaded:** {len(available_templates)} templates available
# - Available templates: {', '.join(available_templates) if available_templates else 'None'}
# - Total loaded in Plotly: {len(loaded_templates)}

# **Features:**
# - ✅ Auto-loading of templates on import
# - ✅ Dynamic template dropdown
# - ✅ Dynamic paper size dropdown
# - ✅ Synthetic climate data generation
#             """
#             status = mo.md(status_text)
#         except Exception as e:
#             status = mo.md(f"✅ **Status:** Library imported but template info unavailable: {e}")
#     else:
#         status = mo.md(f"❌ **Status:** {error_msg}")

#     status
#     return


if __name__ == "__main__":
    app.run()
