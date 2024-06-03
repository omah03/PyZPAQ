import os
import subprocess
import logging
import sys
from pathlib import Path
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

log_file_path = '/app/logs/decompression.log'

Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    filemode='w'
)

def decompress_file(input_file, output_dir, index, total):
    try:
        command = ["zpaq", "x", str(input_file), "-to", str(output_dir)]
        subprocess.run(command, check=True)
        logging.info(f"Decompressed ({index}/{total}): {input_file} to {output_dir}.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to decompress {input_file}. Error: {e}")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def decompress_folder(input_dir, output_dir):
    start_time = time.time()

    files_to_decompress = [Path(root) / file for root, _, files in os.walk(input_dir) for file in files if file.endswith('.zpaq')]
    total_files = len(files_to_decompress)
    logging.info(f"Found {total_files} files to decompress.")

    with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        futures = [executor.submit(decompress_file, file, output_dir, i+1, total_files) for i, file in enumerate(files_to_decompress)]

        for future in as_completed(futures):
            future.result()

    elapsed_time = time.time() - start_time
    logging.info(f"Decompression completed. Total Time Taken: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        logging.error("Usage: python decompress.py <input_directory> <output_directory>")
        sys.exit(1)

    input_dir, output_dir = Path(sys.argv[1]), Path(sys.argv[2])
    if not input_dir.is_dir() or not output_dir.is_dir():
        logging.error(f"Error: Input or output is not a directory. Input: {input_dir}, Output: {output_dir}")
        sys.exit(1)

    logging.info(f"Starting decompression. Input directory: {input_dir}, Output directory: {output_dir}")
    decompress_folder(input_dir, output_dir)
