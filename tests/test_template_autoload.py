"""
Test module for template auto-loading and UI component functionality.

This module tests:
1. Auto-loading of templates during package import
2. Template discovery functions
3. UI component creation (if marimo is available)
"""

import pytest
import plotly.io as pio


class TestTemplateAutoLoading:
    """Test automatic template loading functionality."""

    def test_templates_auto_loaded_on_import(self):
        """Test that templates are automatically loaded when climatevis is imported."""
        # Import should trigger auto-loading
        import climatevis

        # Check that templates are loaded
        available_templates = climatevis.get_available_templates()
        assert len(available_templates) > 0

        # Check specific templates exist
        assert 'base' in available_templates
        assert 'base_autosize' in available_templates
        assert 'test' in available_templates

    def test_templates_registered_in_plotly(self):
        """Test that auto-loaded templates are properly registered with Plotly."""
        import climatevis

        # Check templates are registered in Plotly
        loaded_templates = climatevis.get_loaded_template_names()
        assert 'base' in loaded_templates
        assert 'base_autosize' in loaded_templates
        assert 'test' in loaded_templates

        # Check templates can be accessed via Plotly
        assert 'base' in pio.templates
        assert 'base_autosize' in pio.templates
        assert 'test' in pio.templates

    def test_get_available_templates_function(self):
        """Test the get_available_templates function."""
        import climatevis

        templates = climatevis.get_available_templates()
        assert isinstance(templates, list)
        assert len(templates) >= 3  # At least our built-in templates
        assert all(isinstance(name, str) for name in templates)

    def test_get_builtin_template_names_function(self):
        """Test the get_builtin_template_names function."""
        import climatevis

        builtin_templates = climatevis.get_builtin_template_names()
        assert isinstance(builtin_templates, list)
        assert 'base' in builtin_templates
        assert 'base_autosize' in builtin_templates
        assert 'test' in builtin_templates

    def test_load_all_builtin_templates_function(self):
        """Test the load_all_builtin_templates function."""
        import climatevis

        # This should work even if called multiple times
        loaded = climatevis.load_all_builtin_templates()
        assert isinstance(loaded, dict)
        assert 'base' in loaded
        assert 'base_autosize' in loaded
        assert 'test' in loaded


class TestTemplateUIComponents:
    """Test template UI component functionality."""

    def test_template_dropdown_creation_without_marimo(self):
        """Test that template dropdown gracefully handles missing marimo."""
        import climatevis

        # Get template options should work without marimo
        options = climatevis.get_template_options()
        assert isinstance(options, list)
        assert len(options) > 0

    def test_paper_size_options_function(self):
        """Test the get_paper_size_options function."""
        import climatevis

        paper_sizes = climatevis.get_paper_size_options()
        assert isinstance(paper_sizes, list)
        assert 'A4_LANDSCAPE' in paper_sizes
        assert 'A4_PORTRAIT' in paper_sizes
        assert 'A5_LANDSCAPE' in paper_sizes

    @pytest.mark.skipif(
        not pytest.importorskip("marimo", reason="marimo not available"),
        reason="marimo not available"
    )
    def test_create_template_dropdown_with_marimo(self):
        """Test template dropdown creation when marimo is available."""
        import climatevis

        try:
            dropdown = climatevis.create_template_dropdown()
            # If marimo is available, this should create a dropdown
            assert dropdown is not None
            # Check that it has the expected interface
            assert hasattr(dropdown, 'value')
        except ImportError:
            pytest.skip("marimo not available")

    @pytest.mark.skipif(
        not pytest.importorskip("marimo", reason="marimo not available"),
        reason="marimo not available"
    )
    def test_create_paper_size_dropdown_with_marimo(self):
        """Test paper size dropdown creation when marimo is available."""
        import climatevis

        try:
            dropdown = climatevis.create_paper_size_dropdown()
            # If marimo is available, this should create a dropdown
            assert dropdown is not None
            # Check that it has the expected interface
            assert hasattr(dropdown, 'value')
        except ImportError:
            pytest.skip("marimo not available")


class TestTemplateIntegration:
    """Test integration between auto-loaded templates and plotting functions."""

    def test_plot_with_auto_loaded_template(self):
        """Test that plotting functions work with auto-loaded templates."""
        import climatevis
        import pandas as pd
        import numpy as np

        # Create test data
        dates = pd.date_range('2023-01-01', periods=100, freq='h')
        values = np.random.normal(0, 1, 100)
        series = pd.Series(values, index=dates, name="Test Data")
        series.attrs["unit"] = "unit"

        # This should work without manually loading templates
        fig = climatevis.plot_series(
            [series],
            template_name='base',  # Auto-loaded template
            paper_size='A4_LANDSCAPE'
        )

        assert fig is not None

        # Test with other auto-loaded templates
        fig2 = climatevis.plot_series(
            [series],
            template_name='base_autosize',
            paper_size='A4_LANDSCAPE'
        )

        assert fig2 is not None

    def test_no_template_registration_error(self):
        """Test that we don't get template registration errors after import."""
        import climatevis
        import pandas as pd
        import numpy as np

        # Create test data
        dates = pd.date_range('2023-01-01', periods=10, freq='h')
        values = np.random.normal(0, 1, 10)
        series = pd.Series(values, index=dates, name="Test Data")
        series.attrs["unit"] = "unit"

        # This should NOT raise "Template 'base' is not registered" error
        try:
            fig = climatevis.plot_series([series], template_name='base')
            assert fig is not None
        except ValueError as e:
            if "not registered" in str(e):
                pytest.fail(f"Template registration error occurred: {e}")
            else:
                raise  # Re-raise if it's a different ValueError


class TestBackwardCompatibility:
    """Test that existing functionality still works."""

    def test_manual_template_loading_still_works(self):
        """Test that manual template loading functions still work."""
        import climatevis

        # Manual loading should still work
        template_data = climatevis.util_plotly.load_builtin_template('base', 'manual_base')
        assert isinstance(template_data, dict)
        assert 'layout' in template_data

        # Should be registered
        loaded_templates = climatevis.get_loaded_template_names()
        assert 'manual_base' in loaded_templates

    def test_existing_plot_functions_unchanged(self):
        """Test that existing plot function signatures are unchanged."""
        import climatevis
        import pandas as pd
        import numpy as np

        # Create test data
        dates = pd.date_range('2023-01-01', periods=50, freq='h')
        values = np.random.normal(20, 5, 50)
        series = pd.Series(values, index=dates, name="Temperature")
        series.attrs["unit"] = "°C"

        # Original function signature should still work
        fig = climatevis.plot_series(
            series_list=[series],
            template_name='base',
            paper_size='A4_LANDSCAPE',
            y1_axis_title="Temperature",
            mode="line",
            show_days=False
        )

        assert fig is not None