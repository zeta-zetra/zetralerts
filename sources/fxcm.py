import datetime
import pandas as pd
import logging

from dotenv import dotenv_values
from forexconnect import ForexConnect, fxcorepy


logging.basicConfig(filename='zetralerts.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


date_format = '%Y-%m-%d %H:%M:%S'
config      = dotenv_values(".env")

USER_ID  = config["FXCM_USER_ID"]
PWD      = config["FXCM_PWD"]
CON      = config["FXCM_CONN"]
SESS     = config["FXCM_SESS"]

FXCM_TIMEFRAME = {"15min": "m15", "5min": "m5", "1min": "m1", "1d":"D1"}
FXCM_SYMBOLS   = {"EURUSD":"EUR/USD"}


def get_data_from_fxcm(symbol: str, timeframe: str, from_date:str = "", to_date: str ="", bars: int = 10 ,USER_ID:str = USER_ID, PWD:str = PWD, CON:str= CON, SESS:str= SESS) -> pd.DataFrame:
    """
    Get Data from FXCM Broker
    
    :params symbol is the currency pair of interest 
    :type :str 
    
    :params timeframe is the timeframe of interest 
    :type :str 
    
    :params from_date is the start date for data request.
    :type :str 
    
    :params to_data is the end date for data request.
    :type :str 
    
    :params bars is the number of candlesticks to get 
    :type :int 
    
    :params USER_ID is the FXCM ACCOUNT ID 
    :type :str 
    
    :params PWD is the Password of the FXCM ACCOUNT
    :type :str 
    
    :params CON is the URL to USE.
    :type :str 
    
    :params SESS is the session type. Options: ['real', 'demo']
    :type :str 
    
    :return: (pd.DataFrame)
    """
    
    
    timeframe = FXCM_TIMEFRAME[timeframe]
    symbol    = FXCM_SYMBOLS[symbol]
    
    with ForexConnect() as fx:
        
        try:
            fx.login(USER_ID, PWD, CON, SESS)
            
            if from_date == "" and to_date == "" :
              to_date         = datetime.datetime.now()
              history         = fx.get_history(symbol, timeframe, None, to_date, bars)
            
            elif from_date == "" and to_date:
                to_date         = datetime.datetime.strptime(to_date, "%Y%m%d")
                history         = fx.get_history(symbol, timeframe, None, to_date, bars)
                
                
            elif from_date and to_date:
                from_date = datetime.datetime.strptime(from_date, "%Y%m%d")
                to_date   = datetime.datetime.strptime(to_date, "%Y%m%d")
                history   = fx.get_history(symbol, timeframe, from_date, to_date)
                
                
            
            
            date  = []
            open_,high,low,close, volume = [],[],[],[],[]
            for row in history:           
                date.append(pd.to_datetime(str(row['Date'])).strftime(date_format))
                open_.append(row['BidOpen'])
                high.append(row['BidHigh'])
                low.append(row['BidLow'])
                close.append(row['BidClose'])
                volume.append(row['Volume'])
                
            ohlc_dict = {"date": date,"open":open_, "high": high,"low":low, "close":close, "volume":volume}
            
            df = pd.DataFrame.from_dict(ohlc_dict)
            
            
        except Exception as e:
            logging.error(f"FXCM ERROR: {e}")
            df = pd.DataFrame()
        try:
            fx.logout()
        except Exception as e:
            logging.error(f"FXCM Logout ERROR: {e}")
            df = pd.DataFrame()
            
    return df 


if __name__ == "__main__":
    # print(get_data_from_fxcm("EUR/USD", "m15", from_date="20230713", to_date="20230714"))
    print(get_data_from_fxcm("EUR/USD", "m15", bars=25))