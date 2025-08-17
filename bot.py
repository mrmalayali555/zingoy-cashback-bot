import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

# Telegram credentials
TELEGRAM_TOKEN = "7572360149:AAHrjTAhjcpLyHJVPNQRM2TE64EDD0qCC-4"
TELEGRAM_CHAT_ID = "7443910565"

URL = "https://www.zingoy.com/gift-cards/croma-retail"

check_count = 0
bot_started = False  # flag to ensure "bot started" message only once


def send_telegram(message):
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


def extract_cashback(soup, html_text):
    """Try multiple methods to get cashback percentage"""
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

    # Method 2: regex search in raw HTML/text
    matches = re.findall(r"(\d+)\s*% Cashback", html_text, flags=re.IGNORECASE)
    for m in matches:
        try:
            val = float(m.strip())
            if 0 < val < 100:
                values.append(val)
        except:
            continue

    return max(values) if values else None


def check_cashback():
    global check_count, bot_started
    check_count += 1

    try:
        response = requests.get(URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        cashback_value = extract_cashback(soup, response.text)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Send "bot started" message only once
        if not bot_started:
            send_telegram("🤖 Bot started successfully!\n\nNow monitoring Croma cashback every 10 minutes (GitHub Actions limit).")
            bot_started = True

        # If no cashback found, skip silently (no spam)
        if cashback_value is None:
            return

        # Only notify if cashback ≥ 22
        if cashback_value >= 22:
            message = (
                "🚀 <b>Cashback Alert!</b>\n\n"
                f"🎯 Cashback Rate: <b>{cashback_value}%</b>\n"
                "✅ Profitable to buy now!\n\n"
                f"⏰ Checked at: {now}\n"
                f"🔄 Total checks today: {check_count}\n\n"
                "👉 <a href='https://www.zingoy.com/gift-cards/croma-retail'>Buy Croma Gift Card</a>"
            )
            send_telegram(message)

    except Exception as e:
        send_telegram(f"⚠️ Error fetching cashback data: {e}")


if __name__ == "__main__":
    check_cashback()
