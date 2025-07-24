# utils/sp500_loader.py

import csv

def load_sp500_symbols(filepath='data/sp500.csv'):
    """
    Loads list of S&P500 symbols from CSV file.
    Returns a list of strings (tickers).
    """
    symbols = []
    try:
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                symbol = row.get('symbol', '').strip().upper()
                if symbol:
                    symbols.append(symbol)
    except Exception as e:
        print(f"Error loading S&P500 list: {e}")
    
    return symbols
