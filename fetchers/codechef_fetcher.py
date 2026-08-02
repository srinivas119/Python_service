import requests
from bs4 import BeautifulSoup


def fetch_codechef(username):

    url = f"https://www.codechef.com/users/{username}"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    rating = 0
    highest = 0
    stars = "N/A"
    solved = 0

    try:
        rating = int(
            soup.find("div", class_="rating-number").text.strip()
        )
    except:
        pass

    try:
        highest = int(
            soup.find(
                "small",
                class_="rating"
            ).text.split("Highest Rating")[1].strip()
        )
    except:
        highest = rating

    try:
        stars = soup.find(
            "span",
            class_="rating"
        ).text.strip()
    except:
        pass

    try:
        solved = int(
            soup.find_all("h5")[0].text.split()[-1]
        )
    except:
        solved = 0

    return {

        "rating": rating,

        "highest_rating": highest,

        "stars": stars,

        "total": solved

    }