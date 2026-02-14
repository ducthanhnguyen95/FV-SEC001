"""CLI interface for the Ad Performance Aggregator.

Provides a Click-based command-line interface for processing
advertising campaign data and generating performance reports.
"""

import sys
import click

from src.reader import load_csv_lazy, get_file_size_mb
from src.aggregator import aggregate_campaigns, get_top10_ctr, get_top10_cpa, get_total_row_count
from src.writer import write_results
from src.benchmarker import Benchmarker


def _print_success(msg: str) -> None:
    """Print a success message in green."""
    click.secho(f"  ✓ {msg}", fg="green")


def _print_info(msg: str) -> None:
    """Print an info message in blue."""
    click.secho(f"  ℹ {msg}", fg="blue")


def _print_error(msg: str) -> None:
    """Print an error message in red."""
    click.secho(f"  ✗ {msg}", fg="red", err=True)


@click.command(
    help="Ad Performance Aggregator — Process advertising CSV data and generate Top 10 campaign reports."
)
@click.option(
    "--input", "-i",
    "input_file",
    required=True,
    type=click.Path(exists=True),
    help="Path to the input CSV file (e.g., ad_data.csv)",
)
@click.option(
    "--output", "-o",
    "output_dir",
    default="results",
    type=click.Path(),
    help="Output directory for result CSV files (default: results/)",
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    default=False,
    help="Enable verbose output with progress details",
)
@click.option(
    "--benchmark", "-b",
    is_flag=True,
    default=False,
    help="Display performance benchmark after processing",
)
def main(input_file: str, output_dir: str, verbose: bool, benchmark: bool) -> None:
    """Main entry point for the Ad Performance Aggregator CLI."""
    click.echo()
    click.secho("  Ad Performance Aggregator", fg="cyan", bold=True)
    click.secho("  ========================", fg="cyan")
    click.echo()

    bench = Benchmarker()

    try:
        with bench:
            # Step 1: Read CSV
            if verbose:
                _print_info(f"Reading input file: {input_file}")
                _print_info(f"File size: {get_file_size_mb(input_file)} MB")

            lazy_df = load_csv_lazy(input_file)
            _print_success("CSV file loaded (lazy mode)")

            # Step 2: Aggregate
            if verbose:
                _print_info("Aggregating campaign data...")

            aggregated_df = aggregate_campaigns(lazy_df)
            num_campaigns = len(aggregated_df)
            _print_success(f"Aggregated {num_campaigns} campaigns")

            # Step 3: Compute Top 10
            top10_ctr = get_top10_ctr(aggregated_df)
            top10_cpa = get_top10_cpa(aggregated_df)
            _print_success("Computed Top 10 CTR and Top 10 CPA")

            # Step 4: Write results
            if verbose:
                _print_info(f"Writing results to: {output_dir}/")

            ctr_path, cpa_path = write_results(top10_ctr, top10_cpa, output_dir)
            _print_success(f"Written: {ctr_path}")
            _print_success(f"Written: {cpa_path}")

            # Set benchmark metadata (row count derived from aggregation, no re-scan)
            bench.set_metadata(
                input_file_size_mb=get_file_size_mb(input_file),
                rows_processed=get_total_row_count(aggregated_df),
                unique_campaigns=num_campaigns,
            )

        click.echo()
        _print_success("Processing complete!")

        if benchmark:
            click.echo(bench.result.display())

    except FileNotFoundError as e:
        _print_error(str(e))
        sys.exit(1)
    except ValueError as e:
        _print_error(str(e))
        sys.exit(1)
    except Exception as e:
        _print_error(f"Unexpected error: {e}")
        sys.exit(1)
