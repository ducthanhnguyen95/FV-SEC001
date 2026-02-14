---
phase: testing
title: Testing Strategy
description: Testing approach for Ad Performance Aggregator
---

# Testing Strategy

## Test Coverage Goals
- Unit test coverage: >90%
- Integration test: Full pipeline end-to-end
- Performance test: Benchmark against 1GB file

## Unit Tests

### Reader Module (`test_reader.py`)
- [x] Load valid CSV file
- [x] Validate schema (correct columns and types)
- [x] Handle missing file gracefully
- [x] Handle empty file

### Aggregator Module (`test_aggregator.py`)
- [x] Correct aggregation of impressions, clicks, spend, conversions
- [x] CTR calculation accuracy
- [x] CPA calculation accuracy
- [x] CPA with zero conversions returns null
- [x] Multiple dates aggregated per campaign

### Writer Module (`test_writer.py`)
- [x] Top 10 CTR output format
- [x] Top 10 CPA output format
- [x] CPA excludes zero-conversion campaigns
- [x] CSV header correctness
- [x] Output directory creation

## Integration Tests (`test_integration.py`)
- [x] End-to-end pipeline with sample data
- [x] Output files exist and are valid CSV
- [x] Results match expected values

## Performance Tests
- [x] Process full 1GB dataset
- [x] Measure processing time
- [x] Measure peak memory usage
- [x] Verify throughput metrics

## Test Data
- `tests/conftest.py`: Pytest fixtures with sample campaign data
- 10 campaigns, 50 records, known expected results
