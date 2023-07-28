"""
Utility Functions on alerts

Date   : 2023-07-28
Author : Zetra
"""

import logging

# Own modules
from telegram_message import send_telegram_message


def trigger_message(message: str) -> bool:
    """
    Trigger message based on the rules being satisfied
    
    :params message is the log message 
    :type :str 
    
    :return: (bool)
    """

    logging.info(message)
    send_telegram_message(message)
    
    return True