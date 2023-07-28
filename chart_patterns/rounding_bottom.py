"""
Find the rounding bottom

Date   : 2023-07-28
Author : Zetra
"""

import numpy as np
import os
import pandas as pd

from scipy.signal import argrelextrema


def find_rounding_bottom_points(df: pd.DataFrame, lookback: int) -> List[int]:
    """
    Find all the rounding bottom points

    :params df is the dataframe that has df data
    :type :pd.DataFrame
    
    :params lookback is the number of periods to lookback
    :type :int 
    
    :return: (all_points) 
    """
    
    all_points = []
    for candle_idx in range(lookback+10, len(df)):

        maxim = np.array([])
        minim = np.array([])
        xxmin = np.array([])
        xxmax = np.array([])

        for i in range(candle_idx-lookback, candle_idx+1):
            if df.loc[i,"pivot"] == 1:
                minim = np.append(minim, df.loc[i, "close"])
                xxmin = np.append(xxmin, i) 
            if df.loc[i,"pivot"] == 2:
                maxim = np.append(maxim, df.loc[i,"close"])
                xxmax = np.append(xxmax, i)

        
        if (xxmax.size <3 and xxmin.size <3) or xxmax.size==0 or xxmin.size==0:
            continue

        # Fit a nonlinear line: ax^2 + bx + c        
        z = np.polyfit(xxmin, minim, 2)

        # Check if the first and second derivatives are for a parabolic function
        if 2*xxmin[0]*z[0] + z[1]*xxmin[0] < 0 and 2*z[0] > 0:
             if z[0] >=2.19388889e-04 and z[1]<=-3.52871667e-02:          
                    all_points.append(candle_idx)
                                    

    return all_points


def find_pivots(df: pd.DataFrame) -> pd.DataFrame:
    """
    Find the pivots 
    
    :params df is the OHLC dataframe
    :type :pd.DataFrame
    
    :return: (pd.DataFrame)
    """

    # Get the minimas and maximas 
    local_max = argrelextrema(df["close"].values, np.greater)[0]
    local_min = argrelextrema(df["close"].values, np.less)[0]   

    # Set max points to `2` 
    for m in local_max:
        df.loc[m, "pivot"] = 2
        
    # Set min points to `1`
    for m in local_min:
        df.loc[m, "pivot"] = 1
        
    return df 


def detect_rounding_bottom(df: pd.DataFrame, lookback: int = 30) -> bool:
    """
    Detect the rounding bottom 
    
    :params df is the OHLC dataframe
    :type :pd.DataFrame
    
    :params lookback is the number of past periods to use 
    :type :int 
    
    :return: (bool)
    """
    
    df  = find_pivots(df) 
    pts = find_rounding_bottom_points(df, lookback=lookback)
    
    if len(pts) > 0:
        return True
    
    return False 
    
