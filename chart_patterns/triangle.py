"""
Find a triangle pattern

Author: Zetra
Date  : 2023-07-28
"""

import numpy as np
import os
import pandas as pd


from progress.bar import Bar 
from scipy.stats import linregress
from typing import List, Union


def pivot_id(ohlc: pd.DataFrame, l: int, n1: int, n2: int) -> int:
    """
    Get the pivot id 

    :params ohlc is a dataframe
    :type :pd.DataFrame
    
    :params l is the current row 
    :type :int
    
    :params n1 is the number of candles to the left
    :type :int
    
    :params n2 is the number of candles to the right
    :type :int
    
    :return: (int)  
    """

    # Check if the length conditions met
    if l-n1 < 0 or l+n2 >= len(ohlc):
        return 0
    
    pivot_low  = 1
    pivot_high = 1

    for i in range(l-n1, l+n2+1):
        if(ohlc.loc[l,"low"] > ohlc.loc[i, "low"]):
            pivot_low = 0

        if(ohlc.loc[l, "high"] < ohlc.loc[i, "high"]):
            pivot_high = 0

    if pivot_low and pivot_high:
        return 3

    elif pivot_low:
        return 1

    elif pivot_high:
        return 2
    else:
        return 0




def find_triangle_points(ohlc: pd.DataFrame, backcandles: int, triangle_type: str = "symmetrical") -> List[int]:
    """
    Find the triangle points based on the pivot points

    :params ohlc -> dataframe that has OHLC data
    :type :pd.DataFrame

    :params backcandles -> number of periods to lookback
    :type :int

    :params triangle_type -> Find a symmetrical, ascending or descending triangle? Options: ['symmetrical', 'ascending', 'descending']
    :type :str 

    :returns triangle points
    """
    all_triangle_points = []

    bar = Bar(f'Finding triangle points for {triangle_type}', max=len(ohlc))
    for candleid in range(backcandles+10, len(ohlc)):
        
        maxim = np.array([])
        minim = np.array([])
        xxmin = np.array([])
        xxmax = np.array([])

        for i in range(candleid-backcandles, candleid+1):
            if ohlc.loc[i,"pivot"] == 1:
                minim = np.append(minim, ohlc.loc[i, "low"])
                xxmin = np.append(xxmin, i) 
            if ohlc.loc[i,"pivot"] == 2:
                maxim = np.append(maxim, ohlc.loc[i,"high"])
                xxmax = np.append(xxmax, i)

       
        if (xxmax.size <3 and xxmin.size <3) or xxmax.size==0 or xxmin.size==0:
               continue

        slmin, intercmin, rmin, pmin, semin = linregress(xxmin, minim)
        slmax, intercmax, rmax, pmax, semax = linregress(xxmax, maxim)

        if triangle_type == "symmetrical":
            if abs(rmax)>=0.9 and abs(rmin)>=0.9 and slmin>=0.0001 and slmax<=-0.0001:
                all_triangle_points.append(candleid)

        elif triangle_type == "ascending":
            if abs(rmax)>=0.9 and abs(rmin)>=0.9 and slmin>=0.0001 and (slmax>=-0.00001 and slmax <= 0.00001):
                all_triangle_points.append(candleid)
    
        elif triangle_type == "descending":
            if abs(rmax)>=0.9 and abs(rmin)>=0.9 and slmax<=-0.0001 and (slmin>=-0.00001 and slmin <= 0.00001):
                all_triangle_points.append(candleid)

        bar.next()

    bar.finish()
    return all_triangle_points


def detect_triangle(df: pd.DataFrame, lookback: int = 20) -> bool:
    """
    Detect if a Triangle pattern has formed
    
    :params df is the OHLC dataframe
    :type :pd.DataFrame
    
    :params lookback is number of bars to use for detecting the pattern
    :type :int
    
    :return: (bool)
    """
    
    df["pivot"] = df.apply(lambda x: pivot_id(df, x.name, 3, 3), axis=1)

    for tt in ['symmetrical', 'ascending', 'descending']:
             pts   = find_triangle_points(df, lookback, triangle_type=tt)
             
             if len(pts) > 0:
                 return True 
             
    return False



