## Relevant Files

- `pyproject.toml` - Main package configuration file with dependencies and metadata ✓ Created
- `MANIFEST.in` - Package data configuration for including YAML template files ✓ Created
- `src/climatevis/__init__.py` - Main package initialization with top-level imports ✓ Updated with 13 key functions
- `src/climatevis/plots/__init__.py` - Plots module initialization and exports ✓ Updated with all 17 functions
- `src/climatevis/util/__init__.py` - Utilities module initialization ✓ Updated with util modules
- `src/climatevis/components/__init__.py` - Components module initialization ✓ Updated with graceful marimo handling
- `src/climatevis/components/weather.py` - Weather selection component ✓ Updated with graceful marimo imports
- `src/climatevis/templates/` - Directory for YAML template files as package data
- `.github/workflows/publish.yml` - GitHub Actions workflow for automated PyPI publishing
- `tests/__init__.py` - Test package initialization ✓ Created
- `tests/test_imports.py` - Test file to validate all imports work correctly ✓ Created
- `tests/test_plotting.py` - Test file to validate core plotting functionality ✓ Created
- `tests/test_templates.py` - Test file to validate template loading from package data ✓ Created
- `tests/test_function_availability.py` - Comprehensive test for all 14+ plot functions ✓ Created
- `README.md` - Updated documentation with installation and usage examples

### Notes

- The current structure needs reorganization from flat modules to proper src/ package structure
- All relative imports need conversion to absolute imports for pip installation
- YAML template files must be included as package data, not code
- Marimo components should be optional imports to avoid hard dependency

## Tasks

- [x] 1.0 Create proper package structure and configuration files
  - [x] 1.1 Create `src/climatevis/` directory structure with proper `__init__.py` files
  - [x] 1.2 Create `pyproject.toml` with package metadata, dependencies (plotly>=5.0, pandas>=1.3, numpy>=1.20, pyyaml>=6.0, marimo), and build configuration
  - [x] 1.3 Create `MANIFEST.in` to include YAML template files and other package data
  - [x] 1.4 Set up basic directory structure: `src/climatevis/{plots,util,components,templates}/`
  - [x] 1.5 Configure package entry points and optional dependencies for marimo components

- [x] 2.0 Reorganize code modules and fix import structure
  - [x] 2.1 Move all files from `plots/` to `src/climatevis/plots/` and update `__init__.py`
  - [x] 2.2 Move all files from `util/` to `src/climatevis/util/` and update `__init__.py`
  - [x] 2.3 Move all files from `components/` to `src/climatevis/components/` and update `__init__.py`
  - [x] 2.4 Convert all relative imports to absolute imports (e.g., `from util import util_plotly` → `from climatevis.util import util_plotly`)
  - [x] 2.5 Update main package `__init__.py` to expose key functions at top level (e.g., `from climatevis.plots import wind_rose`)
  - [x] 2.6 Handle marimo imports gracefully with try/except blocks to make them optional

- [x] 3.0 Configure package data and template loading system
  - [x] 3.1 Move YAML template files from `plotly_templates/` to `src/climatevis/templates/`
  - [x] 3.2 Update `util_plotly.py` to load templates from package data using `importlib.resources` or `pkg_resources`
  - [x] 3.3 Modify `load_plotly_template()` function to work with packaged template files
  - [ ] 3.4 Test template loading with all 3 existing templates (base, base_autosize, test)
  - [x] 3.5 Ensure MANIFEST.in correctly includes all template files

- [x] 4.0 Set up testing framework and validation
  - [x] 4.1 Create `tests/` directory with `__init__.py`
  - [x] 4.2 Create `tests/test_imports.py` to validate all modules import correctly
  - [x] 4.3 Create `tests/test_plotting.py` with basic tests for key plotting functions (wind_rose, plot_series, exceedance)
  - [x] 4.4 Create `tests/test_templates.py` to validate template loading from package data
  - [x] 4.5 Test local installation with `pip install -e .` and verify imports work
  - [x] 4.6 Test that all 14+ plot functions can be imported and called with sample data

- [ ] 5.0 Configure publishing pipeline and documentation
  - [ ] 5.1 Create `.github/workflows/publish.yml` for automated PyPI publishing on releases
  - [ ] 5.2 Create comprehensive `README.md` with installation instructions and examples for all major plot types
  - [ ] 5.3 Add usage examples for wind_rose, exceedance, annual_heatmap, and plot_series functions
  - [ ] 5.4 Document marimo component usage and optional import pattern
  - [ ] 5.5 Test publishing to TestPyPI first, then configure production PyPI publishing
  - [ ] 5.6 Create initial release (v0.1.0) and verify package installs correctly from PyPI