
import time
from datetime import datetime
from ib_insync import *

# חיבור ל-IB Gateway
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

def is_market_open():
    now = datetime.now().time()
    return now >= datetime.strptime("16:30", "%H:%M").time() and now <= datetime.strptime("23:00", "%H:%M").time()

def check_volume_and_trade(stock):
    bars = ib.reqHistoricalData(
        stock,
        endDateTime='',
        durationStr='2 D',
        barSizeSetting='1 min',
        whatToShow='TRADES',
        useRTH=True,
        formatDate=1
    )
    if len(bars) < 2:
        return
    avg_volume = sum([bar.volume for bar in bars[:-1]]) / len(bars[:-1])
    current_volume = bars[-1].volume

    if current_volume > avg_volume * 1.2:
        print(f"נכנסים לעסקה: {stock.symbol} - ווליום גבוה")
        # כאן תכניס את פקודת הקנייה לפי תנאי המגמה

def run_bot():
    stock_list = ['AAPL', 'MSFT', 'GOOGL']
    while True:
        if is_market_open():
            for symbol in stock_list:
                stock = Stock(symbol, 'SMART', 'USD')
                check_volume_and_trade(stock)
        else:
            print("שוק סגור, ממתין לפתיחה...")
        time.sleep(60)

if __name__ == "__main__":
    run_bot()
