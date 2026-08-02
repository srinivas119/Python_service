import requests


def fetch_gfg(username):
    url = f"https://www.geeksforgeeks.org/gfg-assets/_next/data/YOUR_BUILD_ID/profile/{username}.json?tab=activity"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            return None

        data = response.json()

        result = data["result"]

        basic = len(result.get("Basic", {}))
        easy = len(result.get("Easy", {}))
        medium = len(result.get("Medium", {}))
        hard = len(result.get("Hard", {}))

        total = data.get("count", basic + easy + medium + hard)

        return {
            "score": total,
            "total": total,
            "easy": easy,
            "medium": medium,
            "hard": hard,
        }

    except Exception as e:
        print("GFG Error:", e)
        return None
