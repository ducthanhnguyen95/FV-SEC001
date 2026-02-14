# 🐳 Docker Quick Start - 2 Phút Setup

## ✅ Cách Dễ Nhất (Recommended)

### Bước 1: Build Image Standalone
```bash
cd /Users/thanhnd/Documents/self-project/FV-SEC001
docker build -f Dockerfile.standalone -t ad-aggregator:standalone .
```

### Bước 2: Chạy (Không cần mount data!)
```bash
mkdir -p docker_results
docker run --rm -v $(pwd)/docker_results:/app/results ad-aggregator:standalone
```

### Bước 3: Xem Kết Quả
```bash
ls -lh docker_results/
head docker_results/top10_ctr.csv
```

**Done! ✨**

---

## 📤 Share Image Với Người Khác

### Option 1: Docker Hub (Best)

```bash
# Login Docker Hub
docker login

# Tag image
docker tag ad-aggregator:standalone yourusername/ad-aggregator:latest

# Push
docker push yourusername/ad-aggregator:latest
```

**Người khác pull và chạy:**
```bash
docker pull yourusername/ad-aggregator:latest
mkdir -p results
docker run --rm -v $(pwd)/results:/app/results yourusername/ad-aggregator:latest
```

---

### Option 2: Save as File

```bash
# Save to file (~2.2GB compressed)
docker save ad-aggregator:standalone | gzip > ad-aggregator.tar.gz

# Copy file to another machine, then load:
docker load < ad-aggregator.tar.gz

# Run
docker run --rm -v $(pwd)/results:/app/results ad-aggregator:standalone
```

---

## 🧪 Test Script

Chạy full test suite:
```bash
./test_docker.sh
```

---

## 📊 Image Sizes

| Image | Size | Use Case |
|-------|------|----------|
| `ad-aggregator:latest` | 327 MB | Development (mount data) |
| `ad-aggregator:standalone` | 2.41 GB | Production/Sharing (data included) |

---

## ❓ Troubleshooting

### "Cannot connect to Docker daemon"
```bash
# macOS: Mở Docker Desktop
open -a Docker
```

### "Permission denied" trên results/
```bash
chmod 777 docker_results
```

### Xem chi tiết lỗi
```bash
docker run --rm -v $(pwd)/docker_results:/app/results ad-aggregator:standalone 2>&1
```

---

## 🎯 Benchmark Results

| Metric | Value |
|--------|-------|
| Processing Time | 0.64 seconds |
| Throughput | 41.8M rows/sec |
| Peak Memory | 2.37 GB |
| Docker Overhead | ~0.26s (~40% slower than native) |

Native Python: 0.38s  
Docker: 0.64s  
Still excellent performance! ⚡

---

## ✅ Checklist For Sharing

- [ ] Build standalone image
- [ ] Test locally (`docker run`)
- [ ] Verify output files correct
- [ ] Tag with your username
- [ ] Push to Docker Hub
- [ ] Share Docker Hub link
- [ ] Document usage in README

**Docker Hub Command:**
```bash
docker pull yourusername/ad-aggregator:latest
docker run --rm -v $(pwd)/results:/app/results yourusername/ad-aggregator:latest
```

Done! 🚀
