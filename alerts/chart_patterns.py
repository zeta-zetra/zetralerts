"""
Alerts for Chart patterns

Date   : 2023-07-28
Author : Zetra 
"""

import chime 

from typing import List 

# Own modules
from sources.fxcm import get_data_from_fxcm
from chart_patterns.triangle import detect_triangle
from chart_patterns.rounding_bottom import detect_rounding_bottom
from alerts.utils import trigger_message


# Set the sound notification for local development
chime.theme("zelda")


def alerts_chart_patterns(symbol: str, timeframe: str, pattern: List[str] = ["triangle", "rounding_bottom"], **kwargs) -> bool:
    """
    Check alerts for chart patterns
    
    :params symbol is the currency pair 
    :type :str 
    
    :params timeframe is the trading timeframe
    :type :str 
    
    :params pattern is the type of patterns to find. Options: ["triangle", "rounding_bottom"]
    :type :List[str]
    
    :return: (bool)
    """
    
    ohlc = get_data_from_fxcm(symbol, timeframe, bars=30)

    for ptn in pattern:
        if ptn == "triangle": 
            resp    = detect_triangle(ohlc)
            message = "Triangle pattern has been found."

        
        elif ptn == "rounding_bottom":
            resp    = detect_rounding_bottom(ohlc)
            message = "Rounding bottom pattern has been found." 
            
        if resp:
            if not LIVE:
                chime.success(sync=True)
            trigger_message(message)            
            
    return False 