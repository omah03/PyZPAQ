#!/bin/bash

INPUT_DIR="" 
OUTPUT_DIR=""
APP_DIR=""
LOGS_DIR=""

mkdir -p "${LOGS_DIR}"

docker run --rm \
  -v "${INPUT_DIR}:/input:ro" \
  -v "${OUTPUT_DIR}:/output" \
  -v "${APP_DIR}:/app" \
  -v "${LOGS_DIR}:/app/logs" \
  compressor python3 /app/compress.py /input /output P24001_Test
