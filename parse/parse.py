from bs4 import BeautifulSoup
import pandas as pd
import re

with open("watch-history.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "lxml")

entries = []

for div in soup.find_all("div", class_="content-cell"):
    link = div.find("a")
    if link and "watch" in link.get("href"):
        title = link.get_text(strip=True)
        url = link.get("href")

        text = div.get_text(" ", strip=True)

        match = re.search(r"[A-Za-z]{3} \d{1,2}, \d{4}, \d{1,2}:\d{2}:\d{2}\s?[AP]M PST", text)
        date_str = match.group(0) if match else None

        cleaned = text.replace("Watched ", "")
        if date_str:
            cleaned = cleaned.replace(date_str, "").strip()

        channel = cleaned.replace(title, "").strip()

        entries.append({
            "title": title,
            "channel": channel,
            "url": url,
            "watched_on": date_str
        })

df = pd.DataFrame(entries)
df.to_csv("youtube_history.csv", index=False)

print(df.head())
