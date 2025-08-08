# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Testing
```bash
# Run all tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_plotting_integration.py -v

# Run tests with specific markers
pytest -m "not slow" -v
pytest -m integration -v
pytest -m unit -v

# Run single test function
pytest tests/test_function_availability.py::TestFunctionAvailability::test_all_functions_importable -v
```

### Code Quality
```bash
# Format code with Black (line length 88)
black .
black src/climatevis/

# Sort imports with isort (configured for Black compatibility)
isort .
isort src/climatevis/

# Lint with flake8
flake8
flake8 src/climatevis/
```

### Building and Installation
```bash
# Build the package
python -m build

# Install in development mode
pip install -e .

# Install with optional dependencies
pip install -e ".[marimo]"  # For marimo UI components
pip install -e ".[dev]"     # For development tools
```

### Running Examples
```bash
# Run marimo interactive examples
marimo run user_test_marimo/app_plotting_test.py
```

## Code Architecture

### Package Structure
- `src/climatevis/` - Main package source code
  - `plots/` - Core plotting functions (time series, histograms, wind roses, etc.)
  - `components/` - Marimo UI components for interactive applications
  - `templates/` - YAML template definitions and management
  - `util/` - Utility functions (Plotly helpers, validation, psychrometric charts)

### Key Components

**Plotting System (`src/climatevis/plots/`):**
- All plotting functions follow consistent signature patterns with `template_name` and `paper_size` parameters
- Functions expect pandas Series with DatetimeIndex for time-based plots
- Series metadata is stored in `.attrs` dictionary (e.g., `series.attrs['unit'] = '°C'`)
- Multi-series plots handle different units by using dual y-axes

**Template System (`src/climatevis/util/util_plotly.py`):**
- Templates are loaded from YAML files in `src/climatevis/templates/`
- Auto-loading occurs on package import via `load_all_builtin_templates()`
- Templates define Plotly layout configurations and paper sizes
- Available templates: `base`, `base_autosize`, `test`

**Marimo Integration (`src/climatevis/components/`):**
- Optional dependency - import fails gracefully if marimo not installed
- Provides pre-configured dropdown components for templates and paper sizes
- Weather data selection utilities for interactive applications

**Validation System (`src/climatevis/util/validation.py`):**
- Input validation for data types, DatetimeIndex requirements
- Unit compatibility checks for multi-series plots
- Template and paper size validation

### Development Patterns

**Function Signatures:**
Most plotting functions follow this pattern:
```python
def plot_function(data, template_name, paper_size, **kwargs):
    # Input validation
    # Data processing
    # Plotly figure creation with template
    # Return plotly.graph_objects.Figure
```

**Error Handling:**
- All functions include comprehensive input validation
- Clear error messages for common issues (wrong data types, missing DatetimeIndex)
- Graceful degradation for optional features

**Testing Structure:**
- `tests/test_imports.py` - Import validation
- `tests/test_function_availability.py` - Function availability checks
- `tests/test_plotting_integration.py` - End-to-end plotting tests
- `tests/test_templates.py` - Template loading and validation
- `tests/test_validation_integration.py` - Input validation tests

### Paper Size System
Predefined paper sizes from A6 to A0 in both landscape and portrait orientations, defined as pixel dimensions for consistent output across different display contexts.

### Dependencies
- Core: plotly, pandas, numpy, pyyaml
- Optional: marimo (for UI components)
- Development: pytest, black, isort, flake8

## Important Notes

- Always use `pytest -v` for running tests to get detailed output
- Code formatting is enforced with Black (88 char line length) and isort
- Template loading happens automatically on import - check for warnings if templates fail to load
- Marimo components are optional - code should handle ImportError gracefully
- All time series data must have DatetimeIndex - this is strictly validated
- When adding new plotting functions, follow existing patterns for template and paper size handling