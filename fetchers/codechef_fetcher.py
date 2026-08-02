import requests
from bs4 import BeautifulSoup


def fetch_codechef(username):
    url = f"https://www.codechef.com/users/{username}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)

        print("Status Code:", response.status_code)
        print("Final URL:", response.url)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        rating = 0
        highest = 0
        stars = "N/A"
        solved = 0

        rating_div = soup.find("div", class_="rating-number")
        if rating_div:
            rating = int(rating_div.text.strip())

        highest_small = soup.find("small", class_="rating")
        if highest_small:
            text = highest_small.get_text(" ", strip=True)

            import re

            match = re.search(r"Highest Rating\s*([0-9]+)", text)
            if match:
                highest = int(match.group(1))
            else:
                highest = rating
        else:
            highest = rating

        star_span = soup.find("span", class_="rating")
        if star_span:
            stars = star_span.text.strip()

        h5s = soup.find_all("h5")
        if h5s:
            import re

            nums = re.findall(r"\d+", h5s[0].text)
            if nums:
                solved = int(nums[-1])

        return {
            "rating": rating,
            "highest_rating": highest,
            "stars": stars,
            "total": solved,
        }

    except Exception as e:
        print("CodeChef Error:", e)
        return None
