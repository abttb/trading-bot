# bot.py – גרסה מחודשת עם ניהול תקציב

import time
from ib_insync import *
from utils.logger import log_event
from utils.trading import connect_to_ib, place_market_order, disconnect_from_ib, get_available_funds
from utils.sp500_loader import load_sp500_symbols

# הגדרות
CHECK_INTERVAL = 60  # שניות בין סריקות
VOLUME_THRESHOLD = 1.2  # פי כמה מהממוצע נחשב חריג
MAX_POSITIONS = 10  # כמות מניות מקסימלית לפתיחה במקביל
MIN_TRADE_AMOUNT = 50  # סכום מינימלי לעסקה (ב-$)


def is_market_open():
    from datetime import datetime
    now = datetime.now().time()
    return datetime.strptime("16:30", "%H:%M").time() <= now <= datetime.strptime("23:00", "%H:%M").time()


def average_volume(bars):
    if len(bars) < 2:
        return 0
    return sum(bar.volume for bar in bars[:-1]) / (len(bars) - 1)


def check_volume_and_trade(ib, symbol, budget_per_trade):
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
        return False

    avg_vol = average_volume(bars)
    current_vol = bars[-1].volume
    price = bars[-1].close

    log_event(f"{symbol} - ווליום נוכחי: {current_vol}, ממוצע: {avg_vol}, מחיר: {price}")

    if current_vol > avg_vol * VOLUME_THRESHOLD and price > 0:
        qty = int(budget_per_trade // price)
        if qty < 1:
            log_event(f"⛔ תקציב לא מספיק לרכישת {symbol}")
            return False
        log_event(f"📈 כניסה ל-{symbol}, כמות: {qty}, לפי מחיר: {price}")
        order = MarketOrder('BUY', qty)
        trade = place_market_order(ib, stock, order)
        while not trade.isDone():
            ib.waitOnUpdate()
        log_event(f"✅ בוצעה רכישה של {symbol}, סטטוס: {trade.orderStatus.status}")
        return True
    return False


def run_bot():
    log_event("🚀 התחלת פעילות הבוט עם ניהול תקציב")
    symbols = load_sp500_symbols()
    ib = connect_to_ib()

    try:
        available_funds = get_available_funds(ib)
        budget_per_trade = max(available_funds / MAX_POSITIONS, MIN_TRADE_AMOUNT)
        log_event(f"📊 תקציב זמין: ${available_funds:.2f}, תקציב לעסקה: ${budget_per_trade:.2f}")

        opened_positions = 0
        while True:
            if is_market_open():
                for symbol in symbols:
                    if opened_positions >= MAX_POSITIONS:
                        log_event("📛 הגעתי למספר עסקאות מקסימלי")
                        break
                    success = check_volume_and_trade(ib, symbol, budget_per_trade)
                    if success:
                        opened_positions += 1
            else:
                log_event("שוק סגור – ממתין לפתיחה...")
            time.sleep(CHECK_INTERVAL)
    finally:
        disconnect_from_ib(ib)


if __name__ == "__main__":
    run_bot()
