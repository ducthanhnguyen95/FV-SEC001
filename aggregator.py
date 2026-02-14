#!/usr/bin/env python3
"""Ad Performance Aggregator — Entry Point.

Process advertising campaign CSV data and generate
Top 10 CTR and Top 10 CPA reports.

Usage:
    python aggregator.py --input ad_data.csv --output results/
    python aggregator.py -i ad_data.csv -o results/ --verbose --benchmark
"""

from src.cli import main

if __name__ == "__main__":
    main()
