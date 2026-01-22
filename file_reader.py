"""
Efficient file reading module.
Handles large log files using generators and line-by-line streaming.
Avoids loading entire file into memory.
"""

import logging
from typing import Generator, Iterator, Optional
from pathlib import Path


logger = logging.getLogger('log_analyzer')


def read_log_file(file_path: str) -> Generator[str, None, None]:
    """
    Read log file line by line using a generator.
    Efficiently handles large files without loading entire content into memory.
    
    Args:
        file_path: Path to the log file.
    
    Yields:
        Each line from the file as a string.
    
    Raises:
        FileNotFoundError: If the file doesn't exist.
        IOError: If file cannot be read.
    """
    file_path_obj = Path(file_path)
    
    if not file_path_obj.exists():
        raise FileNotFoundError(f"Log file not found: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            line_number = 0
            for line in file:
                line_number += 1
                yield line.rstrip('\n\r')
            
            logger.info(f"Successfully read {line_number} lines from {file_path}")
    
    except IOError as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        raise


def count_lines(file_path: str) -> int:
    """
    Count total lines in a file efficiently.
    
    Args:
        file_path: Path to the file.
    
    Returns:
        Total number of lines in the file.
    """
    count = 0
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for _ in file:
                count += 1
    except IOError as e:
        logger.error(f"Error counting lines in {file_path}: {str(e)}")
    
    return count
