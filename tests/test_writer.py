"""Tests for the output writer module."""

import os
from pathlib import Path

import polars as pl
import pytest

from src.writer import ensure_output_dir, write_csv, write_results


class TestEnsureOutputDir:
    """Tests for output directory creation."""

    def test_creates_directory(self, tmp_path: Path) -> None:
        new_dir = tmp_path / "new_output"
        result = ensure_output_dir(str(new_dir))
        assert result.exists()
        assert result.is_dir()

    def test_existing_directory_ok(self, tmp_path: Path) -> None:
        result = ensure_output_dir(str(tmp_path))
        assert result.exists()

    def test_nested_directory_creation(self, tmp_path: Path) -> None:
        nested = tmp_path / "a" / "b" / "c"
        result = ensure_output_dir(str(nested))
        assert result.exists()


class TestWriteCsv:
    """Tests for CSV writing."""

    def test_file_created(self, tmp_path: Path) -> None:
        df = pl.DataFrame({
            "campaign_id": ["CMP001"],
            "total_impressions": [10000],
            "total_clicks": [500],
            "total_spend": [100.0],
            "total_conversions": [20],
            "CTR": [0.05],
            "CPA": [5.0],
        })
        path = str(tmp_path / "test.csv")
        write_csv(df, path)
        assert os.path.exists(path)

    def test_csv_content_readable(self, tmp_path: Path) -> None:
        df = pl.DataFrame({
            "campaign_id": ["CMP001"],
            "total_impressions": [10000],
            "total_clicks": [500],
            "total_spend": [100.0],
            "total_conversions": [20],
            "CTR": [0.05],
            "CPA": [5.0],
        })
        path = str(tmp_path / "test.csv")
        write_csv(df, path)

        read_back = pl.read_csv(path)
        assert len(read_back) == 1
        assert read_back["campaign_id"].item() == "CMP001"


class TestWriteResults:
    """Tests for full result writing."""

    def test_both_files_created(self, tmp_path: Path) -> None:
        top10_ctr = pl.DataFrame({
            "campaign_id": ["CMP001"],
            "total_impressions": [10000],
            "total_clicks": [500],
            "total_spend": [100.0],
            "total_conversions": [20],
            "CTR": [0.05],
            "CPA": [5.0],
        })
        top10_cpa = top10_ctr.clone()

        out_dir = str(tmp_path / "results")
        ctr_path, cpa_path = write_results(top10_ctr, top10_cpa, out_dir)

        assert os.path.exists(ctr_path)
        assert os.path.exists(cpa_path)
        assert "top10_ctr.csv" in ctr_path
        assert "top10_cpa.csv" in cpa_path
