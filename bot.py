import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Telegram credentials
TELEGRAM_TOKEN = "7572360149:AAHrjTAhjcpLyHJVPNQRM2TE64EDD0qCC-4"
TELEGRAM_CHAT_ID = "7443910565"

URL = "https://www.zingoy.com/gift-cards/croma-retail"

check_count = 0

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Error sending Telegram message:", e)

def check_cashback():
    global check_count
    check_count += 1

    try:
        response = requests.get(URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        # Find ALL cashback spans
        rate_tags = soup.select("span.cb-rate")

        cashback_values = []
        for tag in rate_tags:
            text = tag.get_text(strip=True)
            if text.endswith("%"):
                try:
                    val = float(text.replace("%", "").strip())
                    # Ignore weirdly large values (junk from the page)
                    if 0 < val < 100:
                        cashback_values.append(val)
                except:
                    continue

        if not cashback_values:
            send_telegram("⚠️ Could not find cashback info on Zingoy page.")
            return

        cashback_value = max(cashback_values)  # take the highest valid %

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if cashback_value >= 22:
            message = (
                "🚀 <b>Cashback Alert!</b>\n\n"
                f"🎯 Cashback Rate: <b>{cashback_value}%</b>\n"
                "✅ Profitable to buy now!\n\n"
                f"⏰ Checked at: {now}\n"
                f"🔄 Total checks today: {check_count}\n\n"
                "👉 <a href='https://www.zingoy.com/gift-cards/croma-retail'>Buy Croma Gift Card</a>"
            )
        else:
            message = (
                "❌ <b>Low Cashback</b>\n\n"
                f"🎯 Cashback Rate: <b>{cashback_value}%</b>\n"
                "⚠️ Don’t buy now, cashback is too low.\n\n"
                f"⏰ Checked at: {now}\n"
                f"🔄 Total checks today: {check_count}\n\n"
                "👉 <a href='https://www.zingoy.com/gift-cards/croma-retail'>Check Croma Gift Card</a>"
            )

        send_telegram(message)

    except Exception as e:
        send_telegram(f"⚠️ Error fetching cashback data: {e}")

if __name__ == "__main__":
    check_cashback()
