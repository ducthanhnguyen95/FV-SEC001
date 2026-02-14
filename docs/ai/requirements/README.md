---
phase: requirements
title: Requirements & Problem Understanding
description: FV-SEC001 Ad Performance Aggregator - Requirements Analysis
---

# Requirements & Problem Understanding

## Problem Statement
**What problem are we solving?**

- Process a large CSV dataset (~1GB, ~26.8M rows) of advertising performance records
- Aggregate data by campaign_id and compute key performance metrics
- Generate two ranked result files: Top 10 CTR and Top 10 CPA campaigns
- Build a CLI application that handles large datasets efficiently

## Goals & Objectives
**What do we want to achieve?**

### Primary Goals
- Parse and process `ad_data.csv` (995MB, 26,843,545 rows) correctly
- Aggregate metrics per campaign_id: total impressions, clicks, spend, conversions
- Calculate derived metrics: CTR (Click-Through Rate) and CPA (Cost Per Acquisition)
- Output `top10_ctr.csv` and `top10_cpa.csv` in specified format

### Secondary Goals
- Achieve sub-30 second processing time
- Keep peak memory usage under 1GB
- Provide benchmark reporting (time, memory, throughput)
- Dockerized deployment

### Non-Goals
- No web interface needed (CLI only)
- No real-time processing
- No data visualization

## Input Data Specification

### CSV Schema
| Column         | Type    | Description                   |
|----------------|---------|-------------------------------|
| campaign_id    | string  | Campaign identifier (e.g., CMP001) |
| date           | string  | Date in YYYY-MM-DD format     |
| impressions    | integer | Number of ad impressions       |
| clicks         | integer | Number of ad clicks            |
| spend          | float   | Advertising cost in USD        |
| conversions    | integer | Number of conversions          |

### Data Characteristics
- File size: ~995MB (uncompressed)
- Total rows: 26,843,545 (including header)
- Multiple dates per campaign
- Multiple campaigns (CMP001 - CMP050+)

## Output Specification

### File 1: `top10_ctr.csv`
Top 10 campaigns with highest CTR, sorted descending by CTR.

### File 2: `top10_cpa.csv`
Top 10 campaigns with lowest CPA, sorted ascending by CPA.
Campaigns with zero conversions are excluded.

### Output Columns
`campaign_id, total_impressions, total_clicks, total_spend, total_conversions, CTR, CPA`

## Metric Definitions
- **CTR** (Click-Through Rate) = total_clicks / total_impressions
- **CPA** (Cost Per Acquisition) = total_spend / total_conversions
  - If total_conversions = 0, CPA = null (exclude from top10_cpa)

## Success Criteria
- Correct aggregation verified against manual spot-checks
- Processing time < 60 seconds (target < 30s)
- Peak memory < 2GB (target < 1GB)
- Clean, maintainable code with type hints
- Comprehensive test coverage (>90%)
- Professional documentation

## Constraints & Assumptions
- Single machine processing (no distributed computing)
- File fits on local disk
- Python 3.10+ runtime
- CSV is well-formed (no malformed rows expected, but handle gracefully)
