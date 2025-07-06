# Task List: ClimateVis Library Improvements - Phase 1

## Relevant Files

- `src/climatevis/plots/` - All plotting function files that need validation and type hints
- `src/climatevis/util/util_plotly.py` - Template system with hardcoded fallbacks
- `src/climatevis/__init__.py` - Package initialization and imports (✅ Updated)
- `app_plotting_test.py` - Example application with updated import paths (✅ Updated)
- `README.md` - Main documentation requiring comprehensive updates
- `PLOTTING_TEST_README.md` - Test documentation updates
- `tests/` - Test files requiring updates for new validation and functionality
- `src/climatevis/util/validation.py` - New validation utility functions (to be created)

### Notes

- Unit tests should be placed alongside the code files they are testing
- Use `pytest` to run tests. Running without a path executes all tests found by the pytest configuration
- All changes must maintain backward compatibility with existing function signatures
- Template fallbacks should be minimal but functional versions of existing templates

## Tasks

- [x] 1.0 Remove Code Duplication and Standardize Imports
  - [x] 1.1 Identify and catalog all duplicate files between `src/climatevis/plots/` and root `plots/` directory
  - [x] 1.2 Remove entire root `plots/` directory and its contents
  - [x] 1.3 Update any remaining import references in tests to use `src/climatevis/` paths
  - [x] 1.4 Update `app_plotting_test.py` to use correct import paths
  - [x] 1.5 Verify no broken imports remain in the codebase
  - [x] 1.6 Update `src/climatevis/__init__.py` to ensure proper package exports

- [ ] 2.0 Implement Comprehensive Input Validation
  - [x] 2.1 Create validation utility functions in `src/climatevis/util/validation.py`
  - [x] 2.2 Implement series list validation (type, content, DatetimeIndex)
  - [ ] 2.3 Implement Series attributes validation (unit, name) with helpful error messages
  - [ ] 2.4 Implement DatetimeIndex compatibility validation across series lists
  - [ ] 2.5 Implement template name validation against available templates
  - [ ] 2.6 Implement paper size validation against predefined options
  - [ ] 2.7 Add validation to `plot_series` function with comprehensive error handling
  - [ ] 2.8 Add validation to `plot_timeseries_df` function
  - [ ] 2.9 Add validation to `wind_rose` function
  - [ ] 2.10 Add validation to `exceedance` function
  - [ ] 2.11 Add validation to `exceedance_bands` function
  - [ ] 2.12 Add validation to `annual_heatmap` function
  - [ ] 2.13 Add validation to `histogram` function
  - [ ] 2.14 Add validation to `cumulative_probability` function
  - [ ] 2.15 Add validation to `monthly_profiles` function
  - [ ] 2.16 Add validation to `annual_profile_daily` function
  - [ ] 2.17 Add validation to `plot_rotated_box` function
  - [ ] 2.18 Test all validation functions with edge cases and error conditions

- [ ] 3.0 Add Type Hints and Standardize Import Patterns
  - [ ] 3.1 Add type hints to all function signatures in `src/climatevis/plots/`
  - [ ] 3.2 Add type hints to all return values in plotting functions
  - [ ] 3.3 Add type hints to major variables and parameters throughout codebase
  - [ ] 3.4 Standardize all imports to use absolute paths (`from climatevis.util import util_plotly`)
  - [ ] 3.5 Organize imports following PEP 8 guidelines (standard library, third-party, local)
  - [ ] 3.6 Add type hints to utility functions in `src/climatevis/util/`
  - [ ] 3.7 Add type hints to template functions in `src/climatevis/util/util_plotly.py`
  - [ ] 3.8 Verify type coverage exceeds 95% across all functions
  - [ ] 3.9 Test that all type hints are syntactically correct

- [ ] 4.0 Create Robust Template System with Hardcoded Fallbacks
  - [ ] 4.1 Create hardcoded template dictionaries in `src/climatevis/util/util_plotly.py`
  - [ ] 4.2 Implement fallback mechanism when file-based template loading fails
  - [ ] 4.3 Add YAML template structure validation on load
  - [ ] 4.4 Update template loading functions to use fallback system
  - [ ] 4.5 Test template fallback system with various failure scenarios
  - [ ] 4.6 Ensure template loading success rate exceeds 99% in different environments
  - [ ] 4.7 Maintain existing template API while adding reliability
  - [ ] 4.8 Add clear error messages for template loading failures

- [ ] 5.0 Update Documentation and README
  - [ ] 5.1 Update main `README.md` to reflect all API changes and improvements
  - [ ] 5.2 Add comprehensive section on Series requirements and expected attributes
  - [ ] 5.3 Create detailed examples showing proper data preparation for weather data
  - [ ] 5.4 Document the hardcoded template fallback system and its benefits
  - [ ] 5.5 Add troubleshooting section for common issues and error messages
  - [ ] 5.6 Include performance considerations for large datasets (8760×20)
  - [ ] 5.7 Document Marimo integration patterns and best practices
  - [ ] 5.8 Provide clear examples of proper Series attributes usage
  - [ ] 5.9 Update `PLOTTING_TEST_README.md` with new validation examples
  - [ ] 5.10 Test all documentation examples for accuracy and completeness
  - [ ] 5.11 Add migration guide for users transitioning from old import paths