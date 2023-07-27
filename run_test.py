"""
Test if messages can be sent to the Telegram Bot

More tests can be added in here to see if the application works.

Author: Zetra
Date  : 2023-07-21
"""

# Own modules
from sources.fxcm import get_data_from_fxcm
from telegram_message import send_telegram_message



def send_message_test(message: str):
    """
    Send a message to the bot
    
    :params message
    :type :str 
    
    :return: (None)
    """
    
    if send_telegram_message(message):
        print("Message sent successfully...Check your phone.")
    else:
        print("Message was not sent successfully...Start Debugging")
    
def send_ohlc_prices(broker: str = "FXCM", symbol: str = "EURUSD"):
    """
    Send OHLC prices to the Telegram bot
    
    :params broker to get the prices from. Options: ['FXCM'] 
    :type :str 
    
    :params symbol is the currency pair. Options: ['EURUSD']
    :type :str 
    
    :return: (None)
    """
    
    if broker == "FXCM":
        ohlc    = get_data_from_fxcm("EURUSD", "15min", bars=1)
        close   = ohlc.close[0]
        message = f"The EURUSD close price at the 15min timeframe is {close}"
        
    send_message_test(message)
    
def run_test():
    """ Run test """
        
    send_ohlc_prices()
        
if __name__ == "__main__":
    run_test()