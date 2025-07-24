# bot.py – גרסה מחודשת מלאה

import time
from ib_insync import *
from utils.logger import log_event
from utils.trading import connect_to_ib, place_market_order, disconnect_from_ib
from utils.sp500_loader import load_sp500_symbols

# הגדרות
CHECK_INTERVAL = 60  # שניות בין סריקות
VOLUME_THRESHOLD = 1.2  # פי כמה מהממוצע נחשב חריג


def is_market_open():
    from datetime import datetime
    now = datetime.now().time()
    return datetime.strptime("16:30", "%H:%M").time() <= now <= datetime.strptime("23:00", "%H:%M").time()


def average_volume(bars):
    if len(bars) < 2:
        return 0
    return sum(bar.volume for bar in bars[:-1]) / (len(bars) - 1)


def check_volume_and_trade(ib, symbol):
    stock = Stock(symbol, 'SMART', 'USD')
    ib.qualifyContracts(stock)

    bars = ib.reqHistoricalData(
        stock,
        endDateTime='',
        durationStr='2 D',
        barSizeSetting='1 min',
        whatToShow='TRADES',
        useRTH=True,
        formatDate=1
    )

    if not bars:
        log_event(f"לא התקבלו נתונים עבור {symbol}")
        return

    avg_vol = average_volume(bars)
    current_vol = bars[-1].volume

    log_event(f"{symbol} - ווליום נוכחי: {current_vol}, ממוצע: {avg_vol}")

    if current_vol > avg_vol * VOLUME_THRESHOLD:
        log_event(f"📈 כניסה אפשרית ל-{symbol} (ווליום חריג)")
        order = MarketOrder('BUY', 1)
        trade = place_market_order(ib, stock, order)
        while not trade.isDone():
            ib.waitOnUpdate()
        log_event(f"✅ בוצעה רכישה של {symbol}, סטטוס: {trade.orderStatus.status}")


def run_bot():
    log_event("🚀 התחלת פעילות הבוט")
    symbols = load_sp500_symbols()
    ib = connect_to_ib()

    try:
        while True:
            if is_market_open():
                for symbol in symbols:
                    check_volume_and_trade(ib, symbol)
            else:
                log_event("שוק סגור – ממתין לפתיחה...")
            time.sleep(CHECK_INTERVAL)
    finally:
        disconnect_from_ib(ib)


if __name__ == "__main__":
    run_bot()
