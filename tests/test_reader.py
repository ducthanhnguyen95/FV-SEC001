"""Tests for the CSV reader module."""

import polars as pl
import pytest

from src.reader import load_csv_lazy, validate_file, get_file_size_mb


class TestValidateFile:
    """Tests for file validation."""

    def test_valid_csv_file(self, sample_csv_path: str) -> None:
        path = validate_file(sample_csv_path)
        assert path.exists()

    def test_file_not_found(self) -> None:
        with pytest.raises(FileNotFoundError, match="Input file not found"):
            validate_file("/nonexistent/file.csv")

    def test_empty_file(self, empty_csv_path: str) -> None:
        with pytest.raises(ValueError, match="Input file is empty"):
            validate_file(empty_csv_path)

    def test_not_csv_extension(self, tmp_path) -> None:
        txt_file = tmp_path / "data.txt"
        txt_file.write_text("some content")
        with pytest.raises(ValueError, match="Expected a .csv file"):
            validate_file(str(txt_file))


class TestLoadCsvLazy:
    """Tests for lazy CSV loading."""

    def test_returns_lazy_frame(self, sample_csv_path: str) -> None:
        result = load_csv_lazy(sample_csv_path)
        assert isinstance(result, pl.LazyFrame)

    def test_correct_schema(self, sample_csv_path: str) -> None:
        lazy_df = load_csv_lazy(sample_csv_path)
        schema = lazy_df.collect_schema()
        assert "campaign_id" in schema.names()
        assert "impressions" in schema.names()
        assert "clicks" in schema.names()
        assert "spend" in schema.names()
        assert "conversions" in schema.names()

    def test_row_count(self, sample_csv_path: str) -> None:
        lazy_df = load_csv_lazy(sample_csv_path)
        df = lazy_df.collect()
        assert len(df) == 15  # 15 data rows in sample

    def test_missing_columns(self, tmp_path) -> None:
        bad_csv = tmp_path / "bad.csv"
        bad_csv.write_text("id,value\n1,100\n")
        with pytest.raises(ValueError, match="missing required columns"):
            load_csv_lazy(str(bad_csv))

    def test_file_not_found(self) -> None:
        with pytest.raises(FileNotFoundError):
            load_csv_lazy("/nonexistent/file.csv")


class TestGetFileSizeMb:
    """Tests for file size utility."""

    def test_returns_float(self, sample_csv_path: str) -> None:
        size = get_file_size_mb(sample_csv_path)
        assert isinstance(size, float)
        assert size >= 0.0  # Sample file is small, so size may round to 0.0
