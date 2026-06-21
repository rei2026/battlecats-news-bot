import requests
from bs4 import BeautifulSoup
import os

import os

WEBHOOK_URL = os.environ["WEBHOOK_URL"]
NEWS_URL = "https://battlecats.club/news/"
LAST_URL_FILE = "last_url.txt"

response = requests.get(NEWS_URL)
soup = BeautifulSoup(response.text, "html.parser")

latest_title = None
latest_url = None

for link in soup.find_all("a", href=True):
    title = link.get_text(strip=True)
    href = link["href"]

    if not title:
        continue

    if "20" not in title:
        continue

    if href.startswith("/"):
        href = "https://battlecats.club" + href

    latest_title = title
    latest_url = href
    break

if latest_url is None:
    print("ニュースが見つかりません")
    exit()

last_url = ""

if os.path.exists(LAST_URL_FILE):
    with open(LAST_URL_FILE, "r", encoding="utf-8") as f:
        last_url = f.read().strip()

if latest_url == last_url:
    print("新しいニュースなし")
else:
    message = {
        "content": f"🐱 にゃんこ大戦争ニュース\n\n{latest_title}\n{latest_url}"
    }

    requests.post(WEBHOOK_URL, json=message)

    with open(LAST_URL_FILE, "w", encoding="utf-8") as f:
        f.write(latest_url)

    print("新しいニュースを投稿しました")