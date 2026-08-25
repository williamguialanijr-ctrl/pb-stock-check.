import os
import time
import requests
from bs4 import BeautifulSoup

PRODUCT_URL = "https://p-bandai.com/tw/item/A2866729001"
WEBHOOK_URL = "https://discord.com/api/webhooks/1541634045362970725/ceoT9Mc9m1vzqy613p5r_I9LjU-wO5J0J4FDBD5X0wdop4sBDmPBTvIMQwNyUPPxT2s6"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7"
}

for i in range(5):
    try:
        response = requests.get(PRODUCT_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text()

        # Handle IP blocks / access issues
        if response.status_code != 200 or "Access Denied" in page_text:
            print(f"[{i+1}/5] Page blocked or loading issue (Status {response.status_code}).")

        # Explicitly check if it's currently OUT OF STOCK (English or Chinese)
        elif "SORRY, OUT OF STOCK" in page_text or "OUT OF STOCK" in page_text or "缺貨" in page_text:
            print(f"[{i+1}/5] Out of stock. Waiting 60s...")

        # If "OUT OF STOCK" is no longer found, trigger the alert!
        else:
            payload = {
                "content": "@everyone 🚨 **ONE PIECE CARD COLLECTION IS BACK IN STOCK / PRE-ORDER OPEN!** 🚨\nhttps://p-bandai.com/tw/item/A2866729001"
            }
            requests.post(WEBHOOK_URL, json=payload)
            print(f"[{i+1}/5] In stock! Alert sent to Discord.")
            break

    except Exception as e:
        print(f"[{i+1}/5] Error checking stock: {e}")

    if i < 4:
        time.sleep(60)
