import re
from bs4 import BeautifulSoup
import requests


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

    # Total Problems Solved - Extracting from CodeChef problem solved section containers
    # CodeChef usually holds solved counts inside section containers or specific header markup
    solved_container = soup.find(
        "section", class_="rating-data-section problems-solved"
    )
    if solved_container:
      # Find total problems or sum up counts if headers are visible
      total_match = re.search(
          r"Total Problems Solved[:\s]*(\d+)", solved_container.text
      )
      if total_match:
        solved = int(total_match.group(1))
      else:
        # Fallback: search all numbers next to fully solved categories
        numbers = re.findall(r"\((\d+)\)", solved_container.text)
        if numbers:
          solved = sum(int(n) for n in numbers)

    # Fallback global text search if specific container layout varies
    if solved == 0:
      page_text = soup.get_text(" ", strip=True)
      match = re.search(
          r"(?:Total Problems Solved|Fully Solved)\s*[:]?\s*(\d+)",
          page_text,
          re.IGNORECASE,
      )
      if match:
        solved = int(match.group(1))

    return {
        "rating": rating,
        "highest_rating": highest,
        "stars": stars,
        "total": solved,
        "easy": solved,  # Fallback allocation so UI progress bars render correctly
        "medium": 0,
        "hard": 0,
    }

  except Exception as e:
    print("❌ CodeChef Error:", e)
    return None
