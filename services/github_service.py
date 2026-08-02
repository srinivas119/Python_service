import json
from fetchers.github_fetcher import fetch_github
from fetchers.github_contribution_fetcher import fetch_contributions

from config.database import get_connection


def update_github(user_id, username):

    github = fetch_github(username)

    contrib = fetch_contributions(username)

    if github is None:

        print("GitHub User Not Found")

        return

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        """
        INSERT INTO coding_profiles
        (

            user_id,

            github_repositories,

            github_followers,

            github_following,

            github_languages,

            github_commits,

            github_contributions,

            github_streak,

            updated_at

        )

        VALUES
        (

            %s,

            %s,

            %s,

            %s,

            %s,

            %s,

            %s,

            %s,

            NOW()

        )

        ON CONFLICT(user_id)

        DO UPDATE SET

        github_repositories=EXCLUDED.github_repositories,

        github_followers=EXCLUDED.github_followers,

        github_following=EXCLUDED.github_following,

        github_languages=EXCLUDED.github_languages,

        github_commits=EXCLUDED.github_commits,

        github_contributions=EXCLUDED.github_contributions,

        github_streak=EXCLUDED.github_streak,

        updated_at=NOW()

        """,

        (

            user_id,

            github["repositories"],

            github["followers"],

            github["following"],

            json.dumps(github["languages"]),

            github["repositories"],

            contrib["contributions"],

            contrib["streak"]

        )

    )

    conn.commit()

    cur.close()

    conn.close()

    print(username, "GitHub Updated")