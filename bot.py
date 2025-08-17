import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# --- Telegram credentials ---
TELEGRAM_TOKEN = "7572360149:AAHrjTAhjcpLyHJVPNQRM2TE64EDD0qCC-4"
TELEGRAM_CHAT_ID = "7443910565"

# --- Target cashback threshold ---
TARGET_CASHBACK = 22

# --- Counters ---
check_count = 0
start_date = datetime.now().date()


def send_telegram_message(message, image_url=None):
    """Send message (and optional image) to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

    if image_url:
        img_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "photo": image_url,
            "caption": "🖼 Cashback Snapshot"
        }
        requests.post(img_url, data=payload)


def get_cashback():
    """Scrape cashback % from Zingoy Croma page"""
    url = "https://www.zingoy.com/gift-cards/croma-retail"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=30)
    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text()
    cashback = 0
    for word in text.split():
        if word.replace("%", "").isdigit():
            val = int(word.replace("%", ""))
            if val > cashback:
                cashback = val
    return cashback


def main():
    global check_count, start_date
    # Reset daily counter
    if datetime.now().date() != start_date:
        start_date = datetime.now().date()
        check_count = 0

    check_count += 1
    cashback = get_cashback()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if cashback >= TARGET_CASHBACK:
        message = (
            f"🚀 <b>Cashback Alert!</b>\n\n"
            f"🎯 Cashback Rate: <b>{cashback}%</b>\n"
            f"✅ Profitable to buy now!\n\n"
            f"⏰ Checked at: <b>{now}</b>\n"
            f"🔄 Total checks today: <b>{check_count}</b>\n\n"
            f"👉 <a href='https://www.zingoy.com/gift-cards/croma-retail'>Buy Croma Gift Card</a>"
        )
        send_telegram_message(message, image_url="https://i.imgur.com/fNZU7eB.png")
    else:
        message = (
            f"❌ <b>Low Cashback</b>\n\n"
            f"🎯 Cashback Rate: <b>{cashback}%</b>\n"
            f"⚠️ Don’t buy now, waiting for better rate...\n\n"
            f"⏰ Checked at: <b>{now}</b>\n"
            f"🔄 Total checks today: <b>{check_count}</b>"
        )
        send_telegram_message(message)


if __name__ == "__main__":
    main()
