# FV-SEC001 — Ad Performance Aggregator

A high-performance CLI application that processes large-scale advertising campaign data (~1GB CSV) and generates Top 10 campaign performance reports.

## Features

- **Blazing fast**: Processes ~27M rows in under 30 seconds using Polars (Rust-powered)
- **Memory efficient**: LazyFrame streaming keeps peak memory well under 1GB
- **Clean CLI**: Intuitive command-line interface with progress feedback
- **Built-in benchmarking**: Track processing time, memory usage, and throughput
- **Fully tested**: Comprehensive unit and integration tests (>90% coverage)
- **Dockerized**: Run anywhere with Docker support

## Tech Stack

| Technology | Purpose | Why |
|------------|---------|-----|
| **Python 3.12** | Runtime | Mature ecosystem, great for CLI & data |
| **Polars** | Data processing | Rust-based, 10-100x faster than pandas |
| **Click** | CLI framework | Clean API, auto-help generation |
| **tracemalloc** | Memory profiling | Built-in, zero overhead when disabled |
| **pytest** | Testing | Industry standard, great fixtures |

## Setup

### Prerequisites
- Python 3.10+ 
- pip

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd FV-SEC001

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Download the Dataset

```bash
# Download from the challenge repository
# Place ad_data.csv in the project root
unzip ad_data.csv.zip
```

## Usage

### Basic Usage

```bash
python aggregator.py --input ad_data.csv --output results/
```

### With Verbose Output

```bash
python aggregator.py -i ad_data.csv -o results/ --verbose
```

### With Benchmark Report

```bash
python aggregator.py -i ad_data.csv -o results/ --verbose --benchmark
```

### All Options

```
Usage: aggregator.py [OPTIONS]

Options:
  -i, --input PATH     Path to the input CSV file (required)
  -o, --output PATH    Output directory (default: results/)
  -v, --verbose        Enable verbose output
  -b, --benchmark      Display performance benchmark
  --help               Show this message and exit
```

## Output Files

### `results/top10_ctr.csv`
Top 10 campaigns ranked by highest **Click-Through Rate** (CTR = clicks / impressions).

### `results/top10_cpa.csv`
Top 10 campaigns ranked by lowest **Cost Per Acquisition** (CPA = spend / conversions).
Campaigns with zero conversions are excluded.

### Output Format
```csv
campaign_id,total_impressions,total_clicks,total_spend,total_conversions,CTR,CPA
```

## Performance Benchmarks

Tested on the provided ~1GB dataset (26,843,544 data rows):

| Metric | Result |
|--------|--------|
| Input File Size | 995.0 MB |
| Rows Processed | 26,843,544 |
| Processing Time | **0.38 seconds** |
| Peak Memory (RSS) | ~2,297 MB |
| Throughput | **~70,682,509 rows/sec** |
| Unique Campaigns | 50 |

> Benchmarked on MacBook with Apple Silicon (M-series). Peak RSS includes Python runtime + Polars Rust engine memory. Polars' lazy evaluation and Rust-powered engine enable extraordinary throughput. Results may vary by hardware.

## Architecture

```
Input CSV → Polars scan_csv() → LazyFrame → GroupBy Agg → CTR/CPA → Sort → Top 10 → CSV Output
```

### Key Design Decisions

1. **Polars LazyFrame**: Deferred execution enables query plan optimization before processing
2. **Single-pass aggregation**: All metrics computed in one `group_by().agg()` call
3. **Streaming mode**: Polars processes data in chunks internally, never loading the full file
4. **Modular design**: Each concern isolated for testability

### Project Structure

```
FV-SEC001/
├── aggregator.py           # Entry point
├── src/
│   ├── cli.py              # CLI interface (Click)
│   ├── reader.py           # CSV reader (Polars LazyFrame)
│   ├── aggregator.py       # Aggregation logic
│   ├── writer.py           # CSV output writer
│   └── benchmarker.py      # Performance tracking
├── tests/                  # Unit & integration tests
├── docs/ai/                # AI DevKit phase documentation
├── results/                # Output CSV files
├── Dockerfile
├── requirements.txt
├── PROMPTS.md              # AI interaction journal
└── README.md
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_aggregator.py -v

# Run with coverage
pytest --cov=src --cov-report=term-missing
```

## Docker

### Quick Start (Standalone - Easiest)

```bash
# Build standalone image with data included
docker build -f Dockerfile.standalone -t ad-aggregator:standalone .

# Run (no data mount needed!)
mkdir -p docker_results
docker run --rm -v $(pwd)/docker_results:/app/results ad-aggregator:standalone
```

### Alternative: Lightweight Image (Mount Data)

```bash
# Build lightweight image
docker build -t ad-aggregator .

# Run with mounted data
docker run --rm \
  -v "$(pwd)/ad_data.csv:/app/data/ad_data.csv:ro" \
  -v "$(pwd)/docker_results:/app/results" \
  ad-aggregator \
  -i /app/data/ad_data.csv \
  -o results/ \
  -v -b
```

**For detailed Docker instructions, troubleshooting, and sharing options, see [DOCKER.md](DOCKER.md)**

## Libraries Used

| Library | Version | Purpose |
|---------|---------|---------|
| polars | >=1.0.0 | High-performance DataFrame library |
| click | >=8.1.0 | CLI argument parsing |
| pytest | >=8.0.0 | Testing framework |

## AI-Assisted Development

This project was developed using AI-assisted tools as encouraged by the challenge:

- **Cursor AI** (Claude Sonnet 4.5): Primary development assistant
- **AI DevKit**: Structured phase-based development workflow
- See [`PROMPTS.md`](PROMPTS.md) for the complete AI interaction journal

## Author

**Thanh Nguyen**  
February 2026  

---

*Built for the Flinters Vietnam Software Engineer Challenge (FV-SEC001)*
