"""
Visualization module using Matplotlib.
Generates charts for error distribution.
"""

import logging
import os
from typing import Dict
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend


logger = logging.getLogger('log_analyzer')


def create_error_distribution_chart(analytics: Dict, output_path: str) -> None:
    """
    Create a bar chart showing error code distribution.
    
    Args:
        analytics: Dictionary containing analytics results with error_codes.
        output_path: Path to save the chart image.
    """
    try:
        error_codes = analytics.get('error_codes', {})
        
        if not error_codes:
            logger.warning("No error codes to visualize")
            return
        
        # Prepare data
        codes = sorted(error_codes.keys(), key=lambda x: int(x))
        counts = [error_codes[code] for code in codes]
        
        # Create figure
        plt.figure(figsize=(12, 6))
        
        # Create bar chart
        bars = plt.bar(codes, counts, color='#dc3545', alpha=0.7, edgecolor='black')
        
        # Customize chart
        plt.xlabel('HTTP Status Code', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Occurrences', fontsize=12, fontweight='bold')
        plt.title('Error Code Distribution', fontsize=14, fontweight='bold', pad=20)
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}',
                    ha='center', va='bottom', fontsize=9)
        
        # Rotate x-axis labels if needed
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save chart
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Error distribution chart saved to {output_path}")
    
    except Exception as e:
        logger.error(f"Error creating chart: {str(e)}")
        raise
