import ccxt
import time
import os

# 🔑 Ключи из переменных окружения
api_key = os.environ.get('MEXC_API_KEY')
api_secret = os.environ.get('MEXC_SECRET_KEY')

# 🔌 Подключение к MEXC через ccxt
exchange = ccxt.mexc({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True
})

# ⚙️ Настройки
symbol = 'BTC/USDT'
threshold = 0.01  # 1% дисбаланс

# 🔁 Основная функция ребаланса
def rebalance():
    print("🌀 rebalance() вызван — всё работает")

    ticker = exchange.fetch_ticker(symbol)
    price = ticker['last']

    balance = exchange.fetch_balance()
    btc = balance['total'].get('BTC', 0)
    usdt = balance['total'].get('USDT', 0)

    btc_value = btc * price
    total_value = btc_value + usdt
    target_value = total_value / 2

    delta = abs(btc_value - target_value) / total_value

    if delta < threshold:
        print("✅ Баланс 50/50 — ничего не делаем.")
        return

    if btc_value > target_value:
        amount_to_sell = (btc_value - target_value) / price
        order = exchange.create_market_sell_order(symbol, round(amount_to_sell, 6))
        print("🔻 Продали BTC:", order)
    else:
        amount_to_buy = (target_value - btc_value) / price
        order = exchange.create_market_buy_order(symbol, round(amount_to_buy, 6))
        print("🔼 Купили BTC:", order)

# 🔄 Бесконечный цикл с паузой
while True:
    try:
        rebalance()
    except Exception as e:
        print("❌ Ошибка:", e)
    time.sleep(10)  # каждый 10 секунд (можно вернуть 300)
