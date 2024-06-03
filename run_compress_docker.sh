#!/bin/bash

INPUT_DIR="/media/dc-04-vol03/HBR/storage/P24001_Test" 
OUTPUT_DIR="/media/dc-04-vol03/omar"
APP_DIR="/media/dc-04-vol03/omar"
LOGS_DIR="/media/dc-04-vol03/omar/logs"

mkdir -p "${LOGS_DIR}"

docker run --rm \
  -v "${INPUT_DIR}:/input:ro" \
  -v "${OUTPUT_DIR}:/output" \
  -v "${APP_DIR}:/app" \
  -v "${LOGS_DIR}:/app/logs" \
  compressor python3 /app/compress.py /input /output P24001_Test
