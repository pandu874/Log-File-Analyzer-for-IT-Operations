"""
Flask web application for Log File Analyzer.
Reuses existing analyzer backend without modifying core logic.
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, send_file
from werkzeug.utils import secure_filename

# Add parent directory to path to import analyzer modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from analyzer.logger_config import setup_logger
from analyzer.file_reader import read_log_file
from analyzer.parser import parse_log_file
from analyzer.analytics import analyze_logs
from analyzer.visualizer import create_error_distribution_chart


# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'log-analyzer-secret-key-2024'
app.config['UPLOAD_FOLDER'] = 'data'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['REPORTS_FOLDER'] = 'reports'

ALLOWED_EXTENSIONS = {'txt'}

# Setup logger
logger = setup_logger()


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.template_filter('format_number')
def format_number_filter(value):
    """Format number with thousand separators."""
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return str(value)


def analyze_log_file(filepath: str):
    """Analyze a log file and return results."""
    try:
        logger.info(f"Analyzing log file: {filepath}")
        
        # Read log file using existing function
        log_lines = read_log_file(filepath)
        
        # Parse log entries using existing function
        log_entries = list(parse_log_file(log_lines))
        
        if not log_entries:
            return None, 'No valid log entries found in the file.'
        
        # Analyze logs using existing function
        analytics = analyze_logs(log_entries)
        
        # Generate chart using existing function
        filename_base = os.path.basename(filepath).rsplit('.', 1)[0]
        # Remove 'uploaded_' prefix if present
        if filename_base.startswith('uploaded_'):
            filename_base = filename_base.replace('uploaded_', '', 1)
        chart_filename = f'error_chart_{filename_base}.png'
        chart_path = os.path.join(app.config['REPORTS_FOLDER'], chart_filename)
        os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)
        create_error_distribution_chart(analytics, chart_path)
        
        logger.info(f"Analysis completed successfully for {len(log_entries)} entries")
        
        return {
            'analytics': analytics,
            'chart_filename': chart_filename,
            'total_parsed': len(log_entries)
        }, None
    
    except Exception as e:
        logger.error(f"Error analyzing file: {str(e)}", exc_info=True)
        return None, f'Error processing file: {str(e)}'


@app.route('/')
def index():
    """Home page with file upload form."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Handle file upload and run analysis."""
    if 'log_file' not in request.files:
        flash('No file uploaded. Please select a log file.', 'error')
        return redirect(url_for('index'))
    
    file = request.files['log_file']
    
    if file.filename == '':
        flash('No file selected. Please choose a log file.', 'error')
        return redirect(url_for('index'))
    
    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload a .txt file.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f'uploaded_{filename}')
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(upload_path)
        
        logger.info(f"File uploaded: {upload_path}")
        
        # Use the analyze_log_file function
        results, error = analyze_log_file(upload_path)
        
        # Clean up uploaded file
        try:
            os.remove(upload_path)
        except:
            pass
        
        if error or not results:
            flash(error or 'No valid log entries found in the file. Please check the file format.', 'error')
            return redirect(url_for('index'))
        
        # Render results page
        return render_template('index.html', 
                             analytics=results['analytics'],
                             chart_filename=results['chart_filename'],
                             total_parsed=results['total_parsed'])
    
    except FileNotFoundError as e:
        flash(f'File error: {str(e)}', 'error')
        logger.error(f"File error: {str(e)}")
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error processing file: {str(e)}', 'error')
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        return redirect(url_for('index'))


@app.route('/chart/<filename>')
def chart(filename):
    """Serve chart images."""
    from flask import abort
    reports_path = os.path.abspath(app.config['REPORTS_FOLDER'])
    file_path = os.path.join(reports_path, filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='image/png')
    else:
        abort(404)


if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)
    
    logger.info("Starting Flask web application")
    app.run(host='127.0.0.1', port=5000, debug=True)
