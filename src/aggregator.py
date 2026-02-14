"""Aggregation module for campaign performance data.

Handles grouping by campaign_id and computing all aggregate metrics
including CTR and CPA in a single optimized pass.
"""

import polars as pl


def aggregate_campaigns(lazy_df: pl.LazyFrame) -> pl.DataFrame:
    """Aggregate campaign data and compute performance metrics.

    Performs a single-pass groupby aggregation to compute:
    - total_impressions: sum of all impressions per campaign
    - total_clicks: sum of all clicks per campaign
    - total_spend: sum of all spend per campaign
    - total_conversions: sum of all conversions per campaign
    - CTR: total_clicks / total_impressions
    - CPA: total_spend / total_conversions (null if conversions = 0)

    Args:
        lazy_df: Polars LazyFrame with campaign data.

    Returns:
        Materialized DataFrame with aggregated metrics per campaign.
    """
    result = (
        lazy_df
        .group_by("campaign_id")
        .agg(
            pl.col("impressions").sum().alias("total_impressions"),
            pl.col("clicks").sum().alias("total_clicks"),
            pl.col("spend").sum().alias("total_spend"),
            pl.col("conversions").sum().alias("total_conversions"),
            pl.len().alias("_row_count"),
        )
        .with_columns(
            (pl.col("total_clicks") / pl.col("total_impressions")).alias("CTR"),
            pl.when(pl.col("total_conversions") > 0)
            .then(pl.col("total_spend") / pl.col("total_conversions"))
            .otherwise(None)
            .alias("CPA"),
        )
        .collect()
    )

    return result


def get_total_row_count(aggregated_df: pl.DataFrame) -> int:
    """Get total number of input rows from the aggregated DataFrame.

    Each group stores its row count in _row_count column.

    Args:
        aggregated_df: DataFrame with _row_count column.

    Returns:
        Total number of rows processed.
    """
    return int(aggregated_df["_row_count"].sum())


def get_top10_ctr(df: pl.DataFrame) -> pl.DataFrame:
    """Get top 10 campaigns by highest Click-Through Rate.

    Args:
        df: Aggregated DataFrame with CTR column.

    Returns:
        DataFrame with top 10 campaigns sorted by CTR descending.
    """
    return (
        df
        .sort("CTR", descending=True)
        .head(10)
        .select([
            "campaign_id",
            "total_impressions",
            "total_clicks",
            "total_spend",
            "total_conversions",
            "CTR",
            "CPA",
        ])
    )


def get_top10_cpa(df: pl.DataFrame) -> pl.DataFrame:
    """Get top 10 campaigns by lowest Cost Per Acquisition.

    Excludes campaigns with zero conversions.

    Args:
        df: Aggregated DataFrame with CPA column.

    Returns:
        DataFrame with top 10 campaigns sorted by CPA ascending.
    """
    return (
        df
        .filter(pl.col("total_conversions") > 0)
        .sort("CPA", descending=False)
        .head(10)
        .select([
            "campaign_id",
            "total_impressions",
            "total_clicks",
            "total_spend",
            "total_conversions",
            "CTR",
            "CPA",
        ])
    )
