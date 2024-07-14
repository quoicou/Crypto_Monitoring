from datetime import datetime, time
import json
import requests
import yfinance as yf
import time as sleep_time
import pytz
import multiprocessing

def get_chat_id():
    chat_id = "-1273342593"

    return chat_id

def crypto_monitoring():
    start_time = time(17, 00)
    end_time = time(23, 30)

    while True:
        if start_time <= get_current_time() <= end_time:
            BTC_open, BTC_close, BTC_volume, ETH_open, ETH_close, SOL_open, SOL_close = top_crypto()
            send_crypto_monitoring_message(BTC_open, BTC_close, BTC_volume, ETH_open, ETH_close, SOL_open, SOL_close, fng_crypto())
            sleep_time.sleep(86400)
        else:
            print("Pas l'heure pour Veille Quotidienne Crypto")
            sleep_time.sleep(3600)

    print("Pas le jour pour Veille Quotidienne Crypto")
    sleep_time.sleep(86400)

def get_api_key():
    api_key = "7174292983:AAE2XlW4n-TrebDh3XCAlJ_P4k2qDwe6hpU"

    return api_key

def top_crypto():
    BTC_Ticker = yf.Ticker("BTC-USD")
    BTC = BTC_Ticker.history(period="today").drop(columns=["Dividends", "Stock Splits", "High", "Low"])

    BTC_open = f'{BTC["Open"].iloc[0]:.2f}'
    BTC_close = f'{BTC["Close"].iloc[0]:.2f}'
    BTC_volume = f'{BTC["Volume"].iloc[0]/ 1_000_000_000:.3f}'

    ETH_Ticker = yf.Ticker("ETH-USD")
    ETH = ETH_Ticker.history(period="today").drop(columns=["Dividends", "Stock Splits", "Volume", "High", "Low"])

    ETH_open = f'{ETH["Open"].iloc[0]:.2f}'
    ETH_close = f'{ETH["Close"].iloc[0]:.2f}'

    SOL_Ticker = yf.Ticker("SOL-USD")
    SOL = SOL_Ticker.history(period="today").drop(columns=["Dividends", "Stock Splits", "Volume", "High", "Low"])

    SOL_open = f'{SOL["Open"].iloc[0]:.2f}'
    SOL_close = f'{SOL["Close"].iloc[0]:.2f}'

    return BTC_open, BTC_close, BTC_volume, ETH_open, ETH_close, SOL_open, SOL_close

def get_current_time():
    tz = pytz.timezone('Asia/Shanghai')
    current_time = datetime.now(tz).time()

    return current_time

def fng_crypto():
    url = "https://api.alternative.me/fng/"

    response = requests.get(url)
    data = json.loads(response.content)
    fng_value = data.get("data")[0]["value"]

    return fng_value

def send_crypto_monitoring_message(BTC_open, BTC_close, BTC_volume, ETH_open, ETH_close, SOL_open, SOL_close, fng):
    text = f"⚠️ Monitoring ⚠️\n\n▶️ Fear N' Greed Crypto : {fng}\n\n▶️ Volume BTC : {BTC_volume} Mrds\n\n▶️ BTC : {BTC_open} -> {BTC_close}\n\n▶️ ETH : {ETH_open} -> {ETH_close}\n\n▶️ SOL : {SOL_open} -> {SOL_close}\n\n(Price in $)"

    print(text)

    url = f"https://api.telegram.org/bot{get_api_key()}/sendMessage?chat_id={get_chat_id()}&text={text}&silent=True"

    requests.get(url)

if __name__ == '__main__':
    process_1 = multiprocessing.Process(target=crypto_monitoring)

    process_1.start()
