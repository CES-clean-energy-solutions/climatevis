import yaml
import logging
import plotly.io as pio

# Import for package resource loading
try:
    from importlib.resources import files
except ImportError:
    # Fallback for Python < 3.9
    try:
        from importlib_resources import files
    except ImportError:
        # Fallback to pkg_resources
        import pkg_resources
        files = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Built-in template mapping - single source of truth
BUILTIN_TEMPLATES = {
    'base': 'plotly_template_base.yaml',
    'base_autosize': 'plotly_template_base_autosize.yaml',
    'test': 'plotly_template_test.yaml'
}

# Predefined paper sizes
PAPER_SIZES = {
    "A6_LANDSCAPE": {"width": 559, "height": 397},
    "A6_PORTRAIT": {"width": 397, "height": 559},

    "A5_LANDSCAPE": {"width": 794, "height": 560},
    "A5_PORTRAIT": {"width": 560, "height": 794},

    "A4_LANDSCAPE": {"width": 1123, "height": 794},
    "A4_PORTRAIT": {"width": 794, "height": 1123},

    "A3_LANDSCAPE": {"width": 1587, "height": 1123},
    "A3_PORTRAIT": {"width": 1123, "height": 1587},

    "A2_LANDSCAPE": {"width": 2245, "height": 1587},
    "A2_PORTRAIT": {"width": 1587, "height": 2245},

    "A1_LANDSCAPE": {"width": 3175, "height": 2245},
    "A1_PORTRAIT": {"width": 2245, "height": 3175},

    "A0_LANDSCAPE": {"width": 4494, "height": 3175},
    "A0_PORTRAIT": {"width": 3175, "height": 4494}
}

def load_plotly_template_from_package(template_filename, template_name):
    """
    Load a Plotly template from a package template file and register it with Plotly.

    Parameters:
        template_filename (str): Filename of the template in the climatevis.templates package.
        template_name (str): Name to register the template under in Plotly.

    Returns:
        dict: The loaded template.
    """
    try:
        # Load template from package data
        if files is not None:
            # Use importlib.resources (Python 3.9+) or importlib_resources
            try:
                templates_dir = files('climatevis.templates')
                if templates_dir is None:
                    raise ValueError("Could not locate climatevis.templates package directory")

                template_path = templates_dir / template_filename
                if template_path is None:
                    raise ValueError(f"Could not locate template file: {template_filename}")

                with template_path.open('r', encoding='utf-8') as file:
                    template = yaml.safe_load(file)
            except Exception as e:
                logging.error(f"Failed to load template via importlib.resources: {e}")
                logging.info("Trying alternative importlib.resources approach")
                # Try alternative approach - templates as package data
                try:
                    climatevis_files = files('climatevis')
                    template_path = climatevis_files / 'templates' / template_filename
                    with template_path.open('r', encoding='utf-8') as file:
                        template = yaml.safe_load(file)
                except Exception as e2:
                    logging.error(f"Alternative importlib.resources approach failed: {e2}")
                    logging.info("Falling back to pkg_resources method")
                    # Fallback to pkg_resources
                    try:
                        template_content = pkg_resources.resource_string(
                            'climatevis.templates', template_filename
                        ).decode('utf-8')
                        template = yaml.safe_load(template_content)
                    except Exception as e3:
                        logging.error(f"pkg_resources with climatevis.templates failed: {e3}")
                        logging.info("Trying pkg_resources with climatevis package")
                        # Final fallback - try as package data
                        template_content = pkg_resources.resource_string(
                            'climatevis', f'templates/{template_filename}'
                        ).decode('utf-8')
                        template = yaml.safe_load(template_content)
        else:
            # Fallback to pkg_resources
            try:
                template_content = pkg_resources.resource_string(
                    'climatevis.templates', template_filename
                ).decode('utf-8')
                template = yaml.safe_load(template_content)
            except Exception as e:
                logging.error(f"pkg_resources with climatevis.templates failed: {e}")
                logging.info("Trying pkg_resources with climatevis package")
                # Final fallback - try as package data
                template_content = pkg_resources.resource_string(
                    'climatevis', f'templates/{template_filename}'
                ).decode('utf-8')
                template = yaml.safe_load(template_content)

        # Register the template with Plotly
        pio.templates[template_name] = template
        logging.info(f"Template '{template_name}' successfully loaded from package and registered.")

        return template

    except Exception as e:
        logging.error(f"Failed to load template from package: {e}")
        logging.error(f"Template filename: {template_filename}")
        logging.error(f"Template name: {template_name}")
        logging.error(f"Files module available: {files is not None}")
        raise

def load_plotly_template(yaml_file_path, template_name):
    """
    Load a Plotly template from a YAML file and register it with Plotly.

    This function now supports both file paths and package template names.
    If yaml_file_path is one of the built-in template names, it loads from package data.

    Parameters:
        yaml_file_path (str): Path to the YAML file or built-in template name
                            ('base', 'base_autosize', 'test').
        template_name (str): Name to register the template under in Plotly.

    Returns:
        dict: The loaded template.
    """
    # Check if it's a built-in template name
    if yaml_file_path in BUILTIN_TEMPLATES:
        return load_plotly_template_from_package(BUILTIN_TEMPLATES[yaml_file_path], template_name)

    # Otherwise, treat as file path (backward compatibility)
    try:
        # Load the YAML file
        with open(yaml_file_path, "r") as file:
            template = yaml.safe_load(file)

        # Register the template with Plotly
        pio.templates[template_name] = template
        logging.info(f"Template '{template_name}' successfully loaded and registered.")

        # Log a summary of the template
        # summarize_template(template, template_name)

        return template

    except Exception as e:
        logging.error(f"Failed to load template: {e}")
        raise

def load_builtin_template(template_name, register_as=None):
    """
    Convenience function to load a built-in template from the package.

    Parameters:
        template_name (str): Name of the built-in template
                           ('base', 'base_autosize', 'test').
        register_as (str, optional): Custom name to register template under.
                                   If None, uses template_name.

    Returns:
        dict: The loaded template.
    """
    if register_as is None:
        register_as = template_name

    return load_plotly_template(template_name, register_as)

def get_builtin_template_names():
    """
    Get a list of all available built-in template names.

    Returns:
        list: List of built-in template names.
    """
    return list(BUILTIN_TEMPLATES.keys())

def get_loaded_template_names():
    """
    Get a list of all currently loaded/registered template names.

    Returns:
        list: List of loaded template names.
    """
    return list(pio.templates.keys())

def load_all_builtin_templates():
    """
    Load all built-in templates and register them with their default names.
    This function is called automatically when the package is imported.

    Returns:
        dict: Dictionary mapping template names to loaded template data.
    """
    loaded_templates = {}
    builtin_names = get_builtin_template_names()

    for template_name in builtin_names:
        try:
            template_data = load_builtin_template(template_name)
            loaded_templates[template_name] = template_data
            logging.info(f"Auto-loaded template '{template_name}'")
        except Exception as e:
            logging.error(f"Failed to auto-load template '{template_name}': {e}")

    return loaded_templates

def get_available_templates():
    """
    Get a list of all available template names (both built-in and any custom loaded ones).
    This is useful for UI components like dropdowns.

    Returns:
        list: Sorted list of available template names.
    """
    # Get built-in templates
    builtin = get_builtin_template_names()

    # Get any other loaded templates that might not be built-in
    loaded = get_loaded_template_names()

    # Combine and remove duplicates, then sort
    all_templates = sorted(set(builtin + loaded))

    return all_templates

def summarize_template(template, template_name):
    """
    Log a summary of the loaded template.

    Parameters:
        template (dict): The loaded Plotly template.
        template_name (str): Name of the template.
    """
    logging.info(f"Summary of template '{template_name}':")

    # Summarize layout properties
    if "layout" in template:
        layout_keys = list(template["layout"].keys())
        logging.info(f"  Layout keys: {layout_keys}")

        # Example: Log specific layout properties
        if "font" in template["layout"]:
            logging.info(f"  Font settings: {template['layout']['font']}")
        if "xaxis" in template["layout"]:
            logging.info(f"  X-axis settings: {template['layout']['xaxis']}")
        if "yaxis" in template["layout"]:
            logging.info(f"  Y-axis settings: {template['layout']['yaxis']}")

    # # Summarize data properties
    # if "data" in template:
    #     data_keys = list(template["data"].keys())
    #     logging.info(f"  Data keys (trace types): {data_keys}")

def apply_template_to_figure(fig, template_name, paper_size=None):
    """
    Apply a registered Plotly template to a figure and optionally set the paper size.

    If the template has `autosize=True`, the paper size is ignored.

    Parameters:
        fig (plotly.graph_objects.Figure): The Plotly figure object.
        template_name (str): The name of the registered template to apply.
        paper_size (str, optional): Predefined paper size (e.g., 'A5_LANDSCAPE', 'A4_LANDSCAPE').

    Returns:
        plotly.graph_objects.Figure: The updated figure with the template and paper size applied.
    """
    if template_name not in pio.templates:
        logging.error(f"Template '{template_name}' is not registered.")
        raise ValueError(f"Template '{template_name}' is not registered. Please load it first.")

    # Apply the template
    fig.update_layout(template=template_name)
    logging.info(f"Template '{template_name}' applied to figure.")

    # Check if the template has autosize enabled
    template = pio.templates[template_name]
    # is_autosize_enabled = template.get("layout", {}).get("autosize", False)

    if template['layout']['autosize']:
        logging.info(f"Template '{template_name}' has autosize enabled. Ignoring paper size setting.")
    elif paper_size:
        if paper_size not in PAPER_SIZES:
            logging.error(f"Invalid paper size '{paper_size}'. Available sizes: {list(PAPER_SIZES.keys())}")
            raise ValueError(f"Invalid paper size '{paper_size}'.")
        paper_dimensions = PAPER_SIZES[paper_size]
        fig.update_layout(**paper_dimensions)
        logging.info(f"Paper size '{paper_size}' applied: width={paper_dimensions['width']}, height={paper_dimensions['height']}.")

    return fig