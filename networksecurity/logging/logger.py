
import logging
import os
from datetime import datetime


# LOG_FILE =f"{datetime.now().strftime("%Y_%m_%d_%H_%M_%S.log")}.log" 
# LOG_FILE =f"{datetime.now().strftime("%Y_%m_%d_%H_%M_%S.log")}.log"
LOG_FILE = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"



LOG_DIR = os.path.join(os.getcwd(), "logs",LOG_FILE)
os.makedirs(LOG_DIR, exist_ok=True)  

LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

my_logger = logging.getLogger("<<<logger>>>")

# Example log
# logger.info("Logging setup complete. Log file created.")
