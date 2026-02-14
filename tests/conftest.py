"""Pytest fixtures for Ad Performance Aggregator tests."""

import os
import tempfile
from pathlib import Path

import polars as pl
import pytest


SAMPLE_CSV_CONTENT = """campaign_id,date,impressions,clicks,spend,conversions
CMP001,2025-01-01,10000,500,100.00,20
CMP001,2025-01-02,12000,600,120.00,25
CMP002,2025-01-01,8000,100,50.00,5
CMP002,2025-01-02,9000,120,60.00,8
CMP003,2025-01-01,15000,300,200.00,0
CMP003,2025-01-02,16000,320,210.00,0
CMP004,2025-01-01,5000,400,80.00,30
CMP004,2025-01-02,6000,500,90.00,35
CMP005,2025-01-01,20000,200,300.00,10
CMP005,2025-01-02,22000,220,320.00,12
CMP006,2025-01-01,7000,350,60.00,15
CMP007,2025-01-01,30000,900,150.00,50
CMP008,2025-01-01,25000,250,500.00,5
CMP009,2025-01-01,18000,720,90.00,40
CMP010,2025-01-01,11000,110,400.00,3
"""

# Expected aggregated values for CMP001:
# total_impressions = 10000 + 12000 = 22000
# total_clicks = 500 + 600 = 1100
# total_spend = 100.00 + 120.00 = 220.00
# total_conversions = 20 + 25 = 45
# CTR = 1100 / 22000 = 0.05
# CPA = 220.00 / 45 = 4.888...


@pytest.fixture
def sample_csv_path(tmp_path: Path) -> str:
    """Create a temporary sample CSV file."""
    csv_path = tmp_path / "test_data.csv"
    csv_path.write_text(SAMPLE_CSV_CONTENT)
    return str(csv_path)


@pytest.fixture
def empty_csv_path(tmp_path: Path) -> str:
    """Create an empty CSV file."""
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("")
    return str(csv_path)


@pytest.fixture
def output_dir(tmp_path: Path) -> str:
    """Create a temporary output directory."""
    out = tmp_path / "output"
    out.mkdir()
    return str(out)


@pytest.fixture
def sample_aggregated_df() -> pl.DataFrame:
    """Create a pre-aggregated DataFrame for testing sort/filter logic."""
    return pl.DataFrame({
        "campaign_id": [f"CMP{str(i).zfill(3)}" for i in range(1, 13)],
        "total_impressions": [22000, 17000, 31000, 11000, 42000, 7000, 30000, 25000, 18000, 11000, 50000, 60000],
        "total_clicks": [1100, 220, 620, 900, 420, 350, 900, 250, 720, 110, 1500, 600],
        "total_spend": [220.0, 110.0, 410.0, 170.0, 620.0, 60.0, 150.0, 500.0, 90.0, 400.0, 250.0, 300.0],
        "total_conversions": [45, 13, 0, 65, 22, 15, 50, 5, 40, 3, 80, 0],
        "_row_count": [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1],
        "CTR": [0.05, 0.01294, 0.02, 0.08182, 0.01, 0.05, 0.03, 0.01, 0.04, 0.01, 0.03, 0.01],
        "CPA": [4.889, 8.462, None, 2.615, 28.182, 4.0, 3.0, 100.0, 2.25, 133.333, 3.125, None],
    })
