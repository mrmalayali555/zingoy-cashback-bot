import requests
from bs4 import BeautifulSoup

# Your Telegram details
TOKEN = "7572360149:AAHrjTAhjcpLyHJVPNQRM2TE64EDD0qCC-4"
CHAT_ID = "6013173295"

URL = "https://www.zingoy.com/gift-cards/croma-retail"

def send_telegram(msg):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")

def check_cashback():
    response = requests.get(URL, timeout=30)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()
    if "19 % Cashback" in text or "18 % Cashback" in text:
        send_telegram("✅ Cashback found! It's profitable to buy gift card now!")
    else:
        send_telegram("❌ Cashback below 18%, not profitable.")

if __name__ == "__main__":
    check_cashback()
