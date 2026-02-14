"""Integration tests for the full pipeline."""

import os

import polars as pl
import pytest

from src.reader import load_csv_lazy
from src.aggregator import aggregate_campaigns, get_top10_ctr, get_top10_cpa
from src.writer import write_results


class TestFullPipeline:
    """End-to-end integration tests."""

    def test_full_pipeline(self, sample_csv_path: str, output_dir: str) -> None:
        """Test the complete pipeline from CSV to output files."""
        # Step 1: Read
        lazy_df = load_csv_lazy(sample_csv_path)

        # Step 2: Aggregate
        aggregated = aggregate_campaigns(lazy_df)
        assert len(aggregated) == 10  # 10 unique campaigns

        # Step 3: Top 10
        top10_ctr = get_top10_ctr(aggregated)
        top10_cpa = get_top10_cpa(aggregated)

        assert len(top10_ctr) == 10  # We have exactly 10 campaigns
        assert len(top10_cpa) <= 10

        # Step 4: Write
        ctr_path, cpa_path = write_results(top10_ctr, top10_cpa, output_dir)

        # Verify files
        assert os.path.exists(ctr_path)
        assert os.path.exists(cpa_path)

        # Verify content
        ctr_df = pl.read_csv(ctr_path)
        cpa_df = pl.read_csv(cpa_path)

        assert "campaign_id" in ctr_df.columns
        assert "CTR" in ctr_df.columns
        assert "CPA" in cpa_df.columns

        # CTR should be sorted descending
        ctr_values = ctr_df["CTR"].to_list()
        assert ctr_values == sorted(ctr_values, reverse=True)

        # CPA should be sorted ascending
        cpa_values = cpa_df["CPA"].to_list()
        assert cpa_values == sorted(cpa_values)

    def test_pipeline_with_zero_conversion_exclusion(
        self, sample_csv_path: str, output_dir: str
    ) -> None:
        """Test that zero-conversion campaigns are excluded from CPA ranking."""
        lazy_df = load_csv_lazy(sample_csv_path)
        aggregated = aggregate_campaigns(lazy_df)
        top10_cpa = get_top10_cpa(aggregated)

        # CMP003 has 0 conversions, should not appear in CPA results
        campaign_ids = top10_cpa["campaign_id"].to_list()
        assert "CMP003" not in campaign_ids

        # All CPA values should be non-null
        assert top10_cpa["CPA"].null_count() == 0
