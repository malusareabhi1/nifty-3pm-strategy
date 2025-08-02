import requests

def send_telegram(message):
    token = "your_telegram_bot_token"
    chat_id = "@your_channel_name"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        requests.get(url, params=payload)
        print("📩 Telegram alert sent.")
    except Exception as e:
        print(f"❌ Telegram error: {e}")
