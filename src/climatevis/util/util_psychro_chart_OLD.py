import psychrolib
psychrolib.SetUnitSystem(psychrolib.SI)

import numpy as np
import plotly.graph_objects as go

def add_state_points(fig, state_points, pressure=101325):
    """
    Adds customizable state points to the psychrometric chart.

    Parameters:
    - fig (plotly.graph_objs.Figure): The psychrometric chart figure.
    - state_points (list of dict): List of state points with 'temp', 'w', 'color', and 'label' keys.
    - pressure (float): Atmospheric pressure in Pascals (default: 101325 Pa).

    Returns:
    - fig (plotly.graph_objs.Figure): The updated figure with state points.
    """
    for point in state_points:
        temp_pt = point.get('temp')
        w_pt = point.get('w')
        color_pt = point.get('color', 'blue')  # Default color is blue if not specified
        label_pt = point.get('label', '')      # Default label is empty if not specified

        # Compute additional parameters for hover
        try:
            rh_pt = psychrolib.GetRelHumFromHumRatio(temp_pt, w_pt, pressure) * 100  # Convert to %
            twb_pt = psychrolib.GetTWetBulbFromHumRatio(temp_pt, w_pt, pressure)
            h_pt = psychrolib.GetMoistAirEnthalpy(temp_pt, w_pt) / 1000  # Convert to kJ/kg
        except Exception as e:
            # Print the error message with state point details
            print(f"Error adding State Point {label_pt}: {e}")
            rh_pt = np.nan
            twb_pt = np.nan
            h_pt = np.nan

        # Add state point as a marker with label
        fig.add_trace(go.Scatter(
            x=[temp_pt],
            y=[w_pt],
            mode='markers+text',
            marker=dict(color=color_pt, size=12, symbol='circle'),
            text=[label_pt],
            textposition='top center',
            textfont=dict(color=color_pt, size=12, family="Arial"),
            showlegend=False,
            hoverinfo='text',
            hovertext=(
                f"State Point: {label_pt}<br>"
                f"Temperature: {temp_pt:.1f}°C<br>"
                f"Humidity Ratio: {w_pt:.3f} kg/kg<br>"
                f"Relative Humidity: {rh_pt:.1f}%<br>"
                f"Wet-Bulb Temp: {twb_pt:.1f}°C<br>"
                f"Enthalpy: {h_pt:.1f} kJ/kg"
            )
        ))

    return fig


def get_psych_chart(temp_min=5, temp_max=50, temp_step=0.5,
                    humidity_ratio_min=0.005, humidity_ratio_max=0.030, humidity_ratio_step=0.005,
                    enthalpy_min=10, enthalpy_max=120, enthalpy_step=10,
                    pressure=101325):
    """
    Generates an optimized psychrometric chart using Plotly and psychrolib.

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
    - pressure (float): Atmospheric pressure in Pascals.

    Returns:
    - fig (plotly.graph_objs.Figure): The psychrometric chart figure.
    """

    # Define temperature array
    temp = np.arange(temp_min, temp_max + temp_step, temp_step)

    # Define humidity ratio array
    humidity_ratio = np.arange(humidity_ratio_min, humidity_ratio_max + humidity_ratio_step, humidity_ratio_step)

    # Define enthalpy array
    enthalpy = np.arange(enthalpy_min, enthalpy_max + enthalpy_step, enthalpy_step)

    # Compute saturation humidity ratio for each temperature
    w_saturation = []
    for t in temp:
        try:
            w_sat = psychrolib.GetHumRatioFromRelHum(t, 1.0, pressure)
            w_saturation.append(w_sat)
        except:
            w_saturation.append(None)

    # Create a Plotly figure
    fig = go.Figure()

    # Define colors for grid lines
    line_color_light = '#e0e0e0'  # Light grey for minor lines
    line_color_dark = '#b0b0b0'   # Darker grey for major lines (every 5°C)
    line_width = 1  # Thin lines

    # =======================
    # Plot RH lines
    # =======================
    # Function to compute humidity ratio from relative humidity
    def compute_humidity_ratio(temp, rh, pressure):
        return psychrolib.GetHumRatioFromRelHum(temp, rh, pressure)

    # Compute RH lines
    rh_lines = {}
    for rh in chart["rh"]:
        if rh == 0:
            continue  # Skip RH=0 to avoid undefined humidity ratio
        w = [
            compute_humidity_ratio(t, rh, chart["pressure"])
            for t in chart["temp"]
        ]
        rh_lines[rh] = w


    for rh, w in rh_lines.items():
        fig.add_trace(
            go.Scatter(
                x=chart["temp"],
                y=w,
                mode="lines",
                name=f"RH = {int(rh*100)}%",  # This name will not appear in legend
                line=dict(
                    color=line_color_light, width=line_width),
                showlegend=False,  # Exclude RH lines from the legend
            )
        )

    # =======================
    # Plot Humidity Ratio Lines (Constant w)
    # =======================
    for w in humidity_ratio:
        # Find the first temperature where w <= w_sat(t)
        t_min = None
        for t_val, w_sat in zip(temp, w_saturation):
            if w <= w_sat:
                t_min = t_val
                break
        if t_min is not None:
            # Plot from t_min to temp_max
            temp_valid = temp[temp >= t_min]
            w_values = [w] * len(temp_valid)

            # Compute additional parameters for hover
            rh_values = []
            twb_values = []
            enthalpy_values = []
            for t_val in temp_valid:
                try:
                    rh = psychrolib.GetRelHumFromHumRatio(t_val, w, pressure) * 100  # Convert to %
                    twb = psychrolib.GetTWetBulbFromHumRatio(t_val, w, pressure)
                    h = psychrolib.GetMoistAirEnthalpy(t_val, w, pressure) / 1000  # Convert to kJ/kg
                except:
                    rh = np.nan
                    twb = np.nan
                    h = np.nan
                rh_values.append(rh)
                twb_values.append(twb)
                enthalpy_values.append(h)

            # Create hover text
            hover_text = [
                f"Temperature: {t_val:.1f}°C<br>"
                f"Humidity Ratio: {w:.3f} kg/kg<br>"
                f"Relative Humidity: {rh:.1f}%<br>"
                f"Wet-Bulb Temp: {twb:.1f}°C<br>"
                f"Enthalpy: {h:.1f} kJ/kg"
                for t_val, rh, twb, h in zip(temp_valid, rh_values, twb_values, enthalpy_values)
            ]

            # Add the trace
            fig.add_trace(go.Scatter(
                x=temp_valid,
                y=w_values,
                mode='lines',
                line=dict(color=line_color_light, width=line_width),
                showlegend=False,  # Exclude from legend
                hoverinfo='text',
                hovertext=hover_text
            ))

    # =======================
    # Plot Temperature Lines (Constant T)
    # =======================
    for t in temp:
        try:
            # Compute saturation humidity ratio at this temperature
            w_sat = psychrolib.GetHumRatioFromRelHum(t, 1.0, pressure)
            # Define humidity ratio range from 0 to saturation
            w_range = np.linspace(0, w_sat, 50)  # Reduced points for performance
            # Temperature is constant
            T_range = [t] * len(w_range)

            # Compute additional parameters for hover
            rh_values = []
            twb_values = []
            enthalpy_values = []
            for w_val in w_range:
                try:
                    rh = psychrolib.GetRelHumFromHumRatio(t, w_val, pressure) * 100  # Convert to %
                    twb = psychrolib.GetTWetBulbFromHumRatio(t, w_val, pressure)
                    h_pt = psychrolib.GetMoistAirEnthalpy(temp_pt, w_pt) / 1000  # Convert to kJ/kg
                except:
                    rh = np.nan
                    twb = np.nan
                    h = np.nan
                rh_values.append(rh)
                twb_values.append(twb)
                enthalpy_values.append(h)

            # Create hover text
            hover_text = [
                f"Temperature: {t:.1f}°C<br>"
                f"Humidity Ratio: {w:.3f} kg/kg<br>"
                f"Relative Humidity: {rh:.1f}%<br>"
                f"Wet-Bulb Temp: {twb:.1f}°C<br>"
                f"Enthalpy: {h:.1f} kJ/kg"
                for w, rh, twb, h in zip(w_range, rh_values, twb_values, enthalpy_values)
            ]

            # Determine line color: darker if every 5°C
            if t % 5 == 0:
                current_line_color = line_color_dark
                current_line_width = 1.5  # Slightly thicker for prominence
            else:
                current_line_color = line_color_light
                current_line_width = line_width

            # Add the trace
            fig.add_trace(go.Scatter(
                x=T_range,
                y=w_range,
                mode='lines',
                line=dict(color=current_line_color, width=current_line_width),
                showlegend=False,  # Exclude from legend
                hoverinfo='text',
                hovertext=hover_text
            ))
        except:
            continue  # Skip if calculation fails

    # =======================
    # Plot Enthalpy Lines (Constant h)
    # =======================
    for h in enthalpy:
        temp_vals = []
        w_vals = []
        # Define a range of humidity ratios for enthalpy calculation
        w_enthalpy = np.linspace(humidity_ratio_min, humidity_ratio_max, 50)  # Reduced points for performance
        for w in w_enthalpy:
            try:
                # Compute dry-bulb temperature for given enthalpy and humidity ratio
                # Enthalpy in J/kg (kJ/kg to J/kg)
                t = psychrolib.GetDryBulbFromEnthalpyAndHumRatio(h * 1000, w, pressure)
                # Check if temperature is within the defined range and below saturation
                if temp_min <= t <= temp_max:
                    w_sat = psychrolib.GetHumRatioFromRelHum(t, 1.0, pressure)
                    if w <= w_sat:
                        temp_vals.append(t)
                        w_vals.append(w)
            except:
                continue  # Skip if no solution

        if temp_vals and w_vals:
            # Compute additional parameters for hover
            rh_values = []
            twb_values = []
            for t_val, w_val in zip(temp_vals, w_vals):
                try:
                    rh = psychrolib.GetRelHumFromHumRatio(t_val, w_val, pressure) * 100  # Convert to %
                    twb = psychrolib.GetTWetBulbFromHumRatio(t_val, w_val, pressure)
                except:
                    rh = np.nan
                    twb = np.nan
                rh_values.append(rh)
                twb_values.append(twb)

            # Create hover text
            hover_text = [
                f"Enthalpy: {h} kJ/kg<br>"
                f"Temperature: {t_val:.1f}°C<br>"
                f"Humidity Ratio: {w_val:.3f} kg/kg<br>"
                f"Relative Humidity: {rh:.1f}%<br>"
                f"Wet-Bulb Temp: {twb:.1f}°C"
                for t_val, w_val, rh, twb in zip(temp_vals, w_vals, rh_values, twb_values)
            ]

            # Add the trace
            fig.add_trace(go.Scatter(
                x=temp_vals,
                y=w_vals,
                mode='lines',
                line=dict(color=line_color_light, width=line_width),
                showlegend=False,  # Exclude from legend
                hoverinfo='text',
                hovertext=hover_text
            ))

    # =======================
    # Plot Saturation Curve (RH=100%)
    # =======================
    # Compute additional parameters for hover
    saturation_hover_text = []
    for t_val, w_sat in zip(temp, w_saturation):
        try:
            rh = 100.0  # Saturation curve corresponds to RH=100%
            twb = psychrolib.GetTWetBulbFromHumRatio(t_val, w_sat, pressure)
            h = psychrolib.GetMoistAirEnthalpy(t_val, w_sat, pressure) / 1000  # Convert to kJ/kg
        except:
            rh = np.nan
            twb = np.nan
            h = np.nan
        saturation_hover_text.append(
            f"Saturation Curve<br>Temperature: {t_val:.1f}°C<br>Humidity Ratio: {w_sat:.3f} kg/kg<br>"
            f"Relative Humidity: {rh:.1f}%<br>Wet-Bulb Temp: {twb:.1f}°C<br>Enthalpy: {h:.1f} kJ/kg"
        )

    fig.add_trace(go.Scatter(
        x=temp,
        y=w_saturation,
        mode='lines',
        line=dict(color=line_color_light, width=2),
        name='Saturation (RH=100%)',
        showlegend=False,  # Include in legend
        hoverinfo='text',
        hovertext=saturation_hover_text
    ))

    # =======================
    # Update Layout
    # =======================
    fig.update_layout(
        title='Psychrometric Chart',
        xaxis_title='Dry-Bulb Temperature (°C)',
        yaxis_title='Humidity Ratio (kg/kg)',
        legend_title='Lines',
        template='plotly_white',
        width=900,
        height=700,
        xaxis=dict(
            range=[temp_min, temp_max],
            showgrid=False
        ),
        yaxis=dict(
            range=[0, max(w_saturation)*1.05],
            showgrid=False,
            side='right'  # Position the y-axis on the right side
        ),
        hovermode='closest'
    )

    return fig





def get_psych_cart_OLD(temp_min=5, temp_max=45, temp_step=0.1,
                    humidity_ratio_min=0.005, humidity_ratio_max=0.030, humidity_ratio_step=0.005,
                    enthalpy_min=10, enthalpy_max=120, enthalpy_step=10,
                    pressure=101325):
    """
    Generates a psychrometric chart using Plotly and psychrolib.

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
    - pressure (float): Atmospheric pressure in Pascals.

    Returns:
    - fig (plotly.graph_objs.Figure): The psychrometric chart figure.
    """

    # Define temperature array
    temp = np.arange(temp_min, temp_max + temp_step, temp_step)

    # Define humidity ratio array
    humidity_ratio = np.arange(humidity_ratio_min, humidity_ratio_max + humidity_ratio_step, humidity_ratio_step)

    # Define enthalpy array
    enthalpy = np.arange(enthalpy_min, enthalpy_max + enthalpy_step, enthalpy_step)

    # Compute saturation humidity ratio for each temperature
    w_saturation = []
    for t in temp:
        try:
            w_sat = psychrolib.GetHumRatioFromRelHum(t, 1.0, pressure)
            w_saturation.append(w_sat)
        except:
            w_saturation.append(None)

    # Create a Plotly figure
    fig = go.Figure()

    # Define a lighter grey color for grid lines
    line_color = '#e0e0e0'  # Light grey
    line_width = 1  # Thin lines

    # =======================
    # Plot Humidity Ratio Lines (Constant w)
    # =======================
    for w in humidity_ratio:
        # Find the first temperature where w <= w_sat(t)
        t_min = None
        for t_val, w_sat in zip(temp, w_saturation):
            if w <= w_sat:
                t_min = t_val
                break
        if t_min is not None:
            # Plot from t_min to temp_max
            temp_valid = temp[temp >= t_min]
            w_values = [w] * len(temp_valid)
            hover_text = [f'Humidity Ratio: {w:.3f} kg/kg<br>Temperature: {t:.1f}°C' for t in temp_valid]
            fig.add_trace(go.Scatter(
                x=temp_valid,
                y=w_values,
                mode='lines',
                line=dict(color=line_color, width=line_width),
                showlegend=False,  # Exclude from legend
                hoverinfo='text',
                hovertext=hover_text
            ))

    # =======================
    # Plot Temperature Lines (Constant T)
    # =======================
    for t in temp:
        try:
            # Compute saturation humidity ratio at this temperature
            w_sat = psychrolib.GetHumRatioFromRelHum(t, 1.0, pressure)
            # Define humidity ratio range from 0 to saturation
            w_range = np.linspace(0, w_sat, 100)
            # Temperature is constant
            T_range = [t] * len(w_range)

            hover_text = [f'Temperature: {t:.1f}°C<br>Humidity Ratio: {w:.3f} kg/kg' for w in w_range]

            fig.add_trace(go.Scatter(
                x=T_range,
                y=w_range,
                mode='lines',
                line=dict(color=line_color, width=line_width),
                showlegend=False,  # Exclude from legend
                hoverinfo='text',
                hovertext=hover_text
            ))
        except:
            continue  # Skip if calculation fails

    # =======================
    # Plot Enthalpy Lines (Constant h)
    # =======================
    for h in enthalpy:
        temp_vals = []
        w_vals = []
        # Define a range of humidity ratios for enthalpy calculation
        w_enthalpy = np.linspace(humidity_ratio_min, humidity_ratio_max, 100)
        for w in w_enthalpy:
            try:
                # Compute dry-bulb temperature for given enthalpy and humidity ratio
                # Enthalpy in J/kg (kJ/kg to J/kg)
                t = psychrolib.GetDryBulbFromEnthalpyAndHumRatio(h * 1000, w, pressure)
                # Check if temperature is within the defined range and below saturation
                if temp_min <= t <= temp_max:
                    w_sat = psychrolib.GetHumRatioFromRelHum(t, 1.0, pressure)
                    if w <= w_sat:
                        temp_vals.append(t)
                        w_vals.append(w)
            except:
                continue  # Skip if no solution

        if temp_vals and w_vals:
            hover_text = [f'Enthalpy: {h} kJ/kg<br>Temperature: {t:.1f}°C<br>Humidity Ratio: {w:.3f} kg/kg'
                            for t, w in zip(temp_vals, w_vals)]
            fig.add_trace(go.Scatter(
                x=temp_vals,
                y=w_vals,
                mode='lines',
                line=dict(color=line_color, width=line_width),
                showlegend=False,  # Exclude from legend
                hoverinfo='text',
                hovertext=hover_text
            ))

    # =======================
    # Plot Saturation Curve (RH=100%)
    # =======================
    fig.add_trace(go.Scatter(
        x=temp,
        y=w_saturation,
        mode='lines',
        line=dict(color='black', width=2),
        name='Saturation (RH=100%)',
        showlegend=True,  # Include in legend
        hoverinfo='text',
        hovertext=[f'Saturation Curve<br>Temperature: {t:.1f}°C<br>Humidity Ratio: {w_sat:.3f} kg/kg'
                    for t, w_sat in zip(temp, w_saturation)]
    ))

    # =======================
    # Update Layout
    # =======================
    fig.update_layout(
        title='Psychrometric Chart',
        xaxis_title='Dry-Bulb Temperature (°C)',
        yaxis_title='Humidity Ratio (kg/kg)',
        legend_title='Lines',
        template='plotly_white',
        width=900,
        height=700,
        xaxis=dict(range=[temp_min, temp_max], showgrid=False),
        yaxis=dict(range=[0, max(w_saturation)*1.05], showgrid=False),
        hovermode='closest'
    )

    return fig


def get_psych_cart4_OLD():
    # Initialize psychrolib for SI units
    psychrolib.SetUnitSystem(psychrolib.SI)

    # Define chart parameters
    chart = dict()
    chart["pressure"] = 101325  # Atmospheric pressure in Pa
    chart["temp"] = np.arange(5, 45, 0.1)  # Dry-bulb temperature range (°C)
    chart["rh"] = np.arange(0, 1.1, 0.1)  # Relative Humidity (0 to 1)
    chart["enthalpy"] = np.arange(0, 120000, 10000)  # Enthalpy range (J/kg)
    chart["humidity_ratio"] = np.arange(
        0.005, 0.03, 0.005
    )  # Humidity ratio (kg/kg)
    chart["twb"] = np.arange(-10, 45, 5)  # Wet-bulb temperature range (°C)

    # Function to compute humidity ratio from relative humidity
    def compute_humidity_ratio(temp, rh, pressure):
        return psychrolib.GetHumRatioFromRelHum(temp, rh, pressure)

    # Compute RH lines
    rh_lines = {}
    for rh in chart["rh"]:
        if rh == 0:
            continue  # Skip RH=0 to avoid undefined humidity ratio
        w = [
            compute_humidity_ratio(t, rh, chart["pressure"])
            for t in chart["temp"]
        ]
        rh_lines[rh] = w

    # Create a Plotly figure
    fig = go.Figure()

    # Define a light grey color for grid lines
    grid_line_color = "#d3d3d3"  # Light grey
    grid_line_width = 1  # Thin lines

    # Plot RH lines
    for rh, w in rh_lines.items():
        fig.add_trace(
            go.Scatter(
                x=chart["temp"],
                y=w,
                mode="lines",
                name=f"RH = {int(rh*100)}%",  # This name will not appear in legend
                line=dict(
                    color=grid_line_color, width=grid_line_width),
                showlegend=False,  # Exclude RH lines from the legend
            )
        )

    # Function to compute enthalpy
    def compute_enthalpy(temp, w):
        # Enthalpy in kJ/kg
        return psychrolib.GetMoistAirEnthalpy(temp, w) / 1000

    # Plot Enthalpy lines
    for enthalpy in chart["enthalpy"]:
        temp_vals = []
        w_vals = []
        for w in chart["humidity_ratio"]:
            # Compute temperature for given enthalpy and humidity ratio
            try:
                temp = psychrolib.GetDryBulbFromEnthalpyAndHumRatio(
                    enthalpy * 1000, w, chart["pressure"]
                )
                temp_vals.append(temp)
                w_vals.append(w)
            except:
                continue  # Skip if no solution
        fig.add_trace(
            go.Scatter(
                x=temp_vals,
                y=w_vals,
                mode="lines",
                name=f"Enthalpy = {enthalpy} kJ/kg",
                line=dict(
                    color=grid_line_color, width=grid_line_width, dash="dot"
                ),
            )
        )

    # Function to compute wet-bulb temperature line
    def compute_wet_bulb(twb, pressure):
        w = [
            psychrolib.GetHumRatioFromTWetBulb(t, twb, pressure)
            for t in chart["temp"]
        ]
        return w

    # Plot Twb lines
    for twb in chart["twb"]:
        w = []
        for t in chart["temp"]:
            try:
                w_val = psychrolib.GetHumRatioFromTWetBulb(
                    t, twb, chart["pressure"]
                )
                w.append(w_val)
            except:
                w.append(None)
        fig.add_trace(
            go.Scatter(
                x=chart["temp"],
                y=w,
                mode="lines",
                name=f"Twb = {twb}°C",
                line=dict(
                    color=grid_line_color,
                    width=grid_line_width,
                    dash="dashdot",
                ),
            )
        )


    # Plot Humidity Ratio Lines (Constant w)
    for w in chart['humidity_ratio']:
        # Find the temperature where w_saturation >= w
        try:
            # Find the index where saturation humidity ratio >= current w
            idx = next(i for i, ws in enumerate(w_saturation) if ws >= w)
            # Define the temperature range up to saturation
            temp_range = chart['temp'][:idx+1]
            w_values = [w] * len(temp_range)

            fig.add_trace(go.Scatter(
                x=temp_range,
                y=w_values,
                mode='lines',
                name=f'w = {w:.3f} kg/kg',
                line=dict(color=line_color, width=line_width),
                showlegend=False  # Exclude from legend for a cleaner look
            ))
        except StopIteration:
            # If w is higher than any saturation humidity ratio, skip plotting
            continue

    # Plot Temperature Lines (Constant T)
    for t in chart['temp']:
        # Compute saturation humidity ratio at this temperature
        w_sat = psychrolib.GetHumRatioFromRelHum(t, 1.0, chart['pressure'])
        # Define humidity ratio range from 0 to saturation
        w_range = np.linspace(0, w_sat, 100)
        # Temperature is constant
        T_range = [t] * len(w_range)

        fig.add_trace(go.Scatter(
            x=T_range,
            y=w_range,
            mode='lines',
            name=f'T = {t:.1f}°C',
            line=dict(color=line_color, width=line_width),
            showlegend=False  # Exclude from legend for a cleaner look
        ))

    # # Optional: Add Saturation Curve (RH=100%) as a Distinct Line
    # fig.add_trace(go.Scatter(
    #     x=chart['temp'],
    #     y=w_saturation,
    #     mode='lines',
    #     name='Saturation (RH=100%)',
    #     line=dict(color='black', width=2),
    #     showlegend=True  # Include in legend
    # ))


    # Optional: Add the saturation curve (RH=100%) with a distinct color if desired
    # Uncomment the following lines to include the saturation curve
    """
    def compute_saturation_curve(temp, pressure):
        return psychrolib.GetHumRatioFromRelHum(temp, 1.0, pressure)

    w_sat = [compute_saturation_curve(t, chart['pressure']) for t in chart['temp']]
    fig.add_trace(go.Scatter(
        x=chart['temp'],
        y=w_sat,
        mode='lines',
        name='Saturation (RH=100%)',
        line=dict(color='black', width=2)
    ))
    """

    # Update layout
    fig.update_layout(
        title="Psychrometric Chart",
        xaxis_title="Dry-Bulb Temperature (°C)",
        yaxis_title="Humidity Ratio (kg/kg)",
        legend_title="Lines",
        template="plotly_white",
        width=800,
        height=600,
    )

    return fig


def get_psych_cart5(temp_min=5, temp_max=45, temp_step=0.5,
                    humidity_ratio_min=0.005, humidity_ratio_max=0.030, humidity_ratio_step=0.005,
                    enthalpy_min=10, enthalpy_max=120, enthalpy_step=10,
                    pressure=101325):
    """
    Generates an optimized psychrometric chart using Plotly and psychrolib.

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
    - pressure (float): Atmospheric pressure in Pascals.

    Returns:
    - fig (plotly.graph_objs.Figure): The psychrometric chart figure.
    """

    # Define temperature array
    temp = np.arange(temp_min, temp_max + temp_step, temp_step)

    # Define humidity ratio array
    humidity_ratio = np.arange(humidity_ratio_min, humidity_ratio_max + humidity_ratio_step, humidity_ratio_step)

    # Define enthalpy array
    enthalpy = np.arange(enthalpy_min, enthalpy_max + enthalpy_step, enthalpy_step)

    # Compute saturation humidity ratio for each temperature
    w_saturation = []
    for t in temp:
        try:
            w_sat = psychrolib.GetHumRatioFromRelHum(t, 1.0, pressure)
            w_saturation.append(w_sat)
        except:
            w_saturation.append(None)

    # Create a Plotly figure
    fig = go.Figure()

    # Define a lighter grey color for grid lines
    line_color = '#e0e0e0'  # Light grey
    line_width = 1  # Thin lines


    # Define a light grey color for grjjid lines
    # grid_line_color = "#d3d3d3"  # Light grey
    # grid_line_width = 1  # Thin lines

    # Plot RH lines
    for rh, w in rh_lines.items():
        fig.add_trace(
            go.Scatter(
                x=chart["temp"],
                y=w,
                mode="lines",
                name=f"RH = {int(rh*100)}%",  # This name will not appear in legend
                line=dict(
                    color=line_color, width=line_width),
                showlegend=False,  # Exclude RH lines from the legend
            )
        )



    # =======================
    # Plot Humidity Ratio Lines (Constant w)
    # =======================
    for w in humidity_ratio:
        # Find the first temperature where w <= w_sat(t)
        t_min = None
        for t_val, w_sat in zip(temp, w_saturation):
            if w <= w_sat:
                t_min = t_val
                break
        if t_min is not None:
            # Plot from t_min to temp_max
            temp_valid = temp[temp >= t_min]
            w_values = [w] * len(temp_valid)
            # Simplify hover information by limiting to key points
            hover_text = [f'Humidity Ratio: {w:.3f} kg/kg<br>Temperature: {t:.1f}°C' for t in temp_valid]
            fig.add_trace(go.Scatter(
                x=temp_valid,
                y=w_values,
                mode='lines',
                line=dict(color=line_color, width=line_width),
                showlegend=False,  # Exclude from legend
                hoverinfo='text',
                hovertext=hover_text
            ))

    # =======================
    # Plot Temperature Lines (Constant T)
    # =======================
    for t in temp:
        try:
            # Compute saturation humidity ratio at this temperature
            w_sat = psychrolib.GetHumRatioFromRelHum(t, 1.0, pressure)
            # Define humidity ratio range from 0 to saturation
            w_range = np.linspace(0, w_sat, 50)  # Reduced points for performance
            # Temperature is constant
            T_range = [t] * len(w_range)

            # Simplify hover information by limiting to key points
            hover_text = [f'Temperature: {t:.1f}°C<br>Humidity Ratio: {w:.3f} kg/kg' for w in w_range]

            fig.add_trace(go.Scatter(
                x=T_range,
                y=w_range,
                mode='lines',
                line=dict(color=line_color, width=line_width),
                showlegend=False,  # Exclude from legend
                hoverinfo='text',
                hovertext=hover_text
            ))
        except:
            continue  # Skip if calculation fails

    # =======================
    # Plot Enthalpy Lines (Constant h)
    # =======================
    for h in enthalpy:
        temp_vals = []
        w_vals = []
        # Define a range of humidity ratios for enthalpy calculation
        w_enthalpy = np.linspace(humidity_ratio_min, humidity_ratio_max, 50)  # Reduced points for performance
        for w in w_enthalpy:
            try:
                # Compute dry-bulb temperature for given enthalpy and humidity ratio
                # Enthalpy in J/kg (kJ/kg to J/kg)
                t = psychrolib.GetDryBulbFromEnthalpyAndHumRatio(h * 1000, w, pressure)
                # Check if temperature is within the defined range and below saturation
                if temp_min <= t <= temp_max:
                    w_sat = psychrolib.GetHumRatioFromRelHum(t, 1.0, pressure)
                    if w <= w_sat:
                        temp_vals.append(t)
                        w_vals.append(w)
            except:
                continue  # Skip if no solution

        if temp_vals and w_vals:
            hover_text = [f'Enthalpy: {h} kJ/kg<br>Temperature: {t:.1f}°C<br>Humidity Ratio: {w:.3f} kg/kg'
                            for t, w in zip(temp_vals, w_vals)]
            fig.add_trace(go.Scatter(
                x=temp_vals,
                y=w_vals,
                mode='lines',
                line=dict(color=line_color, width=line_width),
                showlegend=False,  # Exclude from legend
                hoverinfo='text',
                hovertext=hover_text
            ))



    if 0:
        # =======================
        # Plot Saturation Curve (RH=100%)
        # =======================
        fig.add_trace(go.Scatter(
            x=temp,
            y=w_saturation,
            mode='lines',
            line=dict(color='black', width=2),
            name='Saturation (RH=100%)',
            showlegend=True,  # Include in legend
            hoverinfo='text',
            hovertext=[f'Saturation Curve<br>Temperature: {t:.1f}°C<br>Humidity Ratio: {w_sat:.3f} kg/kg'
                        for t, w_sat in zip(temp, w_saturation)]
        ))


    # =======================
    # Update Layout
    # =======================
    fig.update_layout(
        title='Psychrometric Chart',
        xaxis_title='Dry-Bulb Temperature (°C)',
        yaxis_title='Humidity Ratio (kg/kg)',
        legend_title='Lines',
        template='plotly_white',
        width=900,
        height=700,
        xaxis=dict(range=[temp_min, temp_max], showgrid=False),
        yaxis=dict(range=[0, max(w_saturation)*1.05], showgrid=False, side='right'),
        hovermode='closest'
    )

    return fig
