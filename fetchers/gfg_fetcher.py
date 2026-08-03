import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}


def fetch_gfg(username):
    url = "https://practiceapi.geeksforgeeks.org/api/v1/user/problems/submissions/"

    params = {
        "handle": username
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=20,
        )

        print("Status:", response.status_code)
        print("Response:", response.text)

        response.raise_for_status()

        data = response.json()

        print("JSON:", data)

        if data.get("status") != "success":
            return None

        result = data.get("result", {})

        basic = len(result.get("Basic", {}))
        easy = len(result.get("Easy", {}))
        medium = len(result.get("Medium", {}))
        hard = len(result.get("Hard", {}))

        total = data.get("count", basic + easy + medium + hard)

        return {
            "score": total,
            "total": total,
            "basic": basic,
            "easy": easy,
            "medium": medium,
            "hard": hard,
        }

    except Exception as e:
        print("GFG Error:", e)
        return None


if __name__ == "__main__":
    print(fetch_gfg("srinivas119"))
