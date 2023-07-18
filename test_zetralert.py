"""
This file is meant to run deployment tests to see if the deployment was successful.

Examples:
1. Send a message to your Telegram Bot
2. Request Data from your broker
3. Run a trigger
etc, etc.

Date: 2023-07-18 

"""
import chime
import datetime
import logging
import os
import schedule
import time

from dotenv import dotenv_values

# Own modules
from sources.fxcm import get_data_from_fxcm
from indicators import rsi, fibonacci_lines
from telegram_message import send_telegram_message

if "/home/ubuntu" == os.path.abspath(''):
    config = dotenv_values(os.path.join("/var/zetralert/zetralerts/",".env"))
else:
    config = dotenv_values(os.path.join(os.path.abspath(''),".env"))
    
LIVE   =config["LIVE"]

logging.basicConfig(filename='zetralerts.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

chime.theme("zelda")

    
def check_trigger():
    """
    Check any of the below have been triggered
    """
    ohlc = get_data_from_fxcm("EURUSD", "15min", bars=1)
    fibo = fibonacci_lines("EURUSD","15min")
    
    if fibo["r2"] < ohlc.close[0]:
        if LIVE=="False":
            chime.success(sync=True)
        logging.info("Close is greater than R2 of the Fibonacci Line")
        send_telegram_message("Close is greater than R2 of the Fibonacci Line")
    elif fibo["s2"] > ohlc.close[0]:
        if LIVE == "False":
            chime.success(sync=True)
        logging.info("Close is less than S2 of the Fibonacci Line")
        send_telegram_message("Close is less than S2 of the Fibonacci Line")
    
    print("Just checked trigger")
    
if __name__ == "__main__":
    print("Starting the test for Zetralerts...")
    fibo = fibonacci_lines("EURUSD","15min")
    schedule.every(10).seconds.do(check_trigger)
    print("Scheduling a run every 10 seconds...")

    while True:
        schedule.run_pending()
        time.sleep(1)