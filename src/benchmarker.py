"""Benchmarking module for tracking performance metrics.

Uses resource module for accurate memory tracking (including native/Rust allocations)
and time.perf_counter for high-resolution timing.
Designed as a context manager for clean usage.
"""

import resource
import time
from dataclasses import dataclass


@dataclass
class BenchmarkResult:
    """Container for benchmark results."""
    processing_time_sec: float = 0.0
    peak_memory_mb: float = 0.0
    input_file_size_mb: float = 0.0
    rows_processed: int = 0
    unique_campaigns: int = 0

    @property
    def throughput(self) -> float:
        """Rows processed per second."""
        if self.processing_time_sec > 0:
            return self.rows_processed / self.processing_time_sec
        return 0.0

    def display(self) -> str:
        """Format benchmark results for display."""
        separator = "=" * 60
        return (
            f"\n{separator}\n"
            f"  BENCHMARK RESULTS\n"
            f"{separator}\n"
            f"  Input file size  : {self.input_file_size_mb:.1f} MB\n"
            f"  Rows processed   : {self.rows_processed:,}\n"
            f"  Unique campaigns : {self.unique_campaigns:,}\n"
            f"  Processing time  : {self.processing_time_sec:.2f} seconds\n"
            f"  Peak memory      : {self.peak_memory_mb:.1f} MB\n"
            f"  Throughput       : {self.throughput:,.0f} rows/sec\n"
            f"{separator}\n"
        )


class Benchmarker:
    """Context manager for benchmarking processing performance.

    Uses resource.getrusage() to measure peak RSS (Resident Set Size),
    which captures memory from all allocations including native/Rust
    libraries like Polars.

    Usage:
        bench = Benchmarker()
        with bench:
            # ... processing code ...
        print(bench.result.display())
    """

    def __init__(self) -> None:
        self._start_time: float = 0.0
        self._start_memory: int = 0
        self._result = BenchmarkResult()

    @property
    def result(self) -> BenchmarkResult:
        return self._result

    def __enter__(self) -> "Benchmarker":
        self._start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        self._start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._result.processing_time_sec = time.perf_counter() - self._start_time
        peak_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        # macOS reports in bytes, Linux in kilobytes
        import platform
        if platform.system() == "Darwin":
            self._result.peak_memory_mb = peak_rss / (1024 * 1024)
        else:
            self._result.peak_memory_mb = peak_rss / 1024

    def set_metadata(
        self,
        input_file_size_mb: float = 0.0,
        rows_processed: int = 0,
        unique_campaigns: int = 0,
    ) -> None:
        """Set additional metadata for the benchmark report.

        Args:
            input_file_size_mb: Size of input file in MB.
            rows_processed: Number of rows processed.
            unique_campaigns: Number of unique campaign_ids.
        """
        self._result.input_file_size_mb = input_file_size_mb
        self._result.rows_processed = rows_processed
        self._result.unique_campaigns = unique_campaigns
