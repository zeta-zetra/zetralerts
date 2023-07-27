"""
Define all the Fibonacci based alerts

Date   : 2023-07-26
Author : Zetra 
"""



import chime 

# Own modules
from sources.fxcm import get_data_from_fxcm
from indicators import fibonacci_lines
from telegram_message import send_telegram_message

# Set the sound notification for local development
chime.theme("zelda")


def trigger_message(message: str) -> bool:
    """
    Trigger message based on the rules being satisfied
    
    """

    logging.info(message)
    send_telegram_message(message)
    
    return True

def fibonacci_breakout(symbol: str, timeframe: str,  **kwargs) -> bool:
    """
    Set an alert for when the close is above (below) the Fibonacci resistance (support) 
    levels
    
    :params symbol is the currency pair
    :type :str 
    
    :params timeframe is the trading timeframe.
    :type :str 
    
    :return: (bool)
    """
    
    
    ohlc = get_data_from_fxcm(symbol, timeframe, bars=1)
    fibo = fibonacci_lines(symbol,timeframe)
    
    msg_resp = False
    if fibo["r2"] < ohlc.close[0]:
        msg_resp = trigger_message("Close is greater than R1 of the Fibonacci Line.")
                
    elif fibo["s2"] > ohlc.close[0]:
         msg_resp = trigger_message("Close is less than S2 of the Fibonacci Line")

        
    if msg_resp and not LIVE:
        chime.success(sync=True)
        return True 
        
    return False