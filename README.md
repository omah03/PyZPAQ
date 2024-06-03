# PyZPAQ
ZPAQ implementation in python based on https://github.com/zpaq/zpaq/releases

This project provides a suite of tools for compressing, decompressing, and comparing files using the ZPAQ compression algorithm. It includes Python scripts for each operation, Docker containers for environment consistency, and shell scripts for easy execution.

## Overview
The project contains the following components:

- compress.py: Compresses files using ZPAQ.
- decompress.py: Decompresses ZPAQ archives.
- byte_compare.py: Compares two directories of files byte-by-byte.
- Dockerfile: Sets up the Python environment and ZPAQ.
- Shell scripts: Facilitate running the Docker containers with appropriate mounts and parameters.

## Prerequisites
- Docker
- Access to a Unix-like operating system (Linux, macOS)

## Installation
- Clone the Repository
 ``` python
  git clone <repository-url>

```
- Build the Docker Image
`docker build -t compressor .`

## Usage
### Compressing Files

To compress files, use the **run_compress_Docker.sh** script:

``` python
./run_compress_Docker.sh
```

### Decompressing Files

To compress files, use the **run_decompress_Docker.sh** script:

``` python
./run_decompress_Docker.sh
```
**NOTE:
Decompressing automatically creates a folder called "input" and saved all decompressed files underneath it, while maintaining the folder hierarchy.**
### Compressing Files

To compress files, use the **run_compare_Docker.sh** script:

``` python
./run_compare_Docker.sh
```
## How to Customize Directory Paths in Shell Scripts

Follow these steps to modify the `INPUT_DIR`, `OUTPUT_DIR`, `APP_DIR`, and `LOGS_DIR` in your shell scripts:

- **Open your shell script**: Open the script you want to adjust (e.g., `run_compress_Docker.sh`, `run_decompress_Docker.sh`, `run_compare_Docker.sh`).

- **Edit `INPUT_DIR`**:
  - Find the line starting with `INPUT_DIR=`.
  - Replace the existing path with your desired input directory path.
  - **Example**: `INPUT_DIR="/new/path/to/input"`

- **Edit `OUTPUT_DIR`**:
  - Locate the `OUTPUT_DIR=` line.
  - Change the path to your preferred output directory.
  - **Example**: `OUTPUT_DIR="/new/path/to/output"`

- **Edit `APP_DIR`**:
  - Search for `APP_DIR=`.
  - Update the path to where your application scripts are stored.
  - **Example**: `APP_DIR="/new/path/to/app"`

- **Edit `LOGS_DIR`**:
  - Find the `LOGS_DIR=` line.
  - Update to the directory where you want to save log files.
  - **Example**: `LOGS_DIR="/new/path/to/logs"`


## Specific customization for  `run_compress_Docker.sh`

To customize the parent directory name used in the `run_compress_Docker.sh` script, follow these steps:

- **Open the `run_compress_Docker.sh` script**

- **Modify the Parent Directory Name**:
  - Locate the last argument in the Docker run command: `P24001_Test`.
  - Replace `P24001_Test` with your preferred parent directory name that reflects where you want to save compressed files underneath the output directory.

  - **Example**: If you want to change it to `MyProject`, the command would look like this:
    ```bash
    docker run --rm \
      -v "${INPUT_DIR}:/input:ro" \
      -v "${OUTPUT_DIR}:/output" \
      -v "${APP_DIR}:/app" \
      -v "${LOGS_DIR}:/app/logs" \
      compressor python3 /app/compress.py /input /output MyProject
    ```


