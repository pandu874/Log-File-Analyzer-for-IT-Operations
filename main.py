"""
Main entry point for Log File Analyzer.
Orchestrates file reading, parsing, analysis, and visualization.
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

from analyzer.logger_config import setup_logger
from analyzer.file_reader import read_log_file
from analyzer.parser import parse_log_file
from analyzer.analytics import analyze_logs, get_summary_stats
from analyzer.visualizer import create_error_distribution_chart


def generate_sample_logs(file_path: str, num_lines: int = 50000) -> None:
    """
    Generate synthetic log data for testing.
    
    Args:
        file_path: Path to output log file.
        num_lines: Number of log lines to generate.
    """
    logger = setup_logger()
    logger.info(f"Generating sample log file with {num_lines:,} lines...")
    
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD']
    status_codes = [200, 201, 301, 400, 401, 403, 404, 500, 502, 503]
    
    # Higher probability for error codes (4xx, 5xx)
    error_status_codes = [400, 401, 403, 404, 500, 502, 503]
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    base_date = datetime(2024, 1, 1, 0, 0, 0)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        for i in range(num_lines):
            # Generate timestamp
            seconds_offset = random.randint(0, 86400 * 30)  # 30 days
            timestamp = (base_date + timedelta(seconds=seconds_offset)).strftime('%Y-%m-%d %H:%M:%S')
            
            # Generate IP address
            ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            
            # Generate method
            method = random.choice(methods)
            
            # Generate status code (higher chance of errors for realistic data)
            if random.random() < 0.15:  # 15% errors
                status_code = random.choice(error_status_codes)
            else:
                status_code = random.choice(status_codes)
            
            # Write log line
            f.write(f"{timestamp} - {ip} - {method} - {status_code}\n")
            
            # Add some malformed lines (5%)
            if random.random() < 0.05:
                f.write(f"Malformed entry {i} - invalid format\n")
    
    logger.info(f"Sample log file generated: {file_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Log File Analyzer - Enterprise IT Operations Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--log-file',
        type=str,
        default='data/server_logs.txt',
        help='Path to the log file to analyze (default: data/server_logs.txt)'
    )
    parser.add_argument(
        '--generate',
        action='store_true',
        help='Generate sample log file if it does not exist'
    )
    
    args = parser.parse_args()
    
    # Setup logger
    logger = setup_logger()
    logger.info("=" * 60)
    logger.info("Log File Analyzer - Starting Analysis")
    logger.info("=" * 60)
    
    log_file_path = args.log_file
    
    # Check if log file exists, generate if needed
    if not os.path.exists(log_file_path):
        if args.generate:
            generate_sample_logs(log_file_path, num_lines=50000)
        else:
            logger.warning(f"Log file not found: {log_file_path}")
            logger.info("Use --generate flag to create a sample log file")
            logger.error(f"Log file not found: {log_file_path}")
            sys.exit(1)
    
    try:
        # Read log file
        logger.info(f"Reading log file: {log_file_path}")
        log_lines = read_log_file(log_file_path)
        
        # Parse log entries
        logger.info("Parsing log entries...")
        log_entries = list(parse_log_file(log_lines))
        
        if not log_entries:
            logger.warning("No valid log entries found")
            sys.exit(1)
        
        # Analyze logs
        logger.info("Analyzing log data...")
        analytics = analyze_logs(log_entries)
        
        # Generate summary
        summary = get_summary_stats(analytics)
        
        # Print summary to console
        print("\n")
        print(summary)
        print("\n")
        
        # Save summary report
        report_path = 'reports/summary_report.txt'
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(summary)
            f.write(f"\nGenerated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        logger.info(f"Summary report saved to {report_path}")
        
        # Create visualization
        logger.info("Generating error distribution chart...")
        chart_path = 'reports/error_distribution.png'
        create_error_distribution_chart(analytics, chart_path)
        
        logger.info("Analysis completed successfully!")
        logger.info("=" * 60)
    
    except FileNotFoundError as e:
        logger.error(f"File error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
