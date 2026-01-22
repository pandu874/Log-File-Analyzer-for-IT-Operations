"""
Logging configuration module.
Configures Python logging module with INFO, WARNING, and ERROR levels.
Saves logs to a log file.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


def setup_logger(log_file: Optional[str] = None) -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        log_file: Path to log file. If None, defaults to 'log_analyzer.log' in project root.
    
    Returns:
        Configured logger instance.
    """
    if log_file is None:
        log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log_analyzer.log')
    
    # Ensure log directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create logger
    logger = logging.getLogger('log_analyzer')
    logger.setLevel(logging.DEBUG)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # File handler
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler (INFO and above)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
