from fetchers.codechef_fetcher import fetch_codechef
from config.database import get_connection


def update_codechef(user_id, username):

    data = fetch_codechef(username)

    if data is None:

        print("CodeChef User Not Found")

        return

    conn = get_connection()

    cur = conn.cursor()

   cur.execute(
    """
    INSERT INTO coding_profiles
    (
        user_id,
        codechef_rating,
        codechef_highest_rating,
        codechef_stars,
        codechef_total,
        codechef_easy,
        codechef_medium,
        codechef_hard,
        updated_at
    )
    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,NOW()
    )
    ON CONFLICT(user_id)
    DO UPDATE SET
        codechef_rating = EXCLUDED.codechef_rating,
        codechef_highest_rating = EXCLUDED.codechef_highest_rating,
        codechef_stars = EXCLUDED.codechef_stars,
        codechef_total = EXCLUDED.codechef_total,
        codechef_easy = EXCLUDED.codechef_easy,
        codechef_medium = EXCLUDED.codechef_medium,
        codechef_hard = EXCLUDED.codechef_hard,
        updated_at = NOW()
    """,
    (
        user_id,
        data["rating"],
        data["highest_rating"],
        data["stars"],
        data["total"],
        data["easy"],
        data["medium"],
        data["hard"],
    )
)

    conn.commit()

    cur.close()

    conn.close()

    print(username, "CodeChef Updated")
