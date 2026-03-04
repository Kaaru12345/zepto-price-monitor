import requests
import schedule
import time
from datetime import datetime

# TELEGRAM SETTINGS
BOT_TOKEN = "8757257863:AAExdRCyGSdWWPX7GhdTESMzxFRUAPhhdtg"
CHAT_ID = "5641783027"

# ZEPTO API
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

        if price_rupees <= 99:
        # if True:

            alert_message = f"☕ Zepto Price Drop!\n{name} is now ₹{price_rupees}"

            print(alert_message)

            send_telegram(alert_message)

        else:
            print("Price still above ₹99\n")

    except Exception as e:
        print("Error:", e)


# run every 5 minutes
schedule.every(2).minutes.do(check_price)

print("Zepto Price Monitor Started...")

# send startup message
send_telegram("🤖 Zepto Price Monitor Started")

try:
    while True:
        schedule.run_pending()
        time.sleep(1)

except KeyboardInterrupt:
    print("\nBot stopped by user.")