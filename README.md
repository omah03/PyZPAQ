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
