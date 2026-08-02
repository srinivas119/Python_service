import requests
from config.settings import GITHUB_TOKEN


def fetch_github(username):

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(
        f"https://api.github.com/users/{username}",
        headers=headers
    )

    if response.status_code != 200:
        return None

    profile = response.json()

    repos = requests.get(
        profile["repos_url"],
        headers=headers
    )

    languages = {}

    if repos.status_code == 200:

        for repo in repos.json():

            if repo["language"]:

                languages[repo["language"]] = (
                    languages.get(repo["language"], 0) + 1
                )

    return {

        "repositories": profile["public_repos"],

        "followers": profile["followers"],

        "following": profile["following"],

        "languages": languages,

        "created_at": profile["created_at"]

    }