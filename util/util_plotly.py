import yaml
import logging
import plotly.io as pio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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

def load_plotly_template(yaml_file_path, template_name):
    """
    Load a Plotly template from a YAML file and register it with Plotly.

    Parameters:
        yaml_file_path (str): Path to the YAML file containing the template.
        template_name (str): Name to register the template under in Plotly.

    Returns:
        dict: The loaded template.
    """
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