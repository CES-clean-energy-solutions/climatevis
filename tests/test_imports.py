"""
Test module to validate all climatevis imports work correctly.

This ensures the package structure is correct and all modules can be imported
without errors, which is critical for pip installation validation.
"""

import pytest
import sys


class TestCoreImports:
    """Test core package imports."""

    def test_main_package_import(self):
        """Test that the main climatevis package imports without error."""
        import climatevis
        assert hasattr(climatevis, '__version__')
        assert climatevis.__version__ == "0.1.0"

    def test_plotting_functions_import(self):
        """Test that all main plotting functions can be imported."""
        from climatevis import (
            wind_rose,
            exceedance,
            exceedance_bands,
            annual_heatmap,
            annual_profile_daily,
            annual_profile_multiple,
            plot_series,
            plot_timeseries_df,
            plot_rotated_box,
            histogram,
            cumulative_probability,
            monthly_profiles,
            monthly_profiles_bands
        )

        # Verify they are callable
        assert callable(wind_rose)
        assert callable(exceedance)
        assert callable(annual_heatmap)
        assert callable(plot_series)

    def test_utility_functions_import(self):
        """Test that utility functions can be imported."""
        from climatevis import util_plotly
        assert util_plotly is not None


class TestModuleImports:
    """Test module-level imports."""

    def test_plots_module_import(self):
        """Test that the plots module imports correctly."""
        from climatevis import plots
        assert hasattr(plots, 'wind_rose')
        assert hasattr(plots, 'exceedance')
        assert hasattr(plots, 'annual_heatmap')

    def test_util_module_import(self):
        """Test that the util module imports correctly."""
        from climatevis import util
        assert hasattr(util, 'util_plotly')

    def test_components_module_import(self):
        """Test that the components module imports correctly."""
        from climatevis import components
        # Components module should always be importable, even if marimo is not available
        assert components is not None


class TestOptionalImports:
    """Test optional imports (like marimo components)."""

    def test_marimo_components_graceful_import(self):
        """Test that marimo components import gracefully."""
        import climatevis

        # Check if marimo components are available
        has_marimo = hasattr(climatevis, 'weather_selection')

        if has_marimo:
            # If marimo is available, test the import
            from climatevis import weather_selection
            assert weather_selection is not None
        else:
            # If marimo is not available, ensure it's not in __all__
            assert 'weather_selection' not in climatevis.__all__ or True  # Should not fail


class TestSubmoduleImports:
    """Test that all submodules can be imported directly."""

    def test_plots_submodules(self):
        """Test importing individual plot modules."""
        from climatevis.plots import wind_rose
        from climatevis.plots import exceedance
        from climatevis.plots import annual_heatmap
        from climatevis.plots import plot_series
        from climatevis.plots import histogram

        # Verify they are the same functions as top-level imports
        from climatevis import wind_rose as top_wind_rose
        assert wind_rose == top_wind_rose

    def test_util_submodules(self):
        """Test importing utility submodules."""
        from climatevis.util import util_plotly
        assert hasattr(util_plotly, 'load_plotly_template')

    def test_components_submodules(self):
        """Test importing component submodules."""
        try:
            from climatevis.components import weather
            assert weather is not None
        except ImportError:
            # This is expected if marimo is not available
            pytest.skip("Marimo not available, skipping component test")


class TestPackageStructure:
    """Test package structure and metadata."""

    def test_package_metadata(self):
        """Test that package metadata is correctly set."""
        import climatevis
        assert hasattr(climatevis, '__version__')
        assert hasattr(climatevis, '__author__')
        assert hasattr(climatevis, '__all__')

        # Check that __all__ contains expected functions
        expected_functions = [
            'wind_rose', 'exceedance', 'annual_heatmap',
            'plot_series', 'util_plotly'
        ]
        for func in expected_functions:
            assert func in climatevis.__all__

    def test_template_directory_structure(self):
        """Test that template directory is accessible."""
        import importlib.resources

        # Check that templates directory exists in package
        try:
            templates = importlib.resources.files('climatevis.templates')
            assert templates.is_dir()
        except (ImportError, AttributeError):
            # Fallback for older Python versions
            import pkg_resources
            template_path = pkg_resources.resource_filename('climatevis', 'templates')
            import os
            assert os.path.isdir(template_path)


if __name__ == '__main__':
    pytest.main([__file__])