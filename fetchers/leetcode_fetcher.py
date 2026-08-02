import requests

GRAPHQL_URL = "https://leetcode.com/graphql"


def fetch_leetcode(username):

    query = """
    query getUserProfile($username: String!) {

      matchedUser(username: $username) {

        profile {

          ranking

        }

        submitStats {

          acSubmissionNum {

            difficulty

            count

          }

        }

      }

      userContestRanking(username: $username){

        attendedContestsCount

        rating

      }

    }
    """

    variables = {

        "username": username

    }

    response = requests.post(

        GRAPHQL_URL,

        json={

            "query": query,

            "variables": variables

        }

    )

    if response.status_code != 200:

        return None

    result = response.json()

    if result["data"]["matchedUser"] is None:

        return None

    stats = result["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]

    easy = medium = hard = total = 0

    for item in stats:

        if item["difficulty"] == "All":

            total = item["count"]

        elif item["difficulty"] == "Easy":

            easy = item["count"]

        elif item["difficulty"] == "Medium":

            medium = item["count"]

        elif item["difficulty"] == "Hard":

            hard = item["count"]

    contest = result["data"]["userContestRanking"]

    rating = 0

    contests = 0

    if contest:

        rating = int(contest["rating"])

        contests = contest["attendedContestsCount"]

    return {

        "total": total,

        "easy": easy,

        "medium": medium,

        "hard": hard,

        "rating": rating,

        "ranking":

        result["data"]["matchedUser"]["profile"]["ranking"],

        "contests": contests,

        "acceptance": 0,

        "streak": 0

    }