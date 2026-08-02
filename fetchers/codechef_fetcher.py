import requests
from bs4 import BeautifulSoup
import re


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
        print("First 500 chars:")
        print(response.text[:500])

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        rating = 0
        highest = 0
        stars = "N/A"
        solved = 0

        # Rating
        rating_div = soup.find("div", class_="rating-number")
        if rating_div:
            try:
                rating = int(rating_div.text.strip())
            except:
                pass

        # Highest Rating
        highest_small = soup.find("small", class_="rating")
        if highest_small:
            text = highest_small.get_text(" ", strip=True)
            match = re.search(r"Highest Rating\s*([0-9]+)", text)

            if match:
                highest = int(match.group(1))
            else:
                highest = rating
        else:
            highest = rating

        # Stars
        star_span = soup.find("span", class_="rating")
        if star_span:
            stars = star_span.text.strip()

        # Total Problems Solved
        page_text = soup.get_text(" ", strip=True)

        match = re.search(
            r"Total\s+Problems\s+Solved\s*:\s*(\d+)",
            page_text,
            re.IGNORECASE,
        )

        if match:
            solved = int(match.group(1))
        else:
            print("❌ Could not find 'Total Problems Solved' in HTML")
            solved = 0

        return {
            "rating": rating,
            "highest_rating": highest,
            "stars": stars,
            "total": solved,
        }

    except Exception as e:
        print("❌ CodeChef Error:", e)
        return None
