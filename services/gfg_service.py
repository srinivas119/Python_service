from fetchers.gfg_fetcher import fetch_gfg
from config.database import get_connection


def update_gfg(user_id, username):

    data = fetch_gfg(username)

    if data is None:

        print("GFG User Not Found")

        return

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        """
        INSERT INTO coding_profiles
        (

            user_id,

            gfg_score,

            updated_at

        )

        VALUES
        (

            %s,

            %s,

            NOW()

        )

        ON CONFLICT(user_id)

        DO UPDATE SET

            gfg_score=EXCLUDED.gfg_score,

            updated_at=NOW()

        """,

        (

            user_id,

            data["score"]

        )

    )

    conn.commit()

    cur.close()

    conn.close()

    print(username, "GFG Updated")