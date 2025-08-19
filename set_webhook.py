# trigger telegram webhook
import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")
railway_url = "https://82cacbc9845c.ngrok-free.app"

url = f"https://api.telegram.org/bot{token}/setWebhook?url={railway_url}/telegram"
resp = requests.get(url)
print(resp.json())