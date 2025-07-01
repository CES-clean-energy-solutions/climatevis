"""
Template UI Components for ClimateVis

Provides marimo UI components for template selection and management.
"""

try:
    import marimo as mo
    _HAS_MARIMO = True
except ImportError:
    _HAS_MARIMO = False
    mo = None

def create_template_dropdown(value="base", label="Chart Template", **kwargs):
    """
    Create a marimo dropdown pre-configured with all available templates.

    Parameters:
        value (str): Default selected template name. Defaults to "base".
        label (str): Label for the dropdown. Defaults to "Chart Template".
        **kwargs: Additional keyword arguments passed to mo.ui.dropdown().

    Returns:
        mo.ui.dropdown: Configured dropdown component with template options.

    Raises:
        ImportError: If marimo is not available.
        ImportError: If climatevis template functions are not available.
    """
    if not _HAS_MARIMO:
        raise ImportError("marimo is required to use template UI components. Install with: pip install marimo")

    try:
        from climatevis.util.util_plotly import get_available_templates
    except ImportError:
        raise ImportError("climatevis template functions not available. Check installation.")

    # Get available templates
    template_options = get_available_templates()

    if not template_options:
        # Fallback to known templates if auto-loading failed
        template_options = ["base", "base_autosize", "test"]

    # Ensure the default value is in the options
    if value not in template_options and template_options:
        value = template_options[0]

    return mo.ui.dropdown(
        options=template_options,
        value=value,
        label=label,
        **kwargs
    )

def create_paper_size_dropdown(value="A4_LANDSCAPE", label="Paper Size", **kwargs):
    """
    Create a marimo dropdown pre-configured with available paper sizes.

    Parameters:
        value (str): Default selected paper size. Defaults to "A4_LANDSCAPE".
        label (str): Label for the dropdown. Defaults to "Paper Size".
        **kwargs: Additional keyword arguments passed to mo.ui.dropdown().

    Returns:
        mo.ui.dropdown: Configured dropdown component with paper size options.

    Raises:
        ImportError: If marimo is not available.
    """
    if not _HAS_MARIMO:
        raise ImportError("marimo is required to use template UI components. Install with: pip install marimo")

    # Standard paper sizes available in climatevis
    paper_size_options = [
        "A4_LANDSCAPE", "A4_PORTRAIT",
        "A5_LANDSCAPE", "A5_PORTRAIT",
        "A3_LANDSCAPE", "A3_PORTRAIT",
        "A6_LANDSCAPE", "A6_PORTRAIT"
    ]

    return mo.ui.dropdown(
        options=paper_size_options,
        value=value,
        label=label,
        **kwargs
    )

def get_template_options():
    """
    Get the list of available template options for manual dropdown creation.

    Returns:
        list: List of available template names.
    """
    try:
        from climatevis.util.util_plotly import get_available_templates
        return get_available_templates()
    except ImportError:
        # Fallback to known templates
        return ["base", "base_autosize", "test"]

def get_paper_size_options():
    """
    Get the list of available paper size options.

    Returns:
        list: List of available paper size names.
    """
    return [
        "A4_LANDSCAPE", "A4_PORTRAIT",
        "A5_LANDSCAPE", "A5_PORTRAIT",
        "A3_LANDSCAPE", "A3_PORTRAIT",
        "A6_LANDSCAPE", "A6_PORTRAIT"
    ]