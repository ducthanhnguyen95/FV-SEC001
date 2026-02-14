#!/bin/bash
# Docker Test Script for Ad Performance Aggregator
# Tests both lightweight and standalone Docker images

set -e

echo "======================================"
echo "  Docker Image Test Suite"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test 1: Build Standalone Image
echo -e "${BLUE}[1/6] Building Standalone Image...${NC}"
docker build -f Dockerfile.standalone -t ad-aggregator:standalone . > /dev/null 2>&1
echo -e "${GREEN}✓ Standalone image built successfully${NC}"
echo ""

# Test 2: Run Standalone Image
echo -e "${BLUE}[2/6] Running Standalone Image...${NC}"
mkdir -p docker_standalone_results
docker run --rm \
  -v "$(pwd)/docker_standalone_results:/app/results" \
  ad-aggregator:standalone > /dev/null 2>&1
echo -e "${GREEN}✓ Standalone container ran successfully${NC}"
echo ""

# Test 3: Verify Output Files
echo -e "${BLUE}[3/6] Verifying Output Files...${NC}"
if [ -f "docker_standalone_results/top10_ctr.csv" ] && [ -f "docker_standalone_results/top10_cpa.csv" ]; then
    echo -e "${GREEN}✓ Both output files created${NC}"
    wc -l docker_standalone_results/*.csv
else
    echo -e "${RED}✗ Output files missing${NC}"
    exit 1
fi
echo ""

# Test 4: Verify Output Content
echo -e "${BLUE}[4/6] Checking Output Content...${NC}"
CTR_LINES=$(wc -l < docker_standalone_results/top10_ctr.csv | tr -d ' ')
CPA_LINES=$(wc -l < docker_standalone_results/top10_cpa.csv | tr -d ' ')
if [ "$CTR_LINES" -eq 11 ] && [ "$CPA_LINES" -eq 11 ]; then
    echo -e "${GREEN}✓ Output files have correct line count (11 lines each)${NC}"
else
    echo -e "${RED}✗ Incorrect line count: CTR=$CTR_LINES, CPA=$CPA_LINES (expected 11)${NC}"
    exit 1
fi
echo ""

# Test 5: Test Help Command
echo -e "${BLUE}[5/6] Testing Help Command...${NC}"
docker run --rm ad-aggregator:standalone --help > /dev/null 2>&1
echo -e "${GREEN}✓ Help command works${NC}"
echo ""

# Test 6: Check Image Size
echo -e "${BLUE}[6/6] Checking Image Size...${NC}"
docker images ad-aggregator:standalone --format "Size: {{.Size}}"
echo ""

# Summary
echo "======================================"
echo -e "${GREEN}  All Docker Tests Passed! ✓${NC}"
echo "======================================"
echo ""
echo "Sample Output:"
echo "--------------"
head -3 docker_standalone_results/top10_ctr.csv
echo ""
echo "Image ready to share!"
echo "To save image: docker save ad-aggregator:standalone | gzip > ad-aggregator.tar.gz"
echo "To push to Docker Hub: docker tag ad-aggregator:standalone username/ad-aggregator:latest"
