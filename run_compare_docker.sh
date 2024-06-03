#!/bin/bash

ORIGINAL_DIR="/media/dc-04-vol03/HBR/storage/P24001_Test"
DECOMPRESSED_DIR="/media/dc-04-vol03/omar/input"
APP_DIR="/media/dc-04-vol03/omar" 
LOGS_DIR="/media/dc-04-vol03/omar/logs" 

mkdir -p "${LOGS_DIR}"

docker run --rm \
  -v "${ORIGINAL_DIR}:/original:ro" \
  -v "${DECOMPRESSED_DIR}:/decompressed:ro" \
  -v "${APP_DIR}:/app" \
  -v "${LOGS_DIR}:/app/logs" \
  compressor python3 /app/byte_compare.py /original /decompressed

# ./run_compare_docker.sh
