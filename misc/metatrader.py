from datetime import datetime

import logging
import pandas as pd 
import MetaTrader5 as mt5


MT5_TIMEFRAMES = {"15min":mt5.TIMEFRAME_M15, "30min":mt5.TIMEFRAME_M30, "1h": mt5.TIMEFRAME_H1,
                    "4h": mt5.TIMEFRAME_H4, "1d": mt5.TIMEFRAME_D1}


logging.basicConfig(filename='zetralerts.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

 
def get_data_from_mt5(symbol: str, timeframe: str, bars: int = 50, start_base: int = 0) -> pd.DataFrame:
    """
    Get symbol data from the MetaTrader Broker

    :params symbol is the forex pair 
    :type :str 
    
    :params timeframe is the timeframe of the forex pair
    :type  :str 
    
    :params bars is the number of previous bars to get 
    :type :int 
    
    :params start_base is where to start the bars from. i.e. 0 is from today 
    :type :int
    
    :return: (pd.DataFrame)
    """
    
    # establish connection to MetaTrader 5 terminal
    if not mt5.initialize():
        logging.error(f"initialize() failed, error code = {mt5.last_error()}")
        quit()
    
    # Get the timeframe 
    tf  = MT5_TIMEFRAMES[timeframe]
  
    # Get the bars 
    rates = mt5.copy_rates_from_pos(symbol, tf, start_base, bars)
   
    # shut down connection to the MetaTrader 5 terminal
    mt5.shutdown()
    # create DataFrame out of the obtained data
    rates_frame = pd.DataFrame(rates)
    
    # convert time in seconds into the datetime format
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
    
    return rates_frame