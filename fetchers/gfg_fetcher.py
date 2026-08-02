import requests
from bs4 import BeautifulSoup


def fetch_gfg(username):

    url = f"https://auth.geeksforgeeks.org/user/{username}"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    score = 0

    try:

        score = int(

            soup.find(
                "div",
                class_="score_card_value"
            ).text.strip()

        )

    except:

        score = 0

    return {

        "score": score

    }