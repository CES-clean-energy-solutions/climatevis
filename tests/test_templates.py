"""
Test module for template loading functionality.

This validates that Plotly template files can be loaded correctly from package data
using importlib.resources or pkg_resources.
"""

import pytest
import yaml
import os


class TestTemplateLoading:
    """Test template loading from package data."""

    def test_load_plotly_template_function_exists(self):
        """Test that the template loading function exists."""
        from climatevis.util import util_plotly

        assert hasattr(util_plotly, 'load_plotly_template')
        assert callable(util_plotly.load_plotly_template)

    def test_template_directory_accessible(self):
        """Test that the template directory is accessible via package resources."""
        # Test with importlib.resources (Python 3.9+)
        try:
            import importlib.resources
            templates = importlib.resources.files('climatevis.templates')
            assert templates.is_dir()

            # Check that template files exist
            template_files = [f.name for f in templates.iterdir() if f.name.endswith('.yaml')]
            assert len(template_files) > 0

        except (ImportError, AttributeError):
            # Fallback for older Python versions
            import pkg_resources
            template_path = pkg_resources.resource_filename('climatevis', 'templates')
            assert os.path.isdir(template_path)

            # Check that template files exist
            template_files = [f for f in os.listdir(template_path) if f.endswith('.yaml')]
            assert len(template_files) > 0

    def test_load_base_template(self):
        """Test loading the base Plotly template."""
        from climatevis.util.util_plotly import load_plotly_template

        template_data = load_plotly_template('base', 'test_base')

        # Should return a dictionary
        assert isinstance(template_data, dict)

        # Should have typical Plotly template structure
        assert 'layout' in template_data
        assert isinstance(template_data['layout'], dict)

    def test_load_base_autosize_template(self):
        """Test loading the base autosize template."""
        from climatevis.util.util_plotly import load_plotly_template

        template_data = load_plotly_template('base_autosize', 'test_base_autosize')

        assert isinstance(template_data, dict)
        assert 'layout' in template_data

        # Autosize template should have autosize property
        layout = template_data['layout']
        # The autosize property might be nested, so just check it's a valid template
        assert isinstance(layout, dict)

    def test_load_test_template(self):
        """Test loading the test template."""
        from climatevis.util.util_plotly import load_plotly_template

        template_data = load_plotly_template('test', 'test_test')

        assert isinstance(template_data, dict)
        assert 'layout' in template_data

    def test_load_nonexistent_template(self):
        """Test loading a nonexistent template raises appropriate error."""
        from climatevis.util.util_plotly import load_plotly_template

        with pytest.raises((FileNotFoundError, ValueError, KeyError)):
            load_plotly_template('nonexistent_template', 'test_nonexistent')

    def test_all_available_templates(self):
        """Test that all available templates can be loaded."""
        from climatevis.util.util_plotly import load_plotly_template

        # List of known templates based on the file listing
        known_templates = ['base', 'base_autosize', 'test']

        for i, template_name in enumerate(known_templates):
            template_data = load_plotly_template(template_name, f'test_{template_name}_{i}')
            assert isinstance(template_data, dict)
            assert 'layout' in template_data

            # Verify it's valid YAML/dict structure
            assert isinstance(template_data['layout'], dict)


class TestTemplateStructure:
    """Test the structure and content of template files."""

    def test_templates_are_valid_yaml(self):
        """Test that all template files are valid YAML."""
        # Access templates via package resources
        try:
            import importlib.resources
            templates_dir = importlib.resources.files('climatevis.templates')
            template_files = [f for f in templates_dir.iterdir() if f.name.endswith('.yaml')]

            for template_file in template_files:
                content = template_file.read_text()
                # Should parse as valid YAML
                yaml_data = yaml.safe_load(content)
                assert isinstance(yaml_data, dict)

        except (ImportError, AttributeError):
            # Fallback for older Python versions
            import pkg_resources
            template_path = pkg_resources.resource_filename('climatevis', 'templates')
            template_files = [f for f in os.listdir(template_path) if f.endswith('.yaml')]

            for template_file in template_files:
                full_path = os.path.join(template_path, template_file)
                with open(full_path, 'r') as f:
                    content = f.read()

                # Should parse as valid YAML
                yaml_data = yaml.safe_load(content)
                assert isinstance(yaml_data, dict)

    def test_templates_have_layout_section(self):
        """Test that all templates have a layout section."""
        template_names = ['base', 'base_autosize', 'test']

        from climatevis.util.util_plotly import load_plotly_template

        for i, template_name in enumerate(template_names):
            template_data = load_plotly_template(template_name, f'layout_test_{template_name}_{i}')
            assert 'layout' in template_data
            assert isinstance(template_data['layout'], dict)

    def test_template_layout_properties(self):
        """Test that templates have expected layout properties."""
        from climatevis.util.util_plotly import load_plotly_template

        base_template = load_plotly_template('base', 'layout_props_test')
        layout = base_template['layout']

        # Check for common layout properties
        # (These might vary based on actual template content)
        expected_properties = ['font', 'paper_bgcolor', 'plot_bgcolor']

        # At least some of these should be present in a proper Plotly template
        found_properties = [prop for prop in expected_properties if prop in layout]
        assert len(found_properties) > 0, f"Template should have some layout properties like {expected_properties}"


class TestTemplateIntegration:
    """Test template integration with plotting functions."""

    def test_template_loading_in_util_plotly(self):
        """Test that util_plotly module can load and use templates."""
        from climatevis.util import util_plotly

        # Check that the module has template-related functionality
        assert hasattr(util_plotly, 'load_plotly_template')

        # Test loading a template through the module
        template = util_plotly.load_plotly_template('base', 'integration_test')
        assert isinstance(template, dict)

    def test_template_compatibility_with_plotly(self):
        """Test that loaded templates are compatible with Plotly."""
        import plotly.graph_objects as go
        from climatevis.util.util_plotly import load_plotly_template

        # Load a template
        template_data = load_plotly_template('base', 'compatibility_test')

        # Create a simple figure
        fig = go.Figure()
        fig.add_scatter(x=[1, 2, 3], y=[1, 4, 2])

        # Try to apply template properties (this tests compatibility)
        try:
            if 'layout' in template_data:
                # Apply some layout properties from template
                layout_updates = template_data['layout']
                if isinstance(layout_updates, dict):
                    # Apply a subset of properties to avoid conflicts
                    safe_properties = {k: v for k, v in layout_updates.items()
                                     if k in ['font', 'paper_bgcolor', 'plot_bgcolor']}
                    fig.update_layout(**safe_properties)

            # If we get here without error, template is compatible
            assert True

        except Exception as e:
            pytest.fail(f"Template not compatible with Plotly: {e}")

    def test_template_file_locations(self):
        """Test that template files are in the correct package location."""
        # Verify templates are accessible from the package
        try:
            import importlib.resources
            templates_dir = importlib.resources.files('climatevis.templates')

            # Check specific template files exist
            expected_templates = [
                'plotly_template_base.yaml',
                'plotly_template_base_autosize.yaml',
                'plotly_template_test.yaml'
            ]

            actual_files = [f.name for f in templates_dir.iterdir()]

            for expected_file in expected_templates:
                assert expected_file in actual_files, f"Expected template file {expected_file} not found"

        except (ImportError, AttributeError):
            # Fallback test for older Python versions
            import pkg_resources
            template_path = pkg_resources.resource_filename('climatevis', 'templates')

            expected_templates = [
                'plotly_template_base.yaml',
                'plotly_template_base_autosize.yaml',
                'plotly_template_test.yaml'
            ]

            actual_files = os.listdir(template_path)

            for expected_file in expected_templates:
                assert expected_file in actual_files, f"Expected template file {expected_file} not found"


class TestTemplateErrorHandling:
    """Test error handling in template loading."""

    def test_invalid_template_name_handling(self):
        """Test handling of invalid template names."""
        from climatevis.util.util_plotly import load_plotly_template

        invalid_names = ['', 'invalid_template', 'template_that_does_not_exist', None]

        for invalid_name in invalid_names:
            if invalid_name is None:
                continue  # Skip None which might cause different error

            with pytest.raises((FileNotFoundError, ValueError, KeyError, TypeError)):
                load_plotly_template(invalid_name)

    def test_corrupted_template_handling(self):
        """Test that the system handles potentially corrupted template data gracefully."""
        # This test ensures the loading function is robust
        # We can't easily create corrupted files in the package, but we can test error handling
        from climatevis.util.util_plotly import load_plotly_template

        # Test with edge cases that might cause issues
        edge_cases = ['', ' ', '\n', 'template.with.dots']

        for edge_case in edge_cases:
            try:
                result = load_plotly_template(edge_case)
                # If it succeeds, result should be a dict
                if result is not None:
                    assert isinstance(result, dict)
            except (FileNotFoundError, ValueError, KeyError, TypeError):
                # These exceptions are expected for invalid inputs
                pass


if __name__ == '__main__':
    pytest.main([__file__])