from ib_insync import *
from utils.logger import log_event

def connect_to_ib(host='127.0.0.1', port=7497, client_id=1):
    ib = IB()
    try:
        ib.connect(host, port, clientId=client_id)
        log_event("Connected to Interactive Brokers")
        return ib
    except Exception as e:
        log_event(f"Failed to connect to IB: {e}")
        raise

def place_market_order(ib, contract, order):
    try:
        trade = ib.placeOrder(contract, order)
        log_event(f"Market order placed: {order}")
        return trade
    except Exception as e:
        log_event(f"Failed to place order: {e}")
        raise

def disconnect_from_ib(ib):
    try:
        ib.disconnect()
        log_event("Disconnected from Interactive Brokers")
    except Exception as e:
        log_event(f"Failed to disconnect: {e}")
