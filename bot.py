import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.zingoy.com/gift-cards/croma-retail"

def check_cashback():
    response = requests.get(URL, timeout=30)
    soup = BeautifulSoup(response.text, "html.parser")

    cashback_text = soup.get_text()
    print("[DEBUG] Page text fetched")

    # Force a test cashback value (e.g., 19%)
    cashback_value = 19.0  

    if cashback_value >= 10:   # lowered threshold
        return cashback_value
    return None

def send_telegram_message(message: str):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}

    response = requests.post(url, data=data)
    print("[DEBUG] Telegram response:", response.text)

if __name__ == "__main__":
    cashback = check_cashback()
    if cashback:
        msg = f"[ALERT] Cashback {cashback}% found — profitable to buy gift card now!"
        print(msg)
        send_telegram_message(msg)
    else:
        print("[INFO] No profitable cashback found.")
