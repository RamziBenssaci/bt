import requests
from bs4 import BeautifulSoup
import time
import threading
from flask import Flask
import os

TELEGRAM_BOT_TOKEN = '7337234153:AAGVEJm4c1DAYuNGeyrtU5E3SspHNHNwyOs'
TELEGRAM_CHAT_ID = '1939747032'

KEYWORDS = [
    'متجر', 'موقع', 'برمجة', 'ووردبريس', 'وردبريس', 'Shopify', 'shopify', 'Laravel', 'laravel', 'سلة', 'salla',
    'مطور', 'مطور مواقع', 'تصميم', 'تصميم مواقع', 'تصميم متجر', 'قالب', 'قوالب', 'backend', 'frontend',
    'موقع إلكتروني', 'مواقع', 'web', 'website', 'wordpress', 'woocommerce', 'متجر الكتروني', 'موقع ويب',
    'تكويد', 'ديفلوبر', 'developer', 'web development', 'ecommerce', 'commerce', 'online store', 'landing page',
    'shop', 'متجر اونلاين', 'إنشاء متجر', 'إنشاء موقع', 'برمجة موقع', 'تعريب قالب', 'تعريب',
    'تحسين سرعة', 'سرعة الموقع', 'صيانة موقع', 'صيانة متجر', 'متجر ووردبريس', 'باك اند', 'فرونت اند',
    'next.js', 'nuxt.js', 'react', 'vue', 'blade', 'shopify expert', 'salla expert', 'سلة برو',
    'shopify dropshipping', 'دروبسشيبينغ', 'خدمة برمجة', 'خدمة متجر', 'إنشاء متجر سلة', 'إنشاء متجر Shopify',
    'ربط الدفع', 'وسائل الدفع', 'تهيئة متجر', 'تهيئة موقع', 'خدمة تصميم', 'فريلانسر', 'فري لانس'
]

SEEN_TITLES = set()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram Error:", e)

def check_khamsat():
    print("Checking Khamsat...")
    try:
        response = requests.get("https://khamsat.com/community/requests")
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.select('.media-body')

        for item in items:
            title_tag = item.select_one('h3.media-heading a')
            if not title_tag:
                continue
            title = title_tag.text.strip()
            link = "https://khamsat.com" + title_tag['href']
            
            if title in SEEN_TITLES:
                continue
            
            if any(keyword.lower() in title.lower() for keyword in KEYWORDS):
                SEEN_TITLES.add(title)
                send_telegram_message(f"🔔 طلب جديد:\n{title}\n{link}")
                
    except Exception as e:
        print("Error while checking Khamsat:", e)

# Run bot in separate thread
def start_bot_loop():
    while True:
        check_khamsat()
        time.sleep(120)  # Every 2 minutes

# Minimal Flask app to keep service alive on Render
app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Khamsat bot is running!'

if __name__ == '__main__':
    threading.Thread(target=start_bot_loop).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
