# utils/trading.py

from ib_insync import *
from utils.logger import log_event

def connect_to_ib(host='127.0.0.1', port=7497, client_id=1):
    ib = IB()
    try:
        ib.connect(host, port, clientId=client_id)
        log_event("✅ התחברות ל-Interactive Brokers הצליחה")
        return ib
    except Exception as e:
        log_event(f"❌ שגיאה בהתחברות ל-IB: {e}")
        raise

def place_market_order(ib, contract, order):
    try:
        trade = ib.placeOrder(contract, order)
        log_event(f"📤 נשלחה פקודת שוק: {order}")
        return trade
    except Exception as e:
        log_event(f"❌ שגיאה בשליחת פקודת קנייה: {e}")
        raise

def disconnect_from_ib(ib):
    try:
        ib.disconnect()
        log_event("🔌 נותק מהחשבון של Interactive Brokers")
    except Exception as e:
        log_event(f"⚠️ שגיאה בניתוק: {e}")

def get_available_funds(ib):
    """
    Returns available funds or NetLiquidation from IB account summary.
    """
    summary = ib.accountSummary()
    try:
        return float(summary.loc['NetLiquidation', 'value'])
    except Exception as e:
        log_event(f"⚠️ שגיאה בקריאת תקציב מהחשבון: {e}")
        return 0
