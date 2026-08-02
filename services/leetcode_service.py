from fetchers.leetcode_fetcher import fetch_leetcode

from config.database import get_connection


def update_leetcode(user_id, username):

    data = fetch_leetcode(username)

    if data is None:

        print("LeetCode User Not Found")

        return

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        """
        INSERT INTO coding_profiles(

            user_id,

            total_solved,

            leetcode_solved,

            leetcode_easy,

            leetcode_medium,

            leetcode_hard,

            leetcode_rating,

            leetcode_ranking,

            leetcode_contests,

            leetcode_acceptance,

            leetcode_streak,

            updated_at

        )

        VALUES(

            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW()

        )

        ON CONFLICT(user_id)

        DO UPDATE SET

            total_solved=EXCLUDED.total_solved,

            leetcode_solved=EXCLUDED.leetcode_solved,

            leetcode_easy=EXCLUDED.leetcode_easy,

            leetcode_medium=EXCLUDED.leetcode_medium,

            leetcode_hard=EXCLUDED.leetcode_hard,

            leetcode_rating=EXCLUDED.leetcode_rating,

            leetcode_ranking=EXCLUDED.leetcode_ranking,

            leetcode_contests=EXCLUDED.leetcode_contests,

            leetcode_acceptance=EXCLUDED.leetcode_acceptance,

            leetcode_streak=EXCLUDED.leetcode_streak,

            updated_at=NOW()

        """,

        (

            user_id,

            data["total"],

            data["total"],

            data["easy"],

            data["medium"],

            data["hard"],

            data["rating"],

            data["ranking"],

            data["contests"],

            data["acceptance"],

            data["streak"]

        )

    )

    conn.commit()

    cur.close()

    conn.close()

    print(username, "LeetCode Updated")