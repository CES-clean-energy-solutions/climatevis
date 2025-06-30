# Marimo API Reference and Best Practices

This document provides comprehensive guidelines for using marimo's UI components and API patterns effectively.

## 🔧 Data Editor Component

### Overview
The `mo.ui.data_editor` is a component for editing tabular data interactively. It's experimental and intentionally feature-limited.

**Source:** [Marimo Data Editor Documentation](https://docs.marimo.io/api/inputs/data_editor/)

### Basic Usage Patterns

#### 1. **DataFrame Input (Recommended)**
```python
@app.cell
def create_data_editor_from_dataframe(mo, pd):
    """Create data editor from pandas DataFrame"""
    df = pd.DataFrame({
        "Temperature": [25.0, 23.5, 26.2],
        "Zone": ["Zone 1", "Zone 2", "Zone 3"],
        "Active": [True, False, True]
    })

    editor = mo.ui.data_editor(
        data=df,
        label="Edit Zone Data",
        pagination=True,
        page_size=50,
        column_sizing_mode="auto"  # or "fit"
    )

    editor
    return editor,
```

#### 2. **List of Dictionaries (Row-Oriented)**
```python
@app.cell
def create_data_editor_from_list(mo):
    """Create data editor from list of dictionaries"""
    data = [
        {"Zone": "Zone 1", "Temp": 25.0, "Load": 800},
        {"Zone": "Zone 2", "Temp": 23.5, "Load": 600},
        {"Zone": "Zone 3", "Temp": 26.2, "Load": 1000}
    ]

    editor = mo.ui.data_editor(data=data, label="Zone Parameters")
    editor
    return editor,
```

#### 3. **Dictionary of Lists (Column-Oriented)**
```python
@app.cell
def create_data_editor_from_dict(mo):
    """Create data editor from dictionary of lists"""
    data = {
        "Zone": ["Zone 1", "Zone 2", "Zone 3"],
        "Temperature": [25.0, 23.5, 26.2],
        "Load": [800, 600, 1000]
    }

    editor = mo.ui.data_editor(data=data, label="Zone Configuration")
    editor
    return editor,
```

### Data Editor Properties and Methods

#### Core Properties
```python
@app.cell
def access_editor_properties(editor):
    """Access data editor properties"""
    # Current edited data
    edited_data = editor.value  # Returns edited DataFrame/data

    # Original data
    original_data = editor.data  # Returns original input data

    # HTML representation
    html_content = editor.text  # String of HTML

    return edited_data, original_data
```

#### Configuration Parameters
```python
@app.cell
def create_configured_data_editor(mo, df):
    """Data editor with all configuration options"""
    editor = mo.ui.data_editor(
        data=df,

        # Display options
        label="**Edit Simulation Data**",
        pagination=True,           # Enable pagination for large datasets
        page_size=25,             # Items per page
        column_sizing_mode="fit", # "auto" or "fit"

        # Callback for changes
        on_change=lambda data: print(f"Data changed: {len(data)} rows")
    )

    editor
    return editor,
```

### Integration with Forms

#### Form-Wrapped Data Editor
```python
@app.cell
def create_data_editor_form(mo, pd):
    """Data editor wrapped in a form for batch submission"""
    df = pd.DataFrame({
        "Parameter": ["UA_ambient", "Q_internal", "Capacitance"],
        "Zone_1": [150, 800, 1.5e6],
        "Zone_2": [140, 300, 1.0e6],
        "Zone_3": [180, 1200, 2.0e6]
    })

    form = mo.ui.data_editor(df, label="Zone Parameters").form(
        bordered=True,
        submit_button_label="Update Simulation",
        submit_button_tooltip="Apply changes to simulation",
        clear_on_submit=False,
        show_clear_button=True
    )

    form
    return form,

@app.cell
def process_form_submission(form, mo):
    """Process form submission with validation"""
    mo.stop(form.value is None, mo.md("⏳ Make changes and submit"))

    # Process the edited data
    updated_data = form.value

    # Validation logic here
    if len(updated_data) == 0:
        error_msg = mo.md("❌ No data provided").callout(kind="danger")
        error_msg
        return

    success_msg = mo.md(f"✅ Updated {len(updated_data)} rows").callout(kind="success")
    success_msg
    return updated_data,
```

### Data Persistence Patterns

#### Save to File
```python
@app.cell
def save_edited_data_to_file(editor, mo):
    """Save edited data to CSV file"""
    if editor.value is not None:
        # For pandas DataFrame
        if hasattr(editor.value, 'to_csv'):
            editor.value.to_csv("updated_data.csv", index=False)

        # For polars DataFrame
        elif hasattr(editor.value, 'write_csv'):
            editor.value.write_csv("updated_data.csv")

        # For other formats, convert to pandas first
        else:
            import pandas as pd
            pd.DataFrame(editor.value).to_csv("updated_data.csv", index=False)

        status = mo.md("💾 Data saved to file").callout(kind="success")
    else:
        status = mo.md("⏳ No changes to save").callout(kind="neutral")

    status
    return
```

#### Real-time Data Sync
```python
@app.cell
def sync_data_with_simulation(editor, mo):
    """Sync edited data with simulation parameters in real-time"""
    def _sync_data():
        if editor.value is None:
            return None, "No data available"

        try:
            # Convert to simulation parameters
            df = editor.value

            # Extract parameters (example for zone simulation)
            if 'Temperature' in df.columns:
                temperatures = df['Temperature'].values
                return temperatures, "Data synchronized"
            else:
                return None, "Required columns missing"

        except Exception as e:
            return None, f"Sync error: {str(e)}"

    sync_result, sync_message = _sync_data()

    if sync_result is not None:
        status = mo.md(f"🔄 {sync_message}").callout(kind="success")
    else:
        status = mo.md(f"❌ {sync_message}").callout(kind="warning")

    status
    return sync_result,
```

## 📊 Data Editor Limitations and Considerations

### Row Limit
```python
# Data editor has a LIMIT of 1000 rows
EDITOR_LIMIT = 1000  # mo.ui.data_editor.LIMIT

@app.cell
def check_data_size_limits(df, mo):
    """Check if data exceeds editor limits"""
    if len(df) > EDITOR_LIMIT:
        warning = mo.md(f"""
        ⚠️ **Data Size Warning**

        Your data has {len(df)} rows, but data_editor is limited to {EDITOR_LIMIT} rows.

        **Recommended actions:**
        - Use pagination with smaller page_size
        - Filter data before editing
        - Consider splitting into multiple editors
        """).callout(kind="warning")

        # Show preview of first N rows
        preview_editor = mo.ui.data_editor(
            df.head(EDITOR_LIMIT),
            label=f"Preview (first {EDITOR_LIMIT} rows)"
        )

        mo.vstack([warning, preview_editor])
    else:
        full_editor = mo.ui.data_editor(df, label="Full Dataset")
        full_editor

    return
```

### Performance Considerations
```python
@app.cell
def optimize_data_editor_performance(mo, large_df):
    """Optimize data editor for better performance"""

    # For large datasets, use pagination
    optimized_editor = mo.ui.data_editor(
        large_df,
        pagination=True,
        page_size=25,  # Smaller page size for better performance
        column_sizing_mode="fit"  # Fit columns to view
    )

    # Display performance tips
    tips = mo.md("""
    💡 **Performance Tips:**
    - Enable pagination for datasets > 100 rows
    - Use smaller page_size (10-50) for complex data
    - Set column_sizing_mode="fit" for many columns
    - Avoid real-time on_change callbacks for large data
    """).callout(kind="info")

    mo.vstack([tips, optimized_editor])
    return optimized_editor,
```

## 🔄 Integration with Other UI Components

### Combining with Other Inputs
```python
@app.cell
def create_data_editor_with_controls(mo, pd):
    """Data editor with additional control widgets"""

    # Control widgets
    add_row_btn = mo.ui.button(label="➕ Add Row")
    filter_dropdown = mo.ui.dropdown(
        options=["All", "Active Only", "Inactive Only"],
        value="All",
        label="Filter"
    )

    # Sample data
    df = pd.DataFrame({
        "Zone": [f"Zone {i+1}" for i in range(5)],
        "Active": [True, False, True, True, False],
        "Temperature": [25.0, 23.5, 26.2, 24.8, 22.1]
    })

    # Filter data based on dropdown
    if filter_dropdown.value == "Active Only":
        filtered_df = df[df['Active'] == True]
    elif filter_dropdown.value == "Inactive Only":
        filtered_df = df[df['Active'] == False]
    else:
        filtered_df = df

    editor = mo.ui.data_editor(filtered_df, label="Zone Configuration")

    # Layout
    controls = mo.hstack([add_row_btn, filter_dropdown], gap=2)

    mo.vstack([
        mo.md("## Zone Data Editor"),
        controls,
        editor
    ])

    return editor, add_row_btn, filter_dropdown
```

### Validation and Error Handling
```python
@app.cell
def validate_data_editor_input(editor, mo):
    """Validate data editor input with comprehensive error handling"""

    def _validate_data():
        if editor.value is None:
            return False, "No data provided"

        try:
            df = editor.value

            # Check required columns
            required_cols = ['Zone', 'Temperature']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                return False, f"Missing columns: {missing_cols}"

            # Check data types
            if not pd.api.types.is_numeric_dtype(df['Temperature']):
                return False, "Temperature must be numeric"

            # Check value ranges
            if (df['Temperature'] < -50).any() or (df['Temperature'] > 100).any():
                return False, "Temperature must be between -50°C and 100°C"

            # Check for duplicates
            if df['Zone'].duplicated().any():
                return False, "Duplicate zone names found"

            return True, "Data validation passed"

        except Exception as e:
            return False, f"Validation error: {str(e)}"

    is_valid, validation_message = _validate_data()

    if is_valid:
        status = mo.md(f"✅ {validation_message}").callout(kind="success")
        validated_data = editor.value
    else:
        status = mo.md(f"❌ {validation_message}").callout(kind="danger")
        validated_data = None

    status
    return validated_data, is_valid
```

## 🎯 Best Practices Summary

### 1. **Data Format Choice**
- **Use DataFrames** for complex data with mixed types
- **Use list of dicts** for simple, row-oriented data
- **Use dict of lists** for column-oriented operations

### 2. **Performance Optimization**
```python
# ✅ GOOD - For large datasets
editor = mo.ui.data_editor(
    data=df,
    pagination=True,
    page_size=25,
    column_sizing_mode="fit"
)

# ❌ AVOID - For large datasets without pagination
editor = mo.ui.data_editor(data=large_df, pagination=False)
```

### 3. **Form Integration**
```python
# ✅ GOOD - Use forms for batch updates
form = mo.ui.data_editor(df).form(
    submit_button_label="Apply Changes",
    clear_on_submit=False
)

# ❌ AVOID - Real-time updates for large data
editor = mo.ui.data_editor(
    df,
    on_change=heavy_computation  # Can cause performance issues
)
```

### 4. **Error Handling**
```python
# ✅ GOOD - Always validate editor data
@app.cell
def process_editor_data(editor, mo):
    mo.stop(editor.value is None, mo.md("⏳ Enter data first"))

    # Additional validation here
    validated_data = validate_data(editor.value)
    return validated_data,
```

### 5. **Memory Management**
```python
# ✅ GOOD - Clear references to large datasets
@app.cell
def cleanup_large_data(_large_df, editor):
    """Process data then clear large intermediate variables"""
    processed_data = process_editor_data(editor.value)

    # Clear large intermediate data
    del _large_df

    return processed_data,
```

## 🔗 Related Components

- `mo.ui.table()` - For display-only tabular data
- `mo.ui.dataframe()` - For DataFrame display with built-in controls
- `mo.ui.form()` - For grouping multiple inputs including data_editor
- `mo.ui.batch()` - For creating custom UI element collections

## 📚 Additional Resources

- [Official Data Editor Documentation](https://docs.marimo.io/api/inputs/data_editor/)
- [Marimo UI Components Overview](https://docs.marimo.io/api/inputs/)
- [Form Integration Guide](https://docs.marimo.io/api/inputs/form/)

---

**Note:** The `data_editor` component is experimental. Feature requests and issues should be filed at the [marimo GitHub repository](https://github.com/marimo-team/marimo/issues).