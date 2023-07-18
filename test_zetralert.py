import chime
import datetime
import logging
import schedule
import time

from dotenv import dotenv_values

# Own modules
from sources.fxcm import get_data_from_fxcm
from indicators import rsi, fibonacci_lines
from telegram_message import send_telegram_message


config = dotenv_values(".env")

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
    
    fibo = fibonacci_lines("EURUSD","15min")
    schedule.every(10).seconds.do(check_trigger)

    while True:
        schedule.run_pending()
        time.sleep(1)