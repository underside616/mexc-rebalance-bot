import ccxt
import time
import os

api_key = os.environ.get('MEXC_API_KEY')
api_secret = os.environ.get('MEXC_SECRET_KEY')

exchange = ccxt.mexc({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True
})

symbol = 'BTC/USDT'
threshold = 0.01  # 1%

def rebalance():
    ticker = exchange.fetch_ticker(symbol)
    price = ticker['last']

    balance = exchange.fetch_balance()
    btc = balance['total'].get('BTC', 0)
    usdt = balance['total'].get('USDT', 0)

    btc_value = btc * price
    total_value = btc_value + usdt
    target_value = total_value / 2
    delta = abs(btc_value - target_value) / total_value

    print(f"Баланс: BTC={btc}, USDT={usdt}, BTC в $: {btc_value}, Цель: {target_value}, Δ={delta:.4f}")

    if delta < threshold:
        print("✅ Баланс в пределах 50/50 — ничего не делаем.")
        return

    if btc_value > target_value:
        amount_to_sell = (btc_value - target_value) / price
        order = exchange.create_market_sell_order(symbol, round(amount_to_sell, 6))
        print("🔻 Продали BTC:", order)
    else:
        amount_to_buy = (target_value - btc_value) / price
        order = exchange.create_market_buy_order(symbol, round(amount_to_buy, 6))
        print("🟢 Купили BTC:", order)

while True:
    try:
        rebalance()
    except Exception as e:
        print("❌ Ошибка:", e)
    time.sleep(300)
