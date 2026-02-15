# 
import subprocess, logging
from config import config

# We can't run QGIS within our local python env (must use the QGIS-provided Python installation)
# OS-specific command needs to be configured in the config.ini
def run_qgis():
    output = ""
    try:
        output = subprocess.run([config['qgis_cli_cmd'], 'qgis_join.py'], check=True, capture_output=True)
    except Exception as e:
        logging.error(e)
        logging.error("call to QGIS failed")
        logging.error(output)