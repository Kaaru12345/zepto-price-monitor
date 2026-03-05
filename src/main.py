import requests
import schedule
import time
import random
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# TEST PRINT
# print("BOT TOKEN:", BOT_TOKEN)
# print("CHAT ID:", CHAT_ID)

# Zepto API
API_URL = "https://bff-gateway.zepto.com/cart-service/api/v1/cart/product-detail"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json",
    "platform": "WEB",
    "store_id": "b4dc8d65-ed2e-4142-81b6-373982b13500",
    "storeIds": "b4dc8d65-ed2e-4142-81b6-373982b13500"
}

PAYLOAD = {
    "cartProducts": [
        {
            "productVariantId": "6a09750b-2bb7-4d1b-90f9-cd2a66269bfd",
            "quantity": 1
        }
    ]
}

# Random emoji list
EMOJIS = ["☕", "🔥", "🚀", "😎", "💸", "👀", "🤑", "⚡"]


def random_emoji():
    return random.choice(EMOJIS)


def send_telegram(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=payload)


def check_price():

    print("Checking price at:", datetime.now())

    try:

        response = requests.post(API_URL, json=PAYLOAD, headers=HEADERS)

        data = response.json()

        product = data["cartProductResponse"][0]

        name = product["product"]["name"]

        price_paise = product["discountedSellingPrice"]

        price_rupees = price_paise / 100

        print("Product:", name)
        print("Current Price: ₹", price_rupees)

        emoji = random_emoji()

        # Send live update every check
        update_message = f"{emoji} Price Check\n{name}\nPrice: ₹{price_rupees}"

        send_telegram(update_message)

        if price_rupees <= 99:

            alert_message = f"🚨 PRICE DROP!\n{name} is now ₹{price_rupees} {emoji}"

            print(alert_message)

            send_telegram(alert_message)

        else:
            print("Price still above ₹99\n")

    except Exception as e:
        print("Error:", e)


# Run every 2 minutes
schedule.every(2).minutes.do(check_price)

print("Zepto Price Monitor Started...")

send_telegram("🤖 Zepto Price Monitor Started")

# Run forever
try:

    while True:
        schedule.run_pending()
        time.sleep(1)

except KeyboardInterrupt:

    print("Bot stopped")