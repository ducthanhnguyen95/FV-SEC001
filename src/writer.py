"""Output writer module for generating CSV result files."""

import os
from pathlib import Path

import polars as pl


def ensure_output_dir(output_dir: str) -> Path:
    """Create output directory if it doesn't exist.

    Args:
        output_dir: Path to the output directory.

    Returns:
        Resolved Path object for the output directory.
    """
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_csv(df: pl.DataFrame, file_path: str) -> str:
    """Write a DataFrame to CSV with formatted numeric columns.

    Formats CTR to 4 decimal places and CPA to 2 decimal places.
    Rounds total_spend to 2 decimal places.

    Args:
        df: DataFrame to write.
        file_path: Output file path.

    Returns:
        The absolute path of the written file.
    """
    formatted = df.with_columns(
        pl.col("total_spend").round(2),
        pl.col("CTR").round(4),
        pl.col("CPA").round(2),
    )

    formatted.write_csv(file_path)
    return str(Path(file_path).resolve())


def write_results(
    top10_ctr: pl.DataFrame,
    top10_cpa: pl.DataFrame,
    output_dir: str,
) -> tuple[str, str]:
    """Write both result files to the output directory.

    Args:
        top10_ctr: DataFrame with top 10 CTR campaigns.
        top10_cpa: DataFrame with top 10 CPA campaigns.
        output_dir: Directory to write output files.

    Returns:
        Tuple of (ctr_file_path, cpa_file_path).
    """
    out_path = ensure_output_dir(output_dir)

    ctr_path = write_csv(top10_ctr, str(out_path / "top10_ctr.csv"))
    cpa_path = write_csv(top10_cpa, str(out_path / "top10_cpa.csv"))

    return ctr_path, cpa_path
