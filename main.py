import requests
from bs4 import BeautifulSoup
import time

TELEGRAM_BOT_TOKEN = '7337234153:AAGVEJm4c1DAYuNGeyrtU5E3SspHNHNwyOs'
TELEGRAM_CHAT_ID = '1939747032'

KEYWORDS = [
    'متجر', 'موقع', 'برمجة', 'ووردبريس', 'Shopify', 'Laravel', 'مطور',
    'تصميم', 'سلة', 'قالب', 'backend', 'frontend', 'موقع إلكتروني',
    'مواقع', 'web', 'wordpress', 'store', 'موقع ويب'
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

if __name__ == "__main__":
    while True:
        check_khamsat()
        time.sleep(120)  # check every 2 minutes
