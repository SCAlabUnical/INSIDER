import os
import logging

# Get absolute path to the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

solver_config: dict = {
    "PERFORMANCE_PATH": os.path.join(BASE_DIR, 'data', 'performance.json'),
    "LOG_LEVEL": logging.INFO,  # Set default log level
}