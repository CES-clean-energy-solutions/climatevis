# PRD: ClimateVis - Pip-Installable Weather Data Visualization Library

## Introduction/Overview

Create a standalone, pip-installable Python package called `climatevis` from the existing weather visualization library. This will enable team members and the broader community to easily install and use professional weather/climate data visualization tools with a simple `pip install climatevis`.

**Problem**: Currently, the plotting functionality exists as a local module with relative imports, making it difficult to reuse across different projects and share with others.

**Goal**: Transform the existing climatevis library into a professional, public Python package that can be easily installed and used by anyone working with weather/climate data.

## Goals

1. **Reusability**: Enable easy reuse of plotting functions across multiple projects
2. **Shareability**: Make the library publicly available for the climate/weather data community
3. **Professional Distribution**: Create a proper Python package with standard tooling and documentation
4. **Fast Implementation**: Get the package working and published quickly
5. **Integration Success**: Ensure the weather explorer app works seamlessly with the pip-installed package

## User Stories

- **As a team member**, I want to install the plotting library with `pip install climatevis` so that I can use it in any project without copying code
- **As a data scientist**, I want to create professional weather visualizations (wind roses, exceedance curves, annual heatmaps) so that I can analyze climate data effectively
- **As a researcher**, I want access to a comprehensive climate plotting library with 14+ specialized plot types so that I can focus on analysis rather than building visualization tools
- **As a marimo notebook user**, I want integrated UI components for weather file selection so that I can build interactive climate analysis dashboards
- **As a developer**, I want clear documentation and examples so that I can quickly implement the plotting functions

## Functional Requirements

1. **Package Structure**: Create a proper Python package with src/climatevis/ structure
2. **Core Plotting Functions**: Include all 14+ existing plotting functions:
   - **Basic Plots**: `histogram`, `plot_series`, `plot_timeseries_df`
   - **Climate Analysis**: `exceedance`, `exceedance_bands`, `cumulative_probability`
   - **Temporal Visualization**: `annual_heatmap`, `annual_profile_daily`, `annual_profile_multiple`
   - **Statistical Plots**: `monthly_profiles`, `monthly_profiles_bands`
   - **Specialized Plots**: `wind_rose`, `plot_rotated_box`
3. **Template System**: Include all 3 plotly templates (YAML files) as package data with sophisticated template loading system
4. **Utility Functions**: Integrate util_plotly functionality with predefined paper sizes (A0-A6) and template management
5. **Components Module**: Include marimo weather selection component with support for multiple weather file sources
6. **Psychrometric Charts**: Include psychrometric chart utilities (18KB+ of specialized functionality)
7. **Dependency Management**: Proper dependency specification (plotly>=5.0, pandas>=1.3, numpy>=1.20, pyyaml>=6.0, marimo for UI components)
8. **Import Structure**: Fix relative imports to work with pip-installed package
9. **PyPI Publishing**: Configure for public release on PyPI
10. **Documentation**: Basic README with installation and usage examples
11. **Testing**: Basic test structure to ensure functionality
12. **CI/CD**: Automated publishing workflow

## Non-Goals (Out of Scope)

- Backward compatibility with existing import structure
- Extensive documentation beyond basic usage
- Advanced testing coverage (basic tests only for speed)
- Multiple template customization options (use existing templates)
- Support for non-plotly visualization backends

## Technical Considerations

- **Package Name**: `climatevis` (PyPI and import name, matching current directory structure)
- **Current License**: Apache License 2.0 (already in place)
- **Build System**: Use modern pyproject.toml configuration
- **Dependencies**: plotly>=5.0, pandas>=1.3, numpy>=1.20, pyyaml>=6.0, marimo (for UI components)
- **Python Support**: Python 3.8+
- **Template Loading**: Include 3 YAML templates as package data using MANIFEST.in with existing sophisticated loading system
- **Import Structure**: Convert relative imports (`from util import util_plotly`) to absolute imports (`from climatevis.util import util_plotly`)
- **Data Files**: Include plotly template YAML files as package data
- **GitHub Actions**: Automated testing and PyPI publishing

## Success Metrics

1. **Primary Success**: Any project can use `pip install climatevis` and import functions like `from climatevis.plots import wind_rose, exceedance, annual_heatmap`
2. **Package Availability**: Successfully published on PyPI and installable by anyone
3. **Functionality**: All 14+ existing plot types work identically to current implementation
4. **Template System**: Plotly templates load correctly from package data
5. **Marimo Integration**: Weather selection components work in marimo notebooks
6. **Team Adoption**: Team members can use the package in new projects immediately

## Implementation Priority

**Phase 1 (Critical Path)**:
1. Create proper package structure with src/climatevis/ (current structure needs reorganization)
2. Fix relative imports in all modules (convert `from util import util_plotly` to `from climatevis.util import util_plotly`)
3. Create pyproject.toml with proper dependencies and package data configuration
4. Set up MANIFEST.in to include YAML template files
5. Test local installation and imports

**Phase 2 (Publishing)**:
6. Configure GitHub Actions for CI/CD and automated PyPI publishing
7. Publish first version (0.1.0) to PyPI
8. Update any existing projects to use pip-installed package
9. Create comprehensive README with examples for all 14+ plot types
10. Document marimo component usage

## Open Questions

1. Should marimo components be in main package or optional dependency? (Currently integrated, suggest keeping as optional import)
2. Version number for initial release: 0.1.0 recommended
3. License: Apache License 2.0 already in place
4. Should psychrometric chart utilities be included or separate module? (Currently 18KB+ of specialized code)
5. Template loading path strategy for package data access

## Acceptance Criteria

- [ ] `pip install climatevis` works successfully
- [ ] All plotting functions import correctly: `from climatevis.plots import wind_rose, exceedance, annual_heatmap, plot_series, etc.`
- [ ] Also allow `import climvatevis as climatevis` and get access to the main plot functions
- [ ] All 14+ existing plot types render identically to current implementation
- [ ] Plotly templates load correctly from package data
- [ ] Marimo components import and function: `from climatevis.components import weather_selection`
- [ ] Utility functions work: `from climatevis.util import util_plotly`
- [ ] Package is publicly available on PyPI
- [ ] Comprehensive README with installation and usage examples for all plot types
- [ ] GitHub repository with automated publishing is set up
- [ ] Psychrometric chart functionality preserved (if included)