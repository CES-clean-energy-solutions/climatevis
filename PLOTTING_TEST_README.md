# Climate Data Plotting Test App

A simple marimo app to test the climatevis plotting library with synthetic 8760-hour temperature and wind data.

## Features

### Data Generation
- **8760 hours** of synthetic climate data (exactly 1 year)
- **Temperature data**: Realistic seasonal and daily variations (°C)
- **Wind speed data**: Realistic patterns with seasonal variations (m/s)

### Interactive Controls
- **Chart Template**: Choose from different Plotly templates
- **Paper Size**: Select A4 or A5 in landscape/portrait
- **Plot Mode**: Line, area, or markers visualization
- **Variables**: View temperature, wind, or both on dual y-axes

### Plots Available
1. **Temperature Time Series**: Annual temperature patterns
2. **Wind Speed Time Series**: Annual wind patterns
3. **Combined Plot**: Dual y-axis plot with both variables

### Data Summary
- Displays statistical summaries for both variables
- Shows data range, mean, standard deviation
- Confirms exact 8760-hour period

## Usage

Run the app:
```bash
python app_plotting_test.py
```

Then open your browser to view the interactive dashboard.

## Technical Details

- Built with **marimo** reactive notebook framework
- Uses **climatevis** plotting library with **Plotly** backend
- Follows marimo best practices for cell organization
- Proper error handling for import failures
- Pandas Series with correct names and unit attributes

## App Structure

- **setup_imports**: Core imports (marimo, pandas, numpy)
- **setup_climatevis_imports**: Import plotting library with error handling
- **generate_synthetic_climate_data**: Create 8760-hour temperature and wind data
- **create_plotting_controls**: Interactive UI widgets
- **create_*_plot**: Generate individual and combined plots
- **display_***: Show plots, summaries, and status information