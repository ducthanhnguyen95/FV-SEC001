---
phase: implementation
title: Implementation Guide
description: Technical implementation details for Ad Performance Aggregator
---

# Implementation Guide

## Development Setup

### Prerequisites
- Python 3.10+
- pip (package manager)

### Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Code Structure
```
FV-SEC001/
├── aggregator.py           # Main entry point
├── src/
│   ├── __init__.py
│   ├── cli.py              # CLI interface (Click)
│   ├── reader.py           # CSV reader (Polars LazyFrame)
│   ├── aggregator.py       # Aggregation logic
│   ├── writer.py           # CSV output writer
│   └── benchmarker.py      # Performance tracking
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Test fixtures
│   ├── test_reader.py
│   ├── test_aggregator.py
│   ├── test_writer.py
│   └── test_integration.py
├── results/                # Output directory
├── docs/ai/                # AI DevKit documentation
├── requirements.txt
├── Dockerfile
├── README.md
└── PROMPTS.md
```

## Core Implementation Details

### Reader (`src/reader.py`)
- Uses `pl.scan_csv()` for lazy loading
- Validates expected columns exist
- Returns `pl.LazyFrame` for deferred execution

### Aggregator (`src/aggregator.py`)
- Single `groupby('campaign_id').agg(...)` operation
- Calculates CTR and CPA as derived columns
- Handles zero-conversion edge case for CPA

### Writer (`src/writer.py`)
- Sorts and filters aggregated data
- Top 10 CTR: sort by CTR descending
- Top 10 CPA: filter conversions > 0, sort by CPA ascending
- Writes standard CSV output

### Benchmarker (`src/benchmarker.py`)
- Context manager pattern for timing
- Uses `tracemalloc` for memory tracking
- Reports: time, peak memory, throughput

### CLI (`src/cli.py`)
- Click-based argument parsing
- Options: --input, --output, --verbose, --benchmark
- Colored output for readability

## Performance Considerations
- **Lazy evaluation**: `scan_csv()` builds query plan, `collect()` executes
- **Single pass**: One groupby for all aggregations
- **Streaming**: Polars can process data in chunks internally
- **No intermediate copies**: All operations chained on LazyFrame
