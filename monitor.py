import os
import time
from bs4 import BeautifulSoup
from curl_cffi import requests

PRODUCT_URL = "https://p-bandai.com/tw/item/A2866729001"
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
}

if not WEBHOOK_URL:
    print("Error: DISCORD_WEBHOOK_URL environment variable is missing.")
    exit(1)

for i in range(5):
    try:
        response = requests.get(
            PRODUCT_URL, 
            headers=headers, 
            impersonate="chrome", 
            timeout=15
        )
        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text()

        if response.status_code != 200 or "Access Denied" in page_text:
            print(f"[{i+1}/5] Page blocked or access issue (Status {response.status_code}).")

        elif "開始預購" in page_text or "加入購物車" in page_text:
            payload = {
                "content": "@everyone 🚨 **PRE-ORDER IS NOW LIVE / BACK IN STOCK!** 🚨\nhttps://p-bandai.com/tw/item/A2866729001"
            }
            requests.post(WEBHOOK_URL, json=payload, impersonate="chrome")
            print(f"[{i+1}/5] In stock! Alert sent to Discord.")
            break

        else:
            print(f"[{i+1}/5] Out of stock. Waiting 60s...")

    except Exception as e:
        print(f"[{i+1}/5] Error checking stock: {e}")

    if i < 4:
        time.sleep(60)
