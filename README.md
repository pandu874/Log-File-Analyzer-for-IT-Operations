# Log File Analyzer for IT Operations

Enterprise-grade Python application for analyzing server log files and generating actionable insights.

## Features

- **Efficient File Processing**: Handles log files with 50,000+ lines using generators and streaming
- **Robust Parsing**: Uses Regular Expressions to parse log entries, safely skips malformed lines
- **Comprehensive Analytics**: 
  - Total request count
  - Total error responses (4xx and 5xx)
  - Error code frequency analysis
  - Top 5 IP addresses generating errors
- **Data Processing**: Uses Pandas for aggregation and analysis
- **Visualization**: Generates error distribution charts using Matplotlib
- **Logging**: Comprehensive logging with INFO, WARNING, and ERROR levels

## Project Structure

```
log_file_analyzer/
│
├── data/
│   └── server_logs.txt          # Log file to analyze
│
├── analyzer/
│   ├── __init__.py
│   ├── file_reader.py           # Efficient file reading (generator)
│   ├── parser.py                # Regex parsing logic
│   ├── analytics.py             # Pandas-based computations
│   ├── visualizer.py            # Matplotlib visualizations
│   └── logger_config.py         # Logging setup
│
├── reports/
│   ├── summary_report.txt       # Generated summary report
│   └── error_distribution.png   # Generated error chart
│
├── web/
│   ├── app.py                   # Flask web application
│   ├── templates/
│   │   └── index.html          # Web UI template
│   └── static/
│       └── style.css           # Web UI styles
├── main.py                      # CLI entry point
├── requirements.txt
└── README.md
```

## Log Format

The application expects log files in the following format:

```
YYYY-MM-DD HH:MM:SS - IP_ADDRESS - HTTP_METHOD - STATUS_CODE
```

Example:
```
2024-01-15 10:30:45 - 192.168.1.100 - GET - 200
2024-01-15 10:30:46 - 192.168.1.101 - POST - 404
2024-01-15 10:30:47 - 192.168.1.102 - GET - 500
```

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python main.py --log-file data/server_logs.txt
```

### Generate Sample Log File

```bash
python main.py --generate
```

This will generate a sample log file with 50,000+ entries if one doesn't exist.

### Custom Log File Path

```bash
python main.py --log-file /path/to/your/logfile.txt
```

## Web Application

The project includes a Flask-based web interface for easier interaction.

### Starting the Web Application

```bash
python web/app.py
```

The web application will start on `http://127.0.0.1:5000`

### Web Features

- **File Upload**: Upload log files through a web interface
- **Visual Results**: View analysis results in an intuitive web UI
- **Interactive Charts**: View error distribution charts directly in the browser
- **Responsive Design**: Works on desktop and mobile devices

### Web Usage

1. Navigate to `http://127.0.0.1:5000` in your browser
2. Click "Choose File" to select a log file (.txt)
3. Click "Analyze Logs" to process the file
4. View the results including statistics, error codes, top IPs, and charts
5. Click "Analyze Another File" to process a new file

## Output

The application generates:

1. **Console Output**: Summary statistics printed to console
2. **Summary Report**: `reports/summary_report.txt` - Detailed analytics report
3. **Visualization**: `reports/error_distribution.png` - Bar chart of error code distribution
4. **Execution Logs**: `log_analyzer.log` - Detailed execution logs

## Error Handling

- Malformed log entries are safely skipped and logged as warnings
- File I/O errors are caught and logged
- The application continues processing even if some entries fail to parse

## Requirements

- Python 3.8+
- pandas >= 2.0.0
- matplotlib >= 3.7.0
- numpy >= 1.24.0
- flask >= 2.3.0 (for web application)
- werkzeug >= 2.3.0 (for web application)


