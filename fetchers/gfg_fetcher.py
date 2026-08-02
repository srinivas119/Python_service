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
            print(response.text[:500])
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        print("TITLE:", soup.title.string if soup.title else "No title")

        return {
            "score": 0
        }

    except Exception as e:
        print("GFG ERROR:", e)
        return None
