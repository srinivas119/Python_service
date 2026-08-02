from fetchers.codeforces_fetcher import fetch_codeforces
from config.database import get_connection


def update_codeforces(user_id, username):

    data = fetch_codeforces(username)

    if data is None:

        print("Codeforces User Not Found")

        return

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        """
        INSERT INTO coding_profiles(

            user_id,

            codeforces_rating,

            codeforces_max_rating,

            codeforces_rank,

            codeforces_total,

            codeforces_contests,

            updated_at

        )

        VALUES(

            %s,%s,%s,%s,%s,%s,NOW()

        )

        ON CONFLICT(user_id)

        DO UPDATE SET

            codeforces_rating=EXCLUDED.codeforces_rating,

            codeforces_max_rating=EXCLUDED.codeforces_max_rating,

            codeforces_rank=EXCLUDED.codeforces_rank,

            codeforces_total=EXCLUDED.codeforces_total,

            codeforces_contests=EXCLUDED.codeforces_contests,

            updated_at=NOW()

        """,

        (

            user_id,

            data["rating"],

            data["max_rating"],

            data["rank"],

            data["total"],

            data["contests"]

        )

    )

    conn.commit()

    cur.close()

    conn.close()

    print(username, "Codeforces Updated")