import requests
from bs4 import BeautifulSoup
import os
import datetime
import re

# Telegram credentials
TELEGRAM_TOKEN = "7572360149:AAHrjTAhjcpLyHJVPNQRM2TE64EDD0qCC-4"
TELEGRAM_CHAT_ID = "7443910565"

# Tracking checks
CHECK_COUNT = 0
BEST_RATE = 0

def send_message(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})

def check_cashback():
    global CHECK_COUNT, BEST_RATE
    CHECK_COUNT += 1

    url = "https://www.zingoy.com/gift-cards/croma-retail"
    response = requests.get(url, timeout=30)
    soup = BeautifulSoup(response.text, "html.parser")

    # Grab cashback text directly
    cb_element = soup.find("div", class_="cb-rate")
    if not cb_element:
        send_message("⚠️ Cashback element not found on Zingoy page!")
        return

    # Extract % number safely
    cb_text = cb_element.get_text(strip=True)
    match = re.search(r"(\d+)%", cb_text)
    if not match:
        send_message(f"⚠️ Could not parse cashback value: {cb_text}")
        return

    cashback = int(match.group(1))
    BEST_RATE = max(BEST_RATE, cashback)

    # Build attractive message
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if cashback >= 22:
        msg = (
            f"🚀 *Cashback Alert!*\n\n"
            f"🎯 Cashback Rate: *{cashback}%*\n"
            f"✅ Profitable to buy now!\n\n"
            f"⏰ Checked at: {now}\n"
            f"🔄 Total checks today: {CHECK_COUNT}\n"
            f"🏆 Best today: {BEST_RATE}%\n\n"
            f"👉 [Buy Croma Gift Card](https://www.zingoy.com/gift-cards/croma-retail)"
        )
    else:
        msg = (
            f"⚠️ *Low Cashback*\n\n"
            f"🎯 Cashback Rate: *{cashback}%*\n"
            f"❌ Don’t buy now, wait for better offer.\n\n"
            f"⏰ Checked at: {now}\n"
            f"🔄 Total checks today: {CHECK_COUNT}\n"
            f"🏆 Best today: {BEST_RATE}%\n\n"
            f"👉 [Check Again](https://www.zingoy.com/gift-cards/croma-retail)"
        )

    send_message(msg)

if __name__ == "__main__":
    check_cashback()
