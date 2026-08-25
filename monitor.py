import os
import time
import requests
from bs4 import BeautifulSoup

PRODUCT_URL = "https://p-bandai.com/tw/item/A2866729001"
WEBHOOK_URL = "https://discord.com/api/webhooks/1541634045362970725/ceoT9Mc9m1vzqy613p5r_I9LjU-wO5J0J4FDBD5X0wdop4sBDmPBTvIMQwNyUPPxT2s6"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Loops 5 times (1 check every 60 seconds = 5 continuous minutes)
for i in range(5):
    try:
        response = requests.get(PRODUCT_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text()

        if "OUT OF STOCK" not in page_text and "缺貨" not in page_text:
            payload = {
                "content": "@everyone 🚨 **PRE-ORDER IS NOW LIVE / BACK IN STOCK!** 🚨\nGrab your set now: https://p-bandai.com/tw/item/A2866729001"
            }
            requests.post(WEBHOOK_URL, json=payload)
            print("In stock! Alert sent to Discord.")
            break
        else:
            print(f"[{i+1}/5] Out of stock. Waiting 60s...")

    except Exception as e:
        print(f"Error checking stock: {e}")

    # Wait 60 seconds before checking again (skips delay on 5th check)
    if i < 4:
        time.sleep(60)
