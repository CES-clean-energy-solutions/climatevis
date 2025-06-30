try:
    import marimo as mo
    _HAS_MARIMO = True
except ImportError:
    _HAS_MARIMO = False
    mo = None

import pathlib
from pathlib import Path
import glob

####################################
# Base weather files
####################################
dict_weather_select = {
    "NEOM L3": "./Data/Weather data NEOM/NEOM_L3.epw",
    "ASHRAE Sharm El Sheikh": "./Data/Weather data ASHRAE/EGY_JS_Sharm.Sheikh.Intl.AP.624639_TMYx.epw",
    # "AQABA Mast 1 Wind": "./Data/AQABA wind/AQABA_MAST_1.epw",
    "AQABA MAST 1 Wind Temp RH Pressure": "./Data/AQABA wind/AQABA_MAST_1_WIND_TEMP_RH_PRES.epw"

    }

####################################
# Climate change weather files
####################################
climate_change_file_dict = {
    "Sharm El Sheikh RCP 2.6 2050": "./Data/Climate Change/Sharm_El_Sheikh_Airp_-hour-RCP2.6-2050.epw",
    "Sharm El Sheikh RCP 2.6 2100": "./Data/Climate Change/Sharm_El_Sheikh_Airp_-hour-RCP2.6-2100.epw",
    "Sharm El Sheikh RCP 4.5 2050": "./Data/Climate Change/Sharm_El_Sheikh_Airp_-hour-RCP4.5-2050.epw",
    "Sharm El Sheikh RCP 4.5 2100": "./Data/Climate Change/Sharm_El_Sheikh_Airp_-hour-RCP4.5-2100.epw",
    "Sharm El Sheikh RCP 8.5 2050": "./Data/Climate Change/Sharm_El_Sheikh_Airp_-hour-RCP8.5-2050EPW.epw",
    "Sharm El Sheikh RCP 8.5 2100": "./Data/Climate Change/Sharm_El_Sheikh_Airp_-hour-RCP8.5-2100EPW.epw"
}

dict_weather_select.update(climate_change_file_dict)

####################################
# Public Realm weather files
####################################
public_realm_weather_files = glob.glob("./Data/Public Realm/*.epw")
public_realm_weather_dicts = {Path(epw_path).stem: epw_path for epw_path in public_realm_weather_files}
dict_weather_select.update(public_realm_weather_dicts)


####################################
# WRF FD Global EPW weather files
####################################
wrf_files = glob.glob("./Data/WRF FD Global EPW/*.epw")
wrf_file_path_dicts = {Path(epw_path).stem: epw_path for epw_path in wrf_files}
dict_weather_select.update(wrf_file_path_dicts)

####################################
# ASHRAE Benchmark city weather files
####################################
additional_files = glob.glob("./Data/Additional cities weather/*.epw")
additional_file_path_dicts = {Path(epw_path).stem: epw_path for epw_path in additional_files}
dict_weather_select.update(additional_file_path_dicts)

def weather_selection():
    """Creates a dropdown for selecting a weather file."""

    if not _HAS_MARIMO:
        raise ImportError("marimo is required for weather_selection component. Install with: pip install marimo")

    # Create dropdown
    dropdown = mo.ui.dropdown(
        options=dict_weather_select,
        value="NEOM L3",
    )

    return dropdown

# def weather_selection(options, label_text, default_value=None):
#     """Creates a VStack with a dropdown, label, and text input."""

#     # Create UI elements
#     dropdown = mo.ui.dropdown(
#         options=options,
#         value=default_value or options[0],
#         label=label_text
#     )
#     text_input = mo.ui.text(
#         placeholder="Enter text"
#     )

#     # Combine UI elements into a vertical stack
#     vstack = mo.vstack([mo.md(f"**{label_text}**"), dropdown, text_input])

#     return vstack, dropdown, text_input