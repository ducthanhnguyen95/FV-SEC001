"""CSV Reader module using Polars LazyFrame for memory-efficient processing."""

import os
from pathlib import Path

import polars as pl


EXPECTED_COLUMNS = {
    "campaign_id",
    "date",
    "impressions",
    "clicks",
    "spend",
    "conversions",
}

SCHEMA_OVERRIDES = {
    "campaign_id": pl.Utf8,
    "date": pl.Utf8,
    "impressions": pl.Int64,
    "clicks": pl.Int64,
    "spend": pl.Float64,
    "conversions": pl.Int64,
}


def validate_file(file_path: str) -> Path:
    """Validate that the input file exists and is readable.

    Args:
        file_path: Path to the CSV file.

    Returns:
        Resolved Path object.

    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If file is empty or not a CSV.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    if path.stat().st_size == 0:
        raise ValueError(f"Input file is empty: {file_path}")

    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a .csv file, got: {path.suffix}")

    return path


def load_csv_lazy(file_path: str) -> pl.LazyFrame:
    """Load a CSV file as a Polars LazyFrame for streaming processing.

    Uses scan_csv() which builds a query plan without loading the entire
    file into memory. The actual processing is deferred until collect().

    Args:
        file_path: Path to the input CSV file.

    Returns:
        A Polars LazyFrame ready for deferred processing.

    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If file is empty, not CSV, or has invalid schema.
    """
    path = validate_file(file_path)

    lazy_df = pl.scan_csv(
        path,
        schema_overrides=SCHEMA_OVERRIDES,
        ignore_errors=True,
    )

    # Validate that expected columns exist
    actual_columns = set(lazy_df.collect_schema().names())
    missing = EXPECTED_COLUMNS - actual_columns
    if missing:
        raise ValueError(
            f"CSV is missing required columns: {', '.join(sorted(missing))}. "
            f"Found columns: {', '.join(sorted(actual_columns))}"
        )

    # Select only required columns in the correct order
    lazy_df = lazy_df.select(sorted(EXPECTED_COLUMNS))

    return lazy_df


def get_file_size_mb(file_path: str) -> float:
    """Get file size in megabytes.

    Args:
        file_path: Path to the file.

    Returns:
        File size in MB rounded to 1 decimal.
    """
    return round(os.path.getsize(file_path) / (1024 * 1024), 1)
