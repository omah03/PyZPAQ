import os
import logging
import coloredlogs
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

log_file_path = '/app/logs/comparison.log'

Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)

coloredlogs.install(level='INFO', fmt='%(asctime)s %(levelname)s:%(message)s')

file_handler = logging.FileHandler(log_file_path, mode='w')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(message)s'))
logging.getLogger().addHandler(file_handler)

def compare_files(file_pair):
    file1, file2 = file_pair
    try:
        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
            if f1.read() == f2.read():
                logging.info(f"Files {file1} and {file2} are identical.")
                return True
            else:
                logging.error(f"Files {file1} and {file2} differ.")
                return False
    except Exception as e:
        logging.error(f"Error comparing {file1} and {file2}: {e}")
        return False

def compare_folders(original_dir, decompressed_dir):
    original_files = [f for f in Path(original_dir).rglob('*') if f.is_file()]
    decompressed_files = [Path(decompressed_dir) / f.relative_to(original_dir) for f in original_files]

    file_pairs = [(orig, decomp) for orig, decomp in zip(original_files, decompressed_files) if decomp.exists()]

    diff_count = 0
    with ThreadPoolExecutor() as executor:
        future_to_file = {executor.submit(compare_files, pair): pair for pair in file_pairs}
        for future in as_completed(future_to_file):
            if not future.result():
                diff_count += 1

    missing_count = len(original_files) - len(file_pairs)
    diff_count += missing_count

    if missing_count > 0:
        logging.error(f"{missing_count} decompressed files do not exist.")

    logging.info(f"Comparison completed. {diff_count} files differ.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        logging.error("Usage: python compare.py <original_directory> <decompressed_directory>")
        sys.exit(1)

    original_dir = Path(sys.argv[1])
    decompressed_dir = Path(sys.argv[2])

    if not original_dir.is_dir() or not decompressed_dir.is_dir():
        logging.error(f"Error: Input directories are not valid. Original: {original_dir}, Decompressed: {decompressed_dir}")
        sys.exit(1)

    logging.info(f"Starting comparison. Original directory: {original_dir}, Decompressed directory: {decompressed_dir}")
    compare_folders(original_dir, decompressed_dir)
