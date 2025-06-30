import numpy as np
import plotly.graph_objs as go
import psychrolib
import logging

# Initialize psychrolib for SI units
psychrolib.SetUnitSystem(psychrolib.SI)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Constants for colors and styles
COLOR_LIGHT_GREY = '#e0e0e0'      # Light grey for minor grid lines
COLOR_DARK_GREY = '#b0b0b0'       # Darker grey for major grid lines (every 5°C)
# COLOR_RH_LINE = '#ffa500'         # Orange for Relative Humidity lines
COLOR_RH_LINE = COLOR_LIGHT_GREY
COLOR_SATURATION = 'black'        # Black for saturation curve
LINE_WIDTH_MINOR = 1              # Line width for minor grid lines
LINE_WIDTH_MAJOR = 1.5            # Line width for major grid lines
LINE_WIDTH_RH = 1                 # Line width for RH lines
LINE_STYLE_RH = 'solid'            # Line style for RH lines

def generate_hover_text(**kwargs):
    """
    Generates HTML-formatted hover text based on provided keyword arguments.

    Parameters:
    - kwargs: Key-value pairs representing different properties.

    Returns:
    - A string containing HTML-formatted hover text.
    """
    hover_text = "<br>".join([f"{key}: {value}" for key, value in kwargs.items()])
    return hover_text

def plot_humidity_ratio_lines(fig, temp_range, humidity_ratios, pressure):
    """
    Plots humidity ratio lines (constant w) on the psychrometric chart.

    Parameters:
    - fig (go.Figure): The Plotly figure object.
    - temp_range (numpy.ndarray): Array of temperature values.
    - humidity_ratios (numpy.ndarray): Array of humidity ratio values.
    - pressure (float): Atmospheric pressure in Pascals.

    Returns:
    - None
    """
    for w in humidity_ratios:
        # Determine valid temperature range for the given humidity ratio
        temp_min_valid = None
        for t_val in temp_range:
            try:
                w_sat = psychrolib.GetHumRatioFromRelHum(t_val, 1.0, pressure)
                if w <= w_sat:
                    temp_min_valid = t_val
                    break
            except Exception as e:
                logging.error(f"Error computing saturation humidity ratio for T={t_val}°C: {e}")
                continue

        if temp_min_valid is not None:
            temp_valid = temp_range[temp_range >= temp_min_valid]
            w_values = [w] * len(temp_valid)

            # Compute hover information
            hover_text = []
            for t_val in temp_valid:
                try:
                    rh = psychrolib.GetRelHumFromHumRatio(t_val, w, pressure) * 100  # %
                    twb = psychrolib.GetTWetBulbFromHumRatio(t_val, w, pressure)
                    h = psychrolib.GetMoistAirEnthalpy(t_val, w) / 1000  # kJ/kg
                    text = generate_hover_text(
                        Temperature=f"{t_val:.1f}°C",
                        Humidity_Ratio=f"{w:.3f} kg/kg",
                        Relative_Humidity=f"{rh:.1f}%",
                        Wet_Bulb_Temp=f"{twb:.1f}°C",
                        Enthalpy=f"{h:.1f} kJ/kg"
                    )
                except Exception as e:
                    logging.error(f"Error computing hover text for T={t_val}°C, w={w} kg/kg: {e}")
                    text = "Invalid Data"
                hover_text.append(text)

            # Add trace
            fig.add_trace(go.Scatter(
                x=temp_valid,
                y=w_values,
                mode='lines',
                line=dict(color=COLOR_LIGHT_GREY, width=LINE_WIDTH_MINOR),
                showlegend=False,
                hoverinfo='text',
                hovertext=hover_text
            ))

def plot_temperature_lines(fig, temp_range, temp_step, line_color_light, line_color_dark, line_width_minor, line_width_major, pressure):
    """
    Plots temperature lines (constant T) on the psychrometric chart.

    Parameters:
    - fig (go.Figure): The Plotly figure object.
    - temp_range (numpy.ndarray): Array of temperature values.
    - temp_step (float): Step size for temperature.
    - line_color_light (str): Color for minor temperature lines.
    - line_color_dark (str): Color for major temperature lines (every 5°C).
    - line_width_minor (int): Line width for minor temperature lines.
    - line_width_major (float): Line width for major temperature lines.
    - pressure (float): Atmospheric pressure in Pascals.

    Returns:
    - None
    """
    for t in temp_range:
        try:
            w_sat = psychrolib.GetHumRatioFromRelHum(t, 1.0, pressure)
            w_range = np.linspace(0, w_sat, 50)
            T_range = [t] * len(w_range)

            hover_text = []
            for w_val in w_range:
                try:
                    rh = psychrolib.GetRelHumFromHumRatio(t, w_val, pressure) * 100  # %
                    twb = psychrolib.GetTWetBulbFromHumRatio(t, w_val, pressure)
                    h = psychrolib.GetMoistAirEnthalpy(t, w_val) / 1000  # kJ/kg
                    text = generate_hover_text(
                        Temperature=f"{t:.1f}°C",
                        Humidity_Ratio=f"{w_val:.3f} kg/kg",
                        Relative_Humidity=f"{rh:.1f}%",
                        Wet_Bulb_Temp=f"{twb:.1f}°C",
                        Enthalpy=f"{h:.1f} kJ/kg"
                    )
                except Exception as e:
                    logging.error(f"Error computing hover text for T={t}°C, w={w_val} kg/kg: {e}")
                    text = "Invalid Data"
                hover_text.append(text)

            # Determine line color and width
            if t % 5 == 0:
                current_line_color = line_color_dark
                current_line_width = line_width_major
            else:
                current_line_color = line_color_light
                current_line_width = line_width_minor

            # Add trace
            fig.add_trace(go.Scatter(
                x=T_range,
                y=w_range,
                mode='lines',
                line=dict(color=current_line_color, width=current_line_width),
                showlegend=False,
                hoverinfo='text',
                hovertext=hover_text
            ))
        except Exception as e:
            logging.error(f"Error plotting temperature line for T={t}°C: {e}")
            continue

def plot_enthalpy_lines(fig, temp_range, enthalpy_values, temp_min, temp_max, pressure):
    """
    Plots enthalpy lines (constant h) on the psychrometric chart.

    Parameters:
    - fig (go.Figure): The Plotly figure object.
    - temp_range (numpy.ndarray): Array of temperature values.
    - enthalpy_values (numpy.ndarray): Array of enthalpy values.
    - temp_min (float): Minimum temperature for the chart.
    - temp_max (float): Maximum temperature for the chart.
    - pressure (float): Atmospheric pressure in Pascals.

    Returns:
    - None
    """
    for h in enthalpy_values:
        temp_vals = []
        w_vals = []
        hover_text = []

        # Iterate over a range of humidity ratios
        w_enthalpy = np.linspace(0.005, 0.030, 100)
        for w in w_enthalpy:
            try:
                # Compute dry-bulb temperature for given enthalpy and humidity ratio
                t = psychrolib

                t = psychrolib.GetDryBulbFromEnthalpyAndHumRatio(h * 1000, w, pressure)
                if temp_min <= t <= temp_max:
                    w_sat = psychrolib.GetHumRatioFromRelHum(t, 1.0, pressure)
                    if w <= w_sat:
                        temp_vals.append(t)
                        w_vals.append(w)
                        # Compute hover text
                        rh = psychrolib.GetRelHumFromHumRatio(t, w, pressure) * 100  # %
                        twb = psychrolib.GetTWetBulbFromHumRatio(t, w, pressure)
                        text = generate_hover_text(
                            Enthalpy=f"{h} kJ/kg",
                            Temperature=f"{t:.1f}°C",
                            Humidity_Ratio=f"{w:.3f} kg/kg",
                            Relative_Humidity=f"{rh:.1f}%",
                            Wet_Bulb_Temp=f"{twb:.1f}°C"
                        )
                        hover_text.append(text)
            except Exception as e:
                logging.error(f"Error computing enthalpy line for h={h} kJ/kg, w={w} kg/kg: {e}")
                continue

        if temp_vals and w_vals:
            fig.add_trace(go.Scatter(
                x=temp_vals,
                y=w_vals,
                mode='lines',
                line=dict(color=COLOR_LIGHT_GREY, width=1),
                showlegend=False,
                hoverinfo='text',
                hovertext=hover_text
            ))

def plot_saturation_curve(fig, temp_range, saturation_w, pressure):
    """
    Plots the saturation curve (RH=100%) on the psychrometric chart.

    Parameters:
    - fig (go.Figure): The Plotly figure object.
    - temp_range (numpy.ndarray): Array of temperature values.
    - saturation_w (list): List of saturation humidity ratio values.
    - pressure (float): Atmospheric pressure in Pascals.

    Returns:
    - None
    """
    saturation_hover_text = []
    for t_val, w_sat in zip(temp_range, saturation_w):
        try:
            rh = 100.0  # %
            twb = psychrolib.GetTWetBulbFromHumRatio(t_val, w_sat, pressure)
            h = psychrolib.GetMoistAirEnthalpy(t_val, w_sat) / 1000  # kJ/kg
            text = generate_hover_text(
                Saturation_Curve="RH=100%",
                Temperature=f"{t_val:.1f}°C",
                Humidity_Ratio=f"{w_sat:.3f} kg/kg",
                Relative_Humidity=f"{rh}%",
                Wet_Bulb_Temp=f"{twb:.1f}°C",
                Enthalpy=f"{h:.1f} kJ/kg"
            )
        except Exception as e:
            logging.error(f"Error computing saturation curve parameters for T={t_val}°C: {e}")
            text = "Invalid Data"
        saturation_hover_text.append(text)

    fig.add_trace(go.Scatter(
        x=temp_range,
        y=saturation_w,
        mode='lines',
        line=dict(color=COLOR_SATURATION, width=2),
        name='Saturation (RH=100%)',
        showlegend=False,
        hoverinfo='text',
        hovertext=saturation_hover_text
    ))

def plot_relative_humidity_lines(fig, temp_range, rh_values, pressure):
    """
    Plots Relative Humidity (RH) lines on the psychrometric chart.

    Parameters:
    - fig (go.Figure): The Plotly figure object.
    - temp_range (numpy.ndarray): Array of temperature values.
    - rh_values (numpy.ndarray): Array of RH values to plot.
    - pressure (float): Atmospheric pressure in Pascals.

    Returns:
    - None
    """
    for rh in rh_values:
        temp_rh = []
        w_rh = []
        hover_rh = []
        for t_val in temp_range:
            try:
                w_val = psychrolib.GetHumRatioFromRelHum(t_val, rh / 100.0, pressure)
                w_sat = psychrolib.GetHumRatioFromRelHum(t_val, 1.0, pressure)
                if w_val <= w_sat:
                    temp_rh.append(t_val)
                    w_rh.append(w_val)
                    # Compute hover text
                    twb = psychrolib.GetTWetBulbFromHumRatio(t_val, w_val, pressure)
                    h = psychrolib.GetMoistAirEnthalpy(t_val, w_val) / 1000  # kJ/kg
                    text = generate_hover_text(
                        Relative_Humidity=f"{rh}%",
                        Temperature=f"{t_val:.1f}°C",
                        Humidity_Ratio=f"{w_val:.3f} kg/kg",
                        Wet_Bulb_Temp=f"{twb:.1f}°C",
                        Enthalpy=f"{h:.1f} kJ/kg"
                    )
                    hover_rh.append(text)
            except Exception as e:
                logging.error(f"Error computing RH line for RH={rh}%, T={t_val}°C: {e}")
                continue  # Skip if calculation fails

        if temp_rh and w_rh:
            # Include in legend only every 20% RH to avoid clutter
            # show_in_legend = bool(rh % 20 == 0)
            show_in_legend = False
            fig.add_trace(go.Scatter(
                x=temp_rh,
                y=w_rh,
                mode='lines',
                line=dict(color=COLOR_RH_LINE, width=LINE_WIDTH_RH, dash=LINE_STYLE_RH),
                name=f'RH={rh}%',
                showlegend=show_in_legend,
                hoverinfo='text',
                hovertext=hover_rh
            ))

def add_state_points(fig, state_points):
    """
    Adds StatePoint instances to the psychrometric chart.

    Parameters:
    - fig (go.Figure): The Plotly figure object.
    - state_points (list of StatePoint): List of StatePoint instances.

    Returns:
    - fig (go.Figure): Updated Plotly figure with state points added.
    """
    for point in state_points:
        try:
            # Retrieve the required attributes directly from the StatePoint instance
            temp_pt = point.temperature
            w_pt = point._humidity_ratio  # Internal representation in kg/kg

            # Lookup color from StatePoint object (fallback to blue if not available)
            if hasattr(point, 'color_rgb') and point.color_rgb:
                # Convert RGB tuple to rgba string format for Plotly
                r, g, b = point.color_rgb
                color_pt = f"rgb({r}, {g}, {b})"
            elif hasattr(point, 'color') and point.color:
                # If color is already in string format, use it directly
                color_pt = point.color
            else:
                # Fallback to default blue color
                color_pt = 'rgb(0, 0, 255)'  # Default blue as RGB

            label_pt = point.label
            name_pt = point.name

            # Generate hover text directly from the StatePoint instance
            hover_text = generate_hover_text(
                State_Point=f"{label_pt}",
                Temperature=f"{temp_pt:.1f}°C",
                Humidity_Ratio=f"{w_pt:.3f} kg/kg",
                Relative_Humidity=f"{point.relative_humidity:.1f}%",
                Wet_Bulb_Temp=f"{point.wet_bulb_temp:.1f}°C",
                Enthalpy=f"{point.enthalpy / 1000:.1f} kJ/kg",  # Convert J/kg to kJ/kg
                CO2=f"{point.co2_ppm:.1f} ppm"
            )

            # Add state point as a marker with label
            fig.add_trace(go.Scatter(
                x=[temp_pt],
                y=[w_pt],
                mode='markers+text',
                marker=dict(color=color_pt, size=12, symbol='circle'),
                text=[label_pt],
                textposition='top center',
                textfont=dict(color=color_pt, size=12, family="Arial"),
                showlegend=True,
                name=f"{label_pt} {name_pt}",
                hoverinfo='text',
                hovertext=hover_text
            ))

        except Exception as e:
            logging.error(f"Error adding State Point '{point.name}': {e}")
            continue  # Skip adding this state point

    fig.update_layout(
        legend=dict(
            x=0.02,  # Horizontal position (0.0 is far left, 1.0 is far right)
            y=0.98,  # Vertical position (1.0 is top, 0.0 is bottom)
            bgcolor='rgba(255, 255, 255, 0.7)',  # Semi-transparent white background
            bordercolor='black',
            borderwidth=1,
            font=dict(size=10)  # Optional: Adjust font size
        )
    )

    return fig




def get_psych_chart(temp_min=5, temp_max=45, temp_step=0.5,
                  humidity_ratio_min=0.005, humidity_ratio_max=0.030, humidity_ratio_step=0.005,
                  enthalpy_min=10, enthalpy_max=120, enthalpy_step=10,
                  rh_min=10, rh_max=100, rh_step=10,
                  pressure=101325):
    """
    Generates a comprehensive psychrometric chart using Plotly and psychrolib, including
    humidity ratio lines, temperature lines, enthalpy lines, saturation curve, and RH lines.

    Parameters:
    - temp_min (float): Minimum dry-bulb temperature (°C).
    - temp_max (float): Maximum dry-bulb temperature (°C).
    - temp_step (float): Step size for temperature.
    - humidity_ratio_min (float): Minimum humidity ratio (kg/kg).
    - humidity_ratio_max (float): Maximum humidity ratio (kg/kg).
    - humidity_ratio_step (float): Step size for humidity ratio.
    - enthalpy_min (float): Minimum enthalpy (kJ/kg).
    - enthalpy_max (float): Maximum enthalpy (kJ/kg).
    - enthalpy_step (float): Step size for enthalpy.
    - rh_min (float): Minimum Relative Humidity (%) for RH lines.
    - rh_max (float): Maximum Relative Humidity (%) for RH lines.
    - rh_step (float): Step size for RH lines.
    - pressure (float): Atmospheric pressure in Pascals.

    Returns:
    - fig (go.Figure): The completed psychrometric chart.
    """
    # Generate ranges
    temp_range = np.arange(temp_min, temp_max + temp_step, temp_step)
    humidity_ratios = np.arange(humidity_ratio_min, humidity_ratio_max + humidity_ratio_step, humidity_ratio_step)
    enthalpy_values = np.arange(enthalpy_min, enthalpy_max + enthalpy_step, enthalpy_step)
    rh_values = np.arange(rh_min, rh_max + rh_step, rh_step)

    # Compute saturation humidity ratio
    w_saturation = []
    for t in temp_range:
        try:
            w_sat = psychrolib.GetHumRatioFromRelHum(t, 1.0, pressure)
            w_saturation.append(w_sat)
        except Exception as e:
            logging.error(f"Error computing saturation humidity ratio for T={t}°C: {e}")
            w_saturation.append(None)

    # Initialize Plotly figure
    fig = go.Figure()

    # Plot all chart components
    plot_humidity_ratio_lines(fig, temp_range, humidity_ratios, pressure)
    plot_temperature_lines(fig, temp_range, temp_step, COLOR_LIGHT_GREY, COLOR_DARK_GREY, LINE_WIDTH_MINOR, LINE_WIDTH_MAJOR, pressure)
    #TODO: Fix this
    # plot_enthalpy_lines(fig, temp_range, enthalpy_values, temp_min, temp_max, pressure)
    plot_saturation_curve(fig, temp_range, w_saturation, pressure)
    plot_relative_humidity_lines(fig, temp_range, rh_values, pressure)

    # Update layout
    fig.update_layout(
        title='Psychrometric Chart',
        xaxis_title='Dry-Bulb Temperature (°C)',
        yaxis_title='Humidity Ratio (kg/kg)',
        # legend_title='Lines',
        template='plotly_white',
        width=900,
        height=700,
        xaxis=dict(
            range=[temp_min, temp_max],
            showgrid=False
        ),
        yaxis=dict(
            range=[0, max(filter(None, w_saturation)) * 1.05],
            showgrid=False,
            side='right'  # Position the y-axis on the right side
        ),
        hovermode='closest'
    )

    return fig