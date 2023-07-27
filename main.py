"""
This file sends messages to a Telegram Bot if an alert has been triggered.

Author: Zetra
Date  : 2023-07-17
"""

import ast
import logging
import os
import schedule
import time

from dotenv import dotenv_values


# Own modules
from alerts.fibonacci import fibonacci_breakout

# Grab the .env file according to OS 
if "/home/ubuntu" == os.path.abspath(''):
    config = dotenv_values(os.path.join("/var/zetralert/zetralerts/",".env"))
else:
    config = dotenv_values(os.path.join(os.path.abspath(''),".env"))

# Set the logger
logging.basicConfig(filename='zetralerts.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Get the env variables
LIVE   = ast.literal_eval(config["LIVE"])
ALERT  = int(config["ALERT"])

def check_trigger():
    """
    Check any of the below have been triggered
    """

    resp = fibonacci_breakout("EURUSD", "15min", LIVE=LIVE)
    if not resp:
        logging.info("Just checked trigger and no alert.")
    
if __name__ == "__main__":
    
    schedule.every(ALERT).minute.do(check_trigger)

    while True:
        schedule.run_pending()
        time.sleep(1)