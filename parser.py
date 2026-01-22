"""
Log parsing module using Regular Expressions.
Parses log entries and validates format.
Skips malformed log lines safely.
"""

import re
import logging
from typing import Optional, Tuple, Generator
from dataclasses import dataclass
from datetime import datetime


logger = logging.getLogger('log_analyzer')


@dataclass
class LogEntry:
    """Represents a parsed log entry."""
    timestamp: str
    ip_address: str
    method: str
    status_code: int
    raw_line: str


# Regex pattern for log entry format:
# Format 1: Timestamp - IP - Method - Status
# Format 2: Timestamp IP Method [PATH] Status
# Examples:
#   2024-01-15 10:30:45 - 192.168.1.100 - GET - 200
#   2024-01-15 10:30:45 192.168.1.100 GET /path 200
LOG_PATTERN_WITH_DASHES = re.compile(
    r'^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+-\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+-\s+(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+-\s+(\d{3})$',
    re.IGNORECASE
)

LOG_PATTERN_WITH_PATH = re.compile(
    r'^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+(\S+)\s+(\d{3})$',
    re.IGNORECASE
)


def parse_log_line(line: str) -> Optional[LogEntry]:
    """
    Parse a single log line using regex.
    Supports multiple formats:
    - Format 1: YYYY-MM-DD HH:MM:SS - IP - METHOD - STATUS
    - Format 2: YYYY-MM-DD HH:MM:SS IP METHOD PATH STATUS
    
    Args:
        line: Raw log line string.
    
    Returns:
        LogEntry object if parsing successful, None if malformed.
    """
    if not line or not line.strip():
        return None
    
    line_stripped = line.strip()
    
    # Try format with dashes first
    match = LOG_PATTERN_WITH_DASHES.match(line_stripped)
    if match:
        try:
            timestamp = match.group(1)
            ip_address = match.group(2)
            method = match.group(3).upper()
            status_code = int(match.group(4))
            
            # Validate IP address format
            if not is_valid_ip(ip_address):
                logger.warning(f"Invalid IP address in log entry: {ip_address}")
                return None
            
            # Validate status code range
            if status_code < 100 or status_code > 599:
                logger.warning(f"Invalid status code: {status_code}")
                return None
            
            return LogEntry(
                timestamp=timestamp,
                ip_address=ip_address,
                method=method,
                status_code=status_code,
                raw_line=line
            )
        except (ValueError, IndexError) as e:
            logger.warning(f"Error parsing log line: {str(e)} - {line[:100]}")
            return None
    
    # Try format with PATH
    match = LOG_PATTERN_WITH_PATH.match(line_stripped)
    if match:
        try:
            timestamp = match.group(1)
            ip_address = match.group(2)
            method = match.group(3).upper()
            path = match.group(4)  # PATH (not used but extracted)
            status_code = int(match.group(5))
            
            # Validate IP address format
            if not is_valid_ip(ip_address):
                logger.warning(f"Invalid IP address in log entry: {ip_address}")
                return None
            
            # Validate status code range
            if status_code < 100 or status_code > 599:
                logger.warning(f"Invalid status code: {status_code}")
                return None
            
            return LogEntry(
                timestamp=timestamp,
                ip_address=ip_address,
                method=method,
                status_code=status_code,
                raw_line=line
            )
        except (ValueError, IndexError) as e:
            logger.warning(f"Error parsing log line: {str(e)} - {line[:100]}")
            return None
    
    # No pattern matched
    logger.warning(f"Malformed log entry: {line[:100]}")  # Log first 100 chars
    return None


def is_valid_ip(ip: str) -> bool:
    """
    Validate IP address format.
    
    Args:
        ip: IP address string.
    
    Returns:
        True if valid IP format, False otherwise.
    """
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    
    try:
        for part in parts:
            num = int(part)
            if num < 0 or num > 255:
                return False
        return True
    except ValueError:
        return False


def parse_log_file(lines: Generator[str, None, None]) -> Generator[LogEntry, None, None]:
    """
    Parse multiple log lines from a generator.
    
    Args:
        lines: Generator yielding log lines.
    
    Yields:
        Parsed LogEntry objects (skips malformed entries).
    """
    parsed_count = 0
    skipped_count = 0
    
    for line in lines:
        entry = parse_log_line(line)
        if entry:
            parsed_count += 1
            yield entry
        else:
            skipped_count += 1
    
    logger.info(f"Parsed {parsed_count} valid entries, skipped {skipped_count} malformed entries")
