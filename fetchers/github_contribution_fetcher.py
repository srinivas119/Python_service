import requests
from bs4 import BeautifulSoup


def fetch_contributions(username):

    url = f"https://github.com/{username}"

    response = requests.get(url)

    if response.status_code != 200:
        return {

            "contributions": 0,

            "streak": 0

        }

    soup = BeautifulSoup(response.text, "html.parser")

    contributions = 0

    try:

        text = soup.find(
            "h2",
            class_="f4 text-normal mb-2"
        ).text

        contributions = int(

            text.strip().split()[0].replace(",", "")

        )

    except:

        contributions = 0

    return {

        "contributions": contributions,

        "streak": 0

    }