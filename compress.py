import os
import subprocess
import logging
import sys
from pathlib import Path
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

log_file_path = '/app/logs/compression.log'

Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    filemode='w' 
)
def get_file_size(path):
    return os.path.getsize(path)

def compress_file(input_file, output_file):
    try:
        original_size = get_file_size(input_file)
        command = ["zpaq", "a", str(output_file), str(input_file), "-method", "5"]
        subprocess.run(command, check=True)
        compressed_size = get_file_size(output_file)
        file_compression_percentage = 100 - (compressed_size / original_size * 100) if original_size > 0 else 0
        logging.info(f"Compressed {input_file} to {output_file}. Original size: {original_size} bytes, Compressed size: {compressed_size} bytes, Compression: {file_compression_percentage:.2f}%")
        return original_size, compressed_size
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to compress {input_file}. Error: {e}")
        return 0, 0
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return 0, 0
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return 0, 0

def compress_folder(input_dir, output_dir, top_level_folder_name):
    total_original_size = 0
    total_compressed_size = 0
    start_time = time.time()

    files_to_compress = []
    processed_files = set()

    for root, _, files in os.walk(input_dir):
        for file in files:
            files_to_compress.append(Path(root) / file)

    total_files = len(files_to_compress)
    futures = []
    with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        for i, input_file_path in enumerate(files_to_compress, 1):
            relative_path = input_file_path.relative_to(input_dir)
            output_file_path = Path(output_dir) / top_level_folder_name / relative_path.with_suffix(relative_path.suffix + '.zpaq')

            if output_file_path.exists() or output_file_path in processed_files:
                logging.info(f"Skipping {input_file_path} as it is already compressed or in processed files.")
                continue

            os.makedirs(output_file_path.parent, exist_ok=True)
            futures.append(executor.submit(compress_file, input_file_path, output_file_path))

        for future in as_completed(futures):
            try:
                original_size, compressed_size = future.result()
                total_original_size += original_size
                total_compressed_size += compressed_size
                processed_files.add(output_file_path)
            except Exception as exc:
                logging.error(f'Generated an exception: {exc}')

    elapsed_time = time.time() - start_time
    compression_percentage = 100 - ((total_compressed_size / total_original_size) * 100) if total_original_size > 0 else 0
    logging.info(f"Total Original Size: {total_original_size} bytes")
    logging.info(f"Total Compressed Size: {total_compressed_size} bytes")
    logging.info(f"Overall Compression Percentage: {compression_percentage:.2f}%")
    logging.info(f"Total Time Taken: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        logging.error("Usage: python compress.py <input_directory> <output_directory> <top_level_folder_name>")
        sys.exit(1)

    input_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    top_level_folder_name = sys.argv[3]

    if not input_dir.is_dir() or not output_dir.is_dir():
        logging.error(f"Error: Input or output is not a directory. Input: {input_dir}, Output: {output_dir}")
        sys.exit(1)

    logging.info(f"Starting compression. Input directory: {input_dir}, Output directory: {output_dir}")
    compress_folder(input_dir, output_dir, top_level_folder_name)

# docker run --rm -v /media/dc-04-vol03/HBR/storage/P24001_Test:/input:ro -v /media/dc-04-vol03/omar:/output -v /media/dc-04-vol03/omar:/app -v /media/dc-04-vol03/omar:/app/logs compressor python /app/compress.py /input /output P24001_Test
