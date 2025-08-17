import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# 🔹 Your Telegram details
TELEGRAM_TOKEN = "7572360149:AAHrjTAhjcpLyHJVPNQRM2TE64EDD0qCC-4"
TELEGRAM_CHAT_ID = "7443910565"

# 🔹 Zingoy URL
URL = "https://www.zingoy.com/gift-cards/croma-retail"

# Counter for number of checks today
CHECK_COUNT = 0

def send_telegram_message(message, image_url=None):
    """Send message (and optional image) to Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)

    # If image_url is given, send photo
    if image_url:
        photo_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        requests.post(photo_url, data={"chat_id": TELEGRAM_CHAT_ID, "photo": image_url})

def check_cashback():
    global CHECK_COUNT
    CHECK_COUNT += 1

    try:
        response = requests.get(URL, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find cashback percentage
        cashback_text = soup.get_text()
        cashback_percent = 0

        for word in cashback_text.split():
            if "%" in word:
                try:
                    cashback_percent = float(word.replace("%", "").strip())
                    break
                except:
                    continue

        # Current time
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if cashback_percent >= 22:
            message = (
                f"🔥 <b>Profitable Cashback Alert!</b>\n\n"
                f"✅ Cashback Found: <b>{cashback_percent}%</b>\n"
                f"🕒 Checked at: <b>{now}</b>\n"
                f"🔄 Checks today: <b>{CHECK_COUNT}</b>\n\n"
                f"💰 <i>Great time to buy Croma Gift Cards!</i>"
            )
            send_telegram_message(message, image_url="https://i.ibb.co/DQk9YFh/money.jpg")

        else:
            message = (
                f"⚠️ <b>Low Cashback</b>\n\n"
                f"❌ Cashback Now: <b>{cashback_percent}%</b>\n"
                f"🕒 Checked at: <b>{now}</b>\n"
                f"🔄 Checks today: <b>{CHECK_COUNT}</b>\n\n"
                f"🙅 Don’t buy now, wait for a better deal."
            )
            send_telegram_message(message, image_url="https://i.ibb.co/SXhhJMy/warning.jpg")

    except Exception as e:
        send_telegram_message(f"❌ Error checking cashback: {e}")

if __name__ == "__main__":
    check_cashback()
