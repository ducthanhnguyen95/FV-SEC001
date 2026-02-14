---
phase: deployment
title: Deployment Strategy
description: Deployment and containerization for Ad Performance Aggregator
---

# Deployment Strategy

## Local Deployment

### Prerequisites
- Python 3.10+
- pip

### Steps
```bash
git clone <repository-url>
cd FV-SEC001
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python aggregator.py --input ad_data.csv --output results/
```

## Docker Deployment

### Build
```bash
docker build -t ad-aggregator .
```

### Run
```bash
docker run --rm \
  -v $(pwd)/ad_data.csv:/app/ad_data.csv \
  -v $(pwd)/results:/app/results \
  ad-aggregator --input ad_data.csv --output results/
```

### Docker Image Details
- Base: `python:3.12-slim`
- Size: ~150MB
- Non-root user for security
- Optimized layer caching
