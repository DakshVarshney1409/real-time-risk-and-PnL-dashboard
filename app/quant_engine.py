import pandas as pd
import numpy as np
from typing import List, Dict

# 1. Simulation Data Setup
# In a real system, this would load from a dedicated data store.
def get_historical_returns(symbols: List[str], days: int = 252) -> pd.DataFrame:
    """Simulates daily stock returns for VaR calculation."""
    np.random.seed(42) # for reproducibility
    data = {}
    for symbol in symbols:
        # Simulate returns around 0 with a standard deviation of 1.5%
        daily_returns = np.random.normal(0, 0.015, days)
        data[symbol] = daily_returns
        
    return pd.DataFrame(data)

def calculate_pnl_and_var(position_data: Dict, historical_returns: pd.DataFrame) -> Dict:
    """
    Calculates Mark-to-Market (MtM) P&L and 95% Historical VaR.
    """
    symbol = position_data['symbol']
    quantity = position_data['quantity']
    avg_cost = position_data['average_cost']
    market_price = position_data['market_price']
    
    results = {}

    # --- P&L Calculation (Mark-to-Market) ---
    results['mtm_pnl'] = quantity * (market_price - avg_cost)
    
    # --- Historical VaR Calculation (95%) ---
    if symbol not in historical_returns.columns:
        results['historical_var_95'] = 0.0
        return results

    # 1. Calculate historical P&L for the current position
    position_value = quantity * market_price
    historical_pnl = position_value * historical_returns[symbol]

    # 2. Find the 5th percentile (the maximum expected loss at 95% confidence)
    var_95 = historical_pnl.quantile(0.05)
    
    # Store the VaR as a positive loss value
    results['historical_var_95'] = abs(var_95) 

    return results