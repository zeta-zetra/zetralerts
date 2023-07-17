import requests 
from dotenv import dotenv_values


config = dotenv_values(".env")

TOKEN  =config["TELEGRAM_TOKEN"]
CHAT_ID=config["TELEGRAM_CHAT_ID"]

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
        print("Message was sent successfully")
        return True 
    else:
        print("Message was not sent successfully")
        return False 
    

if __name__ =="__main__":
    send_telegram_message("Start trigger...")