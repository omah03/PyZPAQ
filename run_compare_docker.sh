#!/bin/bash

ORIGINAL_DIR=""
DECOMPRESSED_DIR=""
APP_DIR="" 
LOGS_DIR="" 

mkdir -p "${LOGS_DIR}"

docker run --rm \
  -v "${ORIGINAL_DIR}:/original:ro" \
  -v "${DECOMPRESSED_DIR}:/decompressed:ro" \
  -v "${APP_DIR}:/app" \
  -v "${LOGS_DIR}:/app/logs" \
  compressor python3 /app/byte_compare.py /original /decompressed

# ./run_compare_docker.sh
