# Multi-stage build for Ad Performance Aggregator
# This Dockerfile expects data to be mounted at runtime
# Usage: docker run -v $(pwd)/ad_data.csv:/app/data/ad_data.csv:ro -v $(pwd)/results:/app/results ad-aggregator

# Stage 1: Install dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --target=/app/deps -r requirements.txt

# Stage 2: Runtime image
FROM python:3.12-slim

# Security: run as non-root user with specific UID/GID for better compatibility
RUN groupadd -g 1000 appuser && \
    useradd -u 1000 -g appuser --create-home --shell /bin/bash appuser

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /app/deps /usr/local/lib/python3.12/site-packages/

# Copy application code
COPY aggregator.py .
COPY src/ src/

# Create directories with proper permissions
RUN mkdir -p /app/data /app/results && \
    chown -R appuser:appuser /app

USER appuser

ENTRYPOINT ["python", "aggregator.py"]
CMD ["--help"]
