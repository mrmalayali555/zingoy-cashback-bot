import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Telegram details
TELEGRAM_TOKEN = "7572360149:AAHrjTAhjcpLyHJVPNQRM2TE64EDD0qCC-4"
TELEGRAM_CHAT_ID = "7443910565"

# Zingoy Croma page
URL = "https://www.zingoy.com/gift-cards/croma-retail"
CHECK_COUNT = 0

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)

def check_cashback():
    global CHECK_COUNT
    CHECK_COUNT += 1

    try:
        response = requests.get(URL, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract cashback from div.cb-rate
        cashback_div = soup.select_one("div.cb-rate")
        if cashback_div:
            cashback_text = cashback_div.get_text(strip=True)
            cashback_percent = float(cashback_text.replace("%", "").strip())
        else:
            cashback_percent = 0

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if cashback_percent >= 22:
            message = (
                f"🚀 <b>Cashback Alert!</b>\n\n"
                f"🎯 Cashback Rate: <b>{cashback_percent}%</b>\n"
                f"✅ Profitable to buy now!\n\n"
                f"⏰ Checked at: {now}\n"
                f"🔄 Total checks today: {CHECK_COUNT}\n\n"
                f"👉 <a href='{URL}'>Buy Croma Gift Card</a>"
            )
        else:
            message = (
                f"⚠️ <b>Low Cashback</b>\n\n"
                f"🎯 Cashback Rate: <b>{cashback_percent}%</b>\n"
                f"❌ Don’t buy now, wait for better offer.\n\n"
                f"⏰ Checked at: {now}\n"
                f"🔄 Total checks today: {CHECK_COUNT}"
            )

        send_telegram(message)

    except Exception as e:
        send_telegram(f"❌ Error while checking cashback: {e}")

if __name__ == "__main__":
    check_cashback()
