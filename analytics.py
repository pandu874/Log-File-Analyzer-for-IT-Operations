"""
Analytics module using Pandas.
Performs aggregation and analysis on parsed log entries.
"""

import logging
from typing import List, Dict, Tuple
import pandas as pd
from analyzer.parser import LogEntry


logger = logging.getLogger('log_analyzer')


def analyze_logs(log_entries: List[LogEntry]) -> Dict:
    """
    Analyze log entries and compute statistics.
    
    Args:
        log_entries: List of parsed LogEntry objects.
    
    Returns:
        Dictionary containing analytics results.
    """
    if not log_entries:
        logger.warning("No log entries to analyze")
        return {
            'total_requests': 0,
            'total_errors': 0,
            'error_codes': {},
            'top_error_ips': []
        }
    
    try:
        # Convert to DataFrame for analysis
        df = pd.DataFrame([
            {
                'timestamp': entry.timestamp,
                'ip_address': entry.ip_address,
                'method': entry.method,
                'status_code': entry.status_code
            }
            for entry in log_entries
        ])
        
        # Total requests
        total_requests = len(df)
        
        # Total errors (4xx and 5xx)
        total_errors = len(df[(df['status_code'] >= 400) & (df['status_code'] < 600)])
        
        # Error code frequency
        error_df = df[(df['status_code'] >= 400) & (df['status_code'] < 600)]
        error_codes = error_df['status_code'].value_counts().to_dict()
        error_codes = {str(k): int(v) for k, v in error_codes.items()}
        
        # Top 5 IPs generating errors
        top_error_ips = error_df.groupby('ip_address').size().sort_values(ascending=False).head(5)
        top_error_ips_list = [
            {'ip': str(ip), 'error_count': int(count)}
            for ip, count in top_error_ips.items()
        ]
        
        logger.info(f"Analysis completed: {total_requests} total requests, {total_errors} errors")
        
        return {
            'total_requests': total_requests,
            'total_errors': total_errors,
            'error_codes': error_codes,
            'top_error_ips': top_error_ips_list
        }
    
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise


def get_summary_stats(analytics: Dict) -> str:
    """
    Format analytics results as a summary string.
    
    Args:
        analytics: Dictionary containing analytics results.
    
    Returns:
        Formatted summary string.
    """
    summary = []
    summary.append("=" * 60)
    summary.append("LOG FILE ANALYSIS SUMMARY")
    summary.append("=" * 60)
    summary.append(f"Total Requests: {analytics['total_requests']:,}")
    summary.append(f"Total Errors (4xx/5xx): {analytics['total_errors']:,}")
    summary.append("")
    
    if analytics['error_codes']:
        summary.append("Error Code Frequency:")
        summary.append("-" * 60)
        for code, count in sorted(analytics['error_codes'].items(), key=lambda x: int(x[0])):
            summary.append(f"  {code}: {count:,} occurrences")
        summary.append("")
    
    if analytics['top_error_ips']:
        summary.append("Top 5 IP Addresses by Error Count:")
        summary.append("-" * 60)
        for idx, item in enumerate(analytics['top_error_ips'], 1):
            summary.append(f"  {idx}. {item['ip']}: {item['error_count']:,} errors")
        summary.append("")
    
    summary.append("=" * 60)
    
    return "\n".join(summary)
