import pandas as pd 
import pandas_ta as ta 

from sources.fxcm import get_data_from_fxcm

def rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    Calculate the RSI 
    
    :params df is the OHLC data 
    :type :pd.DataFrame
    
    :params period is the length 
    :type :int 
    
    :return: (pd.DataFrame)
    """
    

    return df.ta.rsi(length = period)
    
    
def fibonacci_lines(symbol: str, target_timeframe: str = "1d", bars: int=2, source:str = "FXCM") -> pd.DataFrame:
    """
    Get the Fibonacci Pivot Points
    
    :params symbol is the currency pair
    :type :str 
    
    :params target_timeframe is the timeframe that will be traded 
    :type :str 
    
    :params bars is the number of bars to request 
    :type :int 
    
    :params source is the Broker to use to fetch data. Options: ['FXCM','MT5'] 
    :type :str  
    
    :return: (pd.DataFrame)
    """
    
    if source == "FXCM":
        df = get_data_from_fxcm(symbol, timeframe=target_timeframe, bars=bars)
    
    df["pp"] = (df["high"] + df["low"] + df["close"])/3
    
    df["r1"] = df["pp"]*2 - df["low"]
    df["s1"] = df["pp"]*2 - df["high"]
    
    df["r2"] = df["pp"] + (df["high"] - df["low"])
    df["s2"] = df["pp"] - (df["high"] - df["low"])

    # Shift the Pivot Points
    df["pp"] = df["pp"].shift(1)
    df["r1"] = df["r1"].shift(1)
    df["s1"] = df["s1"].shift(1)
    df["r2"] = df["r2"].shift(1)
    df["s2"] = df["s2"].shift(1)
    
    return df.iloc[1,:]
    