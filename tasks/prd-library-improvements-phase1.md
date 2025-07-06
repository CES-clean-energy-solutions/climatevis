# Product Requirements Document: ClimateVis Library Improvements - Phase 1

## Introduction/Overview

This PRD outlines the first phase of improvements to the ClimateVis plotting library, focusing on code quality, robustness, and maintainability. The goal is to create a more reliable, consistent, and developer-friendly library that works seamlessly with Marimo notebooks and handles weather data files (8760 hours × 20 variables) efficiently.

## Goals

1. **Eliminate code duplication** between `src/` and root `plots/` directories
2. **Implement comprehensive input validation** across all plotting functions
3. **Standardize import patterns** and add type hints throughout the codebase
4. **Create robust template system** with hardcoded fallbacks for reliability
5. **Maintain backward compatibility** while highlighting any breaking changes
6. **Improve error handling** for better debugging experience

## User Stories

- **As a developer** integrating ClimateVis into a Marimo notebook, I want consistent API behavior so that I can rely on the library without unexpected errors.

- **As a data scientist** working with large weather datasets (8760×20), I want robust input validation so that I get clear error messages when data is malformed.

- **As a researcher** using the plotting functions, I want reliable template loading so that my visualizations always render correctly regardless of file system issues.

- **As a developer** maintaining the codebase, I want standardized imports and type hints so that I can easily understand and modify the code.

## Functional Requirements

### 1. Code Duplication Elimination
1.1. The system must remove all duplicate plotting functions from the root `plots/` directory
1.2. The system must ensure all imports reference the `src/climatevis/` package structure
1.3. The system must update any remaining references to use the correct import paths
1.4. The system must maintain the existing public API surface during this transition

### 2. Input Validation Implementation
2.1. The system must validate that `series_list` parameters are lists/tuples containing pandas Series
2.2. The system must validate that all Series have DatetimeIndex
2.3. The system must validate that template names exist in available templates before use
2.4. The system must validate paper size parameters against predefined options
2.5. The system must provide clear, actionable error messages for validation failures
2.6. The system must handle edge cases like empty series lists, None values, and malformed data
2.7. The system must validate Series attributes (unit, name) and provide guidance when missing
2.8. The system must validate that all Series in a list have compatible DatetimeIndex ranges
2.9. The system must provide specific error messages for common Series attribute issues

### 3. Import Standardization
3.1. The system must use absolute imports consistently (`from climatevis.util import util_plotly`)
3.2. The system must add type hints to all function signatures
3.3. The system must add type hints to all return values
3.4. The system must add type hints to all major variables and parameters
3.5. The system must ensure all imports are properly organized (standard library, third-party, local)

### 4. Template System Robustness
4.1. The system must create hardcoded template dictionaries as fallbacks
4.2. The system must implement a fallback mechanism when file-based template loading fails
4.3. The system must validate YAML template structure on load
4.4. The system must provide clear error messages when templates fail to load
4.5. The system must maintain the existing template API while adding reliability

### 5. Documentation and README Updates
5.1. The system must update the main README.md to reflect all API changes and improvements
5.2. The system must clearly document the series list requirements and expected attributes
5.3. The system must provide comprehensive examples showing proper data preparation
5.6. The system must document the hardcoded template fallback system
5.7. The system must provide troubleshooting section for common issues
5.8. The system must include performance considerations for large datasets (8760×20)
5.9. The system must document Marimo integration patterns and best practices
5.10. The system must provide clear examples of proper Series attributes usage

## Non-Goals (Out of Scope)

- Adding new plotting functions or features
- Changing the core plotting logic or algorithms
- Modifying the visual appearance of existing plots
- Adding new dependencies beyond the current stack
- Creating new documentation or examples
- Performance optimizations for large datasets
- Adding new template designs

## Design Considerations

- **Error Messages**: Should be developer-friendly with specific guidance on how to fix issues
- **Type Hints**: Should use modern Python typing (Python 3.8+) with proper generics
- **Import Structure**: Should follow PEP 8 guidelines for import organization
- **Template Fallbacks**: Should be minimal but functional versions of existing templates
- **Series Requirements**: Must clearly document expected pandas Series structure and attributes
- **Data Validation**: Should provide helpful guidance for common data preparation issues

## Technical Considerations

- **Backward Compatibility**: All existing function signatures must remain unchanged
- **Performance**: Validation should be fast and not significantly impact plotting performance
- **Testing**: All changes must maintain or improve existing test coverage
- **Dependencies**: No new dependencies should be added for this phase
- **File Structure**: Maintain the existing `src/climatevis/` package structure

## Success Metrics

1. **Code Quality**: Zero duplicate functions between directories
2. **Test Coverage**: Maintain >90% test coverage after changes
3. **Error Handling**: All validation failures provide actionable error messages
4. **Import Consistency**: 100% of imports use absolute paths
5. **Type Coverage**: >95% of functions have complete type hints
6. **Template Reliability**: Template loading success rate >99% in various environments

## Open Questions

1. Should we add runtime type checking (e.g., with `typeguard`) for development builds?
2. Do we need to create a migration guide for users who might be importing from the old paths?
3. Should we add deprecation warnings for any functions that will be removed?
4. What level of template validation is appropriate (schema validation vs. basic structure)?
5. Should we provide default Series attributes when missing (e.g., auto-generate units)?
6. How detailed should the troubleshooting section be in the README?
7. Should we include performance benchmarks in the documentation?

## Implementation Notes

### Breaking Changes to Highlight
- Removal of duplicate functions from root `plots/` directory
- Any imports that previously worked from root directory will need to be updated
- Template loading behavior may change slightly (more robust but potentially different error messages)
- Stricter validation of Series attributes and DatetimeIndex compatibility
- More specific error messages that may reveal previously silent issues

### Files to Modify
- All files in `src/climatevis/plots/` (add validation and type hints)
- `src/climatevis/util/util_plotly.py` (add hardcoded templates)
- `src/climatevis/__init__.py` (ensure proper imports)
- Remove entire `plots/` directory from root
- Update any remaining references in tests and examples
- `README.md` (comprehensive update with new requirements and examples)
- `PLOTTING_TEST_README.md` (update with new validation examples)

### Testing Strategy
- Add validation tests for each plotting function
- Test template fallback mechanisms
- Verify backward compatibility with existing code
- Test error message clarity and usefulness
- Test Series attribute validation and error messages
- Test DatetimeIndex compatibility validation
- Test documentation examples for accuracy and completeness