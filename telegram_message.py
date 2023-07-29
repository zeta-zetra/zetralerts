import dotenv
import json 
import logging
import os 
import requests 

from dotenv import dotenv_values
from typing import Dict, Union


logging.basicConfig(filename='zetralerts.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

if "/home/ubuntu" == os.path.abspath(''):
    config      = dotenv_values(os.path.join("/var/zetralert/zetralerts/",".env"))
    dotenv_path = os.path.join("/var/zetralert/zetralerts/",".env")
else:
    config      = dotenv_values(os.path.join(os.path.abspath(''),".env"))
    dotenv_path = os.path.join(os.path.abspath(''),".env")

TOKEN  =config["TELEGRAM_TOKEN"]
CHAT_ID=config["TELEGRAM_CHAT_ID"]


def get_telegram_chat_id() -> Dict[str, Union[int, str]]:
    """
    Get the Telegram bot chat id
    
    
    :return: (Dict[str, Union[int, str]])
    """
    req      = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    response = requests.get(req)
    result   = response.json()
    
    if result["ok"]:
        if len(result["result"]) > 0:
            default_chat_id = result["result"][0]["message"]["chat"]["id"]
            
            # Set the chat id in the env file 
            dotenv.set_key(dotenv_path, "TELEGRAM_CHAT_ID", default_chat_id, quote_mode='never')
            
            # Send message to the bot 
            text_msg        = send_telegram_message("We are good to go!", TOKEN, default_chat_id)
            
            if text_msg:
                return json.dumps({"error":0,"chat_id": default_chat_id})
            else:
                return json.dumps({"error":1,"msg":"Please try again." })
        else:
                return json.dumps({"error":2,"msg": "Send any message to your bot"})    
    else:
        return json.dumps({"error":2,"msg": "Please check your API Token. We couldn't reach your bot"})   
    
    return result 

def send_telegram_message(message:str, TOKEN:str = TOKEN, CHAT_ID:str = CHAT_ID) -> bool:
    """
    Send Telegram Message 
    
    :params message will be sent to Telegram bot
    :type :str 
    
    :params TOKEN is the BOT token
    :type :str 
    
    :params CHAT_ID is the chat to send the message to 
    :type :str
    
    :return: (bool)
    """
    
    url  = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    resp = requests.get(url).json() 

    if resp['ok']:
        logging.info("Message was sent successfully")
        return True 
    else:
        logging.info("Message was not sent successfully")
        return False 
    

if __name__ =="__main__":
    # send_telegram_message("Start trigger...")
    # print(get_telegram_updates())
    pass