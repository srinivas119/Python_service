import requests


def fetch_codeforces(username):
    url = f"https://codeforces.com/api/user.info?handles={username}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    result = response.json()

    if result["status"] != "OK":
        return None

    user = result["result"][0]

    # Fetch user submissions to calculate total unique problems solved and contests
    status_url = f"https://codeforces.com/api/user.status?handle={username}"
    status_response = requests.get(status_url)

    solved = set()
    contests = set()

    if status_response.status_code == 200:
        submissions = status_response.json()["result"]

        for sub in submissions:
            if sub.get("verdict") == "OK":
                problem = sub.get("problem", {})
                contest_id = problem.get("contestId")
                index = problem.get("index")

                if contest_id and index:
                    solved.add(f"{contest_id}-{index}")

            if "contestId" in sub:
                contests.add(sub["contestId"])

    return {
        "total": len(solved),
        "rating": user.get("rating", 0),
        "max_rating": user.get("maxRating", 0),
        "rank": user.get("rank", "Unrated"),
        "contests": len(contests),
    }
