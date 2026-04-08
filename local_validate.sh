#!/usr/bin/env bash
set -uo pipefail

PING_URL="http://localhost:7860"
REPO_DIR="."

echo "Step 1/3: Pinging HF Space ($PING_URL/reset) ..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{}' "$PING_URL/reset" --max-time 30 2>/dev/null || printf "000")
echo "HTTP_CODE: $HTTP_CODE"

echo "Step 2/3: Running docker build ..."
docker build "$REPO_DIR"

echo "Step 3/3: Running openenv validate ..."
openenv validate
