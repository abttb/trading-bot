# utils/config.py

import os

def get_target_stocks():
    """
    Returns a list of target stock tickers from environment variable TICKERS.
    Example: TICKERS=AAPL,MSFT,GOOG
    """
    tickers_str = os.getenv("TICKERS", "AAPL")
    tickers = [symbol.strip().upper() for symbol in tickers_str.split(",") if symbol.strip()]
    return tickers
