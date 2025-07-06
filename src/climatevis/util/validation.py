"""
Validation utilities for ClimateVis plotting functions.

This module provides comprehensive validation functions for ensuring data quality
and proper formatting before plotting operations.
"""

import logging
from typing import List, Union, Optional, Any, Dict
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Predefined paper sizes for validation
PAPER_SIZES = {
    "A6_LANDSCAPE", "A6_PORTRAIT",
    "A5_LANDSCAPE", "A5_PORTRAIT",
    "A4_LANDSCAPE", "A4_PORTRAIT",
    "A3_LANDSCAPE", "A3_PORTRAIT",
    "A2_LANDSCAPE", "A2_PORTRAIT",
    "A1_LANDSCAPE", "A1_PORTRAIT",
    "A0_LANDSCAPE", "A0_PORTRAIT"
}

# Common template names for validation
BUILTIN_TEMPLATES = {"base", "base_autosize", "test"}


def validate_series_list(
    series_list: Any,
    function_name: str = "plotting function"
) -> List[pd.Series]:
    """
    Validate that the input is a list/tuple of pandas Series.

    Parameters:
        series_list: The input to validate
        function_name: Name of the calling function for error messages

    Returns:
        List[pd.Series]: The validated list of series

    Raises:
        ValueError: If validation fails
    """
    # Check if it's a list or tuple
    if not isinstance(series_list, (list, tuple)):
        raise ValueError(
            f"{function_name}: series_list must be a list or tuple, got {type(series_list).__name__}"
        )

    # Check if list is not empty
    if len(series_list) == 0:
        raise ValueError(f"{function_name}: series_list cannot be empty")

    # Validate each item is a pandas Series
    validated_series = []
    for i, item in enumerate(series_list):
        if not isinstance(item, pd.Series):
            raise ValueError(
                f"{function_name}: Item {i} in series_list must be a pandas Series, "
                f"got {type(item).__name__}"
            )
        validated_series.append(item)

    return validated_series


def validate_datetime_index(
    series_list: List[pd.Series],
    function_name: str = "plotting function"
) -> None:
    """
    Validate that all series have DatetimeIndex.

    Parameters:
        series_list: List of pandas Series to validate
        function_name: Name of the calling function for error messages

    Raises:
        ValueError: If any series doesn't have DatetimeIndex
    """
    for i, series in enumerate(series_list):
        if not isinstance(series.index, pd.DatetimeIndex):
            raise ValueError(
                f"{function_name}: Series {i} ({series.name or 'unnamed'}) must have "
                f"DatetimeIndex, got {type(series.index).__name__}"
            )


def validate_series_attributes(
    series_list: List[pd.Series],
    function_name: str = "plotting function",
    require_attributes: bool = False
) -> None:
    """
    Validate Series attributes and provide helpful guidance.

    Parameters:
        series_list: List of pandas Series to validate
        function_name: Name of the calling function for error messages
        require_attributes: Whether to require name and unit attributes

    Raises:
        ValueError: If validation fails and require_attributes is True
    """
    for i, series in enumerate(series_list):
        series_name = f"Series {i}"

        # Check for name attribute
        if not hasattr(series, 'name') or series.name is None:
            if require_attributes:
                raise ValueError(
                    f"{function_name}: {series_name} must have a 'name' attribute. "
                    f"Set it with: series.name = 'Your Series Name'"
                )
            else:
                logging.warning(
                    f"{function_name}: {series_name} has no name attribute. "
                    f"Consider setting series.name for better plot labels."
                )

        # Check for unit attribute
        if not hasattr(series, 'attrs') or 'unit' not in series.attrs:
            if require_attributes:
                raise ValueError(
                    f"{function_name}: {series_name} must have a 'unit' attribute in attrs. "
                    f"Set it with: series.attrs['unit'] = 'Your Unit'"
                )
            else:
                logging.warning(
                    f"{function_name}: {series_name} has no unit attribute. "
                    f"Consider setting series.attrs['unit'] for better axis labels."
                )


def validate_datetime_compatibility(
    series_list: List[pd.Series],
    function_name: str = "plotting function"
) -> None:
    """
    Validate that all series have compatible DatetimeIndex ranges.

    Parameters:
        series_list: List of pandas Series to validate
        function_name: Name of the calling function for error messages

    Raises:
        ValueError: If series have incompatible time ranges
    """
    if len(series_list) < 2:
        return  # No compatibility check needed for single series

    # Get the reference index from the first series
    reference_index = series_list[0].index

    for i, series in enumerate(series_list[1:], 1):
        current_index = series.index

        # Check if indices are equal (exact match)
        if not reference_index.equals(current_index):
            # Check for overlap
            ref_start, ref_end = reference_index.min(), reference_index.max()
            curr_start, curr_end = current_index.min(), current_index.max()

            # Check if there's any overlap
            if curr_end < ref_start or curr_start > ref_end:
                raise ValueError(
                    f"{function_name}: Series {i} ({series.name or 'unnamed'}) has "
                    f"no time overlap with the first series. "
                    f"First series range: {ref_start} to {ref_end}, "
                    f"Series {i} range: {curr_start} to {curr_end}"
                )

            # Check for significant overlap (at least 50% of the shorter series)
            overlap_start = max(ref_start, curr_start)
            overlap_end = min(ref_end, curr_end)
            overlap_duration = overlap_end - overlap_start

            ref_duration = ref_end - ref_start
            curr_duration = curr_end - curr_start
            min_duration = min(ref_duration, curr_duration)

            if overlap_duration < min_duration * 0.5:
                logging.warning(
                    f"{function_name}: Series {i} ({series.name or 'unnamed'}) has "
                    f"limited time overlap with the first series. "
                    f"Overlap: {overlap_duration}, "
                    f"Minimum expected: {min_duration * 0.5}"
                )


def validate_template_name(
    template_name: str,
    function_name: str = "plotting function"
) -> None:
    """
    Validate that the template name exists in available templates.

    Parameters:
        template_name: Template name to validate
        function_name: Name of the calling function for error messages

    Raises:
        ValueError: If template name is invalid
    """
    try:
        from climatevis.util.util_plotly import get_available_templates
        available_templates = get_available_templates()
    except ImportError:
        # Fallback to builtin templates if import fails
        available_templates = BUILTIN_TEMPLATES

    if template_name not in available_templates:
        available_list = ", ".join(sorted(available_templates))
        raise ValueError(
            f"{function_name}: Invalid template name '{template_name}'. "
            f"Available templates: {available_list}"
        )


def validate_paper_size(
    paper_size: str,
    function_name: str = "plotting function"
) -> None:
    """
    Validate that the paper size is one of the predefined options.

    Parameters:
        paper_size: Paper size to validate
        function_name: Name of the calling function for error messages

    Raises:
        ValueError: If paper size is invalid
    """
    if paper_size not in PAPER_SIZES:
        available_sizes = ", ".join(sorted(PAPER_SIZES))
        raise ValueError(
            f"{function_name}: Invalid paper size '{paper_size}'. "
            f"Available sizes: {available_sizes}"
        )


def validate_data_quality(
    series_list: List[pd.Series],
    function_name: str = "plotting function"
) -> None:
    """
    Validate data quality and provide warnings for potential issues.

    Parameters:
        series_list: List of pandas Series to validate
        function_name: Name of the calling function for error messages
    """
    for i, series in enumerate(series_list):
        series_name = series.name or f"Series {i}"

        # Check for NaN values
        nan_count = series.isna().sum()
        if nan_count > 0:
            logging.warning(
                f"{function_name}: {series_name} contains {nan_count} NaN values "
                f"({nan_count/len(series)*100:.1f}% of data). "
                f"These will be excluded from plotting."
            )

        # Check for infinite values
        inf_count = np.isinf(series).sum()
        if inf_count > 0:
            logging.warning(
                f"{function_name}: {series_name} contains {inf_count} infinite values. "
                f"These will be excluded from plotting."
            )

        # Check for empty series after removing NaN/Inf
        valid_data = series.dropna()
        if len(valid_data) == 0:
            raise ValueError(
                f"{function_name}: {series_name} has no valid data after removing "
                f"NaN and infinite values."
            )

        # Check for constant data (might indicate issues)
        if len(valid_data) > 1 and valid_data.std() == 0:
            logging.info(
                f"{function_name}: {series_name} has constant values "
                f"({valid_data.iloc[0]}). This may result in a flat line plot."
            )


def validate_plot_parameters(
    series_list: Union[List[pd.Series], pd.Series],
    template_name: str,
    paper_size: str,
    function_name: str = "plotting function",
    require_attributes: bool = False
) -> List[pd.Series]:
    """
    Comprehensive validation for plotting function parameters.

    Parameters:
        series_list: Series or list of series to validate
        template_name: Template name to validate
        paper_size: Paper size to validate
        function_name: Name of the calling function for error messages
        require_attributes: Whether to require name and unit attributes

    Returns:
        List[pd.Series]: Validated list of series

    Raises:
        ValueError: If validation fails
    """
    # Convert single series to list for consistent processing
    if isinstance(series_list, pd.Series):
        series_list = [series_list]

    # Validate series list structure
    validated_series = validate_series_list(series_list, function_name)

    # Validate DatetimeIndex
    validate_datetime_index(validated_series, function_name)

    # Validate series attributes
    validate_series_attributes(validated_series, function_name, require_attributes)

    # Validate DatetimeIndex compatibility
    validate_datetime_compatibility(validated_series, function_name)

    # Validate template name
    validate_template_name(template_name, function_name)

    # Validate paper size
    validate_paper_size(paper_size, function_name)

    # Validate data quality
    validate_data_quality(validated_series, function_name)

    return validated_series


def get_validation_summary(series_list: List[pd.Series]) -> Dict[str, Any]:
    """
    Generate a summary of validation results for debugging.

    Parameters:
        series_list: List of validated series

    Returns:
        Dict containing validation summary
    """
    summary = {
        "total_series": len(series_list),
        "series_info": []
    }

    for i, series in enumerate(series_list):
        series_info = {
            "index": i,
            "name": getattr(series, 'name', None),
            "unit": series.attrs.get('unit', None) if hasattr(series, 'attrs') else None,
            "length": len(series),
            "index_type": type(series.index).__name__,
            "data_type": series.dtype.name,
            "nan_count": series.isna().sum(),
            "inf_count": np.isinf(series).sum() if series.dtype in ['float64', 'float32'] else 0,
            "time_range": f"{series.index.min()} to {series.index.max()}" if isinstance(series.index, pd.DatetimeIndex) else "N/A"
        }
        summary["series_info"].append(series_info)

    return summary