"""Tests for the aggregation module."""

import polars as pl
import pytest

from src.aggregator import aggregate_campaigns, get_top10_ctr, get_top10_cpa
from src.reader import load_csv_lazy


class TestAggregateCampaigns:
    """Tests for campaign aggregation."""

    def test_aggregation_produces_correct_columns(self, sample_csv_path: str) -> None:
        lazy_df = load_csv_lazy(sample_csv_path)
        result = aggregate_campaigns(lazy_df)
        expected_cols = {
            "campaign_id", "total_impressions", "total_clicks",
            "total_spend", "total_conversions", "CTR", "CPA", "_row_count"
        }
        assert set(result.columns) == expected_cols

    def test_aggregation_correct_campaign_count(self, sample_csv_path: str) -> None:
        lazy_df = load_csv_lazy(sample_csv_path)
        result = aggregate_campaigns(lazy_df)
        # 10 unique campaigns in sample data
        assert len(result) == 10

    def test_cmp001_aggregation(self, sample_csv_path: str) -> None:
        lazy_df = load_csv_lazy(sample_csv_path)
        result = aggregate_campaigns(lazy_df)
        cmp001 = result.filter(pl.col("campaign_id") == "CMP001")

        assert cmp001["total_impressions"].item() == 22000
        assert cmp001["total_clicks"].item() == 1100
        assert abs(cmp001["total_spend"].item() - 220.0) < 0.01
        assert cmp001["total_conversions"].item() == 45

    def test_ctr_calculation(self, sample_csv_path: str) -> None:
        lazy_df = load_csv_lazy(sample_csv_path)
        result = aggregate_campaigns(lazy_df)
        cmp001 = result.filter(pl.col("campaign_id") == "CMP001")

        # CTR = 1100 / 22000 = 0.05
        assert abs(cmp001["CTR"].item() - 0.05) < 0.0001

    def test_cpa_calculation(self, sample_csv_path: str) -> None:
        lazy_df = load_csv_lazy(sample_csv_path)
        result = aggregate_campaigns(lazy_df)
        cmp001 = result.filter(pl.col("campaign_id") == "CMP001")

        # CPA = 220.0 / 45 ≈ 4.889
        assert abs(cmp001["CPA"].item() - 4.889) < 0.01

    def test_zero_conversions_cpa_is_null(self, sample_csv_path: str) -> None:
        lazy_df = load_csv_lazy(sample_csv_path)
        result = aggregate_campaigns(lazy_df)
        # CMP003 has 0 conversions
        cmp003 = result.filter(pl.col("campaign_id") == "CMP003")
        assert cmp003["CPA"].item() is None


class TestGetTop10Ctr:
    """Tests for top 10 CTR selection."""

    def test_returns_max_10_rows(self, sample_aggregated_df: pl.DataFrame) -> None:
        result = get_top10_ctr(sample_aggregated_df)
        assert len(result) <= 10

    def test_sorted_by_ctr_descending(self, sample_aggregated_df: pl.DataFrame) -> None:
        result = get_top10_ctr(sample_aggregated_df)
        ctr_values = result["CTR"].to_list()
        assert ctr_values == sorted(ctr_values, reverse=True)

    def test_correct_columns(self, sample_aggregated_df: pl.DataFrame) -> None:
        result = get_top10_ctr(sample_aggregated_df)
        expected = ["campaign_id", "total_impressions", "total_clicks",
                    "total_spend", "total_conversions", "CTR", "CPA"]
        assert result.columns == expected


class TestGetTop10Cpa:
    """Tests for top 10 CPA selection."""

    def test_returns_max_10_rows(self, sample_aggregated_df: pl.DataFrame) -> None:
        result = get_top10_cpa(sample_aggregated_df)
        assert len(result) <= 10

    def test_sorted_by_cpa_ascending(self, sample_aggregated_df: pl.DataFrame) -> None:
        result = get_top10_cpa(sample_aggregated_df)
        cpa_values = result["CPA"].to_list()
        assert cpa_values == sorted(cpa_values)

    def test_excludes_zero_conversions(self, sample_aggregated_df: pl.DataFrame) -> None:
        result = get_top10_cpa(sample_aggregated_df)
        # CMP003 and CMP012 have 0 conversions, should be excluded
        campaign_ids = result["campaign_id"].to_list()
        assert "CMP003" not in campaign_ids
        assert "CMP012" not in campaign_ids

    def test_no_null_cpa(self, sample_aggregated_df: pl.DataFrame) -> None:
        result = get_top10_cpa(sample_aggregated_df)
        assert result["CPA"].null_count() == 0
