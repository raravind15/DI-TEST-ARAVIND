import logging
from datetime import datetime
from google.cloud import storage
import re

logging.basicConfig(level=logging.INFO,format=f"%(asctime)s-%(levelname)s-%(message)s")
logger=logging.getLogger(__name__)

logging.info("Testing")