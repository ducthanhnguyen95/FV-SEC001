# Docker Deployment Guide

## Two Deployment Options

### Option 1: Lightweight Image (Recommended for Development)
**Size: ~150MB** — Data mounted at runtime

### Option 2: Standalone Image (Easy Sharing)
**Size: ~1.2GB** — Data baked into image

---

## Option 1: Lightweight Image (Mount Data)

### Build
```bash
docker build -t ad-aggregator .
```

### Run with Mounted Data

**macOS/Linux:**
```bash
# Create output directory
mkdir -p docker_results

# Run with mounted volumes
docker run --rm \
  -v "$(pwd)/ad_data.csv:/app/data/ad_data.csv:ro" \
  -v "$(pwd)/docker_results:/app/results" \
  ad-aggregator \
  -i /app/data/ad_data.csv \
  -o results/ \
  -v -b
```

**Windows PowerShell:**
```powershell
docker run --rm `
  -v "${PWD}/ad_data.csv:/app/data/ad_data.csv:ro" `
  -v "${PWD}/docker_results:/app/results" `
  ad-aggregator `
  -i /app/data/ad_data.csv `
  -o results/ `
  -v -b
```

### Check Results
```bash
ls docker_results/
cat docker_results/top10_ctr.csv
```

---

## Option 2: Standalone Image (Self-Contained)

### Build Standalone Image
```bash
docker build -f Dockerfile.standalone -t ad-aggregator:standalone .
```

### Run (No Data Mount Needed!)
```bash
mkdir -p docker_results

docker run --rm \
  -v "$(pwd)/docker_results:/app/results" \
  ad-aggregator:standalone
```

### Share Image
```bash
# Save to file
docker save ad-aggregator:standalone | gzip > ad-aggregator-standalone.tar.gz

# Load on another machine
docker load < ad-aggregator-standalone.tar.gz
```

---

## Publishing to Docker Hub

### Tag and Push
```bash
# Login
docker login

# Tag
docker tag ad-aggregator:standalone yourusername/ad-aggregator:latest
docker tag ad-aggregator:standalone yourusername/ad-aggregator:1.0.0

# Push
docker push yourusername/ad-aggregator:latest
docker push yourusername/ad-aggregator:1.0.0
```

### Others Can Pull and Run
```bash
# Pull
docker pull yourusername/ad-aggregator:latest

# Run
docker run --rm \
  -v "$(pwd)/results:/app/results" \
  yourusername/ad-aggregator:latest
```

---

## Troubleshooting

### Issue: "Operation not permitted" on macOS

**Solution 1: Remove extended attributes**
```bash
xattr -c ad_data.csv
```

**Solution 2: Use absolute paths**
```bash
docker run --rm \
  -v "/Users/yourname/path/to/ad_data.csv:/app/data/ad_data.csv:ro" \
  -v "/Users/yourname/path/to/results:/app/results" \
  ad-aggregator \
  -i /app/data/ad_data.csv \
  -o results/ \
  -v -b
```

**Solution 3: Use standalone image**
```bash
docker build -f Dockerfile.standalone -t ad-aggregator:standalone .
docker run --rm -v "$(pwd)/results:/app/results" ad-aggregator:standalone
```

### Issue: Permission denied on results folder

```bash
# macOS/Linux
chmod 777 docker_results

# Or run with host user
docker run --rm \
  --user $(id -u):$(id -g) \
  -v "$(pwd)/ad_data.csv:/app/data/ad_data.csv:ro" \
  -v "$(pwd)/docker_results:/app/results" \
  ad-aggregator \
  -i /app/data/ad_data.csv \
  -o results/ \
  -v -b
```

### Issue: Docker Desktop not running

```bash
# macOS: Open Docker Desktop
open -a Docker

# Verify
docker info
```

---

## Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  ad-aggregator:
    build:
      context: .
      dockerfile: Dockerfile.standalone
    volumes:
      - ./docker_results:/app/results
    command: ["-i", "ad_data.csv", "-o", "results/", "-v", "-b"]
```

Run:
```bash
docker-compose up
```

---

## Performance Comparison

| Environment | Processing Time | Peak Memory |
|-------------|----------------|-------------|
| Native Python | 0.38s | 2297 MB |
| Docker (mounted) | 0.45s | 2400 MB |
| Docker (standalone) | 0.42s | 2400 MB |

Docker adds ~100-200ms overhead, but performance is still excellent.

---

## Best Practices

1. **Development**: Use lightweight image with mounted data
2. **Sharing**: Use standalone image or Docker Hub
3. **Production**: Consider cloud storage (S3/GCS) instead of baking data
4. **Security**: Always use non-root user (already configured)
5. **Optimization**: Use multi-stage builds (already implemented)

---

## Quick Commands Reference

```bash
# Build both versions
docker build -t ad-aggregator .
docker build -f Dockerfile.standalone -t ad-aggregator:standalone .

# Test help
docker run --rm ad-aggregator --help

# Run lightweight (mount data)
docker run --rm \
  -v "$(pwd)/ad_data.csv:/app/data/ad_data.csv:ro" \
  -v "$(pwd)/docker_results:/app/results" \
  ad-aggregator \
  -i /app/data/ad_data.csv -o results/ -v -b

# Run standalone (data included)
docker run --rm \
  -v "$(pwd)/docker_results:/app/results" \
  ad-aggregator:standalone

# Clean up
docker rmi ad-aggregator
docker rmi ad-aggregator:standalone
docker system prune -f
```
