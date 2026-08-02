import requests
from bs4 import BeautifulSoup


def fetch_gfg(username):
    url = f"https://www.geeksforgeeks.org/profile/{username}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)

        print("Status:", response.status_code)
        print("URL:", response.url)

        if response.status_code != 200:
            return None

        # Save HTML for debugging
        with open("gfg.html", "w", encoding="utf-8") as f:
            f.write(response.text)

        soup = BeautifulSoup(response.text, "html.parser")

        print(soup.title)

        return {
            "score": 0
        }

    except Exception as e:
        print("GFG Error:", e)
        return None
