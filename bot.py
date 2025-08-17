import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import os

# Telegram credentials
TELEGRAM_TOKEN = "7572360149:AAHrjTAhjcpLyHJVPNQRM2TE64EDD0qCC-4"
TELEGRAM_CHAT_ID = "7443910565"

URL = "https://www.zingoy.com/gift-cards/croma-retail"
START_FILE = "bot_started.txt"  # file to remember if start message was sent

def send_telegram(message):
    """Send a message to your Telegram chat"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Error sending Telegram message:", e)

def send_start_message():
    """Send start message only once"""
    if not os.path.exists(START_FILE):
        send_telegram("🤖 Bot started successfully!\n\nNow monitoring Croma cashback.")
        with open(START_FILE, "w") as f:
            f.write("started")

def extract_cashback(soup, html_text):
    """Extract cashback percentage from the page"""
    values = []

    # Method 1: span.cb-rate
    for tag in soup.select("span.cb-rate"):
        txt = tag.get_text(strip=True)
        if txt.endswith("%"):
            try:
                val = float(txt.replace("%", "").strip())
                if 0 < val < 100:
                    values.append(val)
            except:
                continue

    # Method 2: regex in raw HTML/text
    matches = re.findall(r"(\d+(?:\.\d+)?)\s*% Cashback", html_text, flags=re.IGNORECASE)
    for m in matches:
        try:
            val = float(m.strip())
            if 0 < val < 100:
                values.append(val)
        except:
            continue

    return max(values) if values else None

def check_cashback():
    """Check the cashback once and send alert only if profitable"""
    try:
        response = requests.get(URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        cashback_value = extract_cashback(soup, response.text)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if cashback_value is None:
            print(f"{now} — Cashback not found")
            return

        # Only send message if cashback >= 22%
        if cashback_value >= 22:
            message = (
                "🚀 <b>Cashback Alert!</b>\n\n"
                f"🎯 Cashback Rate: <b>{cashback_value}%</b>\n"
                "✅ Profitable to buy now!\n\n"
                f"⏰ Checked at: {now}\n\n"
                "👉 <a href='https://www.zingoy.com/gift-cards/croma-retail'>Buy Croma Gift Card</a>"
            )
            send_telegram(message)
            print(f"{now} — Message sent: Cashback {cashback_value}%")
        else:
            print(f"{now} — Cashback {cashback_value}% — Not profitable, no message sent")

    except Exception as e:
        print(f"{datetime.now()} — Error: {e}")

if __name__ == "__main__":
    send_start_message()  # send bot started message once
    check_cashback()      # check cashback once per run
