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
        gfg_total,
        gfg_easy,
        gfg_medium,
        gfg_hard,
        gfg_institute_rank,
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
        NOW()
    )
    ON CONFLICT (user_id)
    DO UPDATE SET
        gfg_score = EXCLUDED.gfg_score,
        gfg_total = EXCLUDED.gfg_total,
        gfg_easy = EXCLUDED.gfg_easy,
        gfg_medium = EXCLUDED.gfg_medium,
        gfg_hard = EXCLUDED.gfg_hard,
        gfg_institute_rank = EXCLUDED.gfg_institute_rank,
        updated_at = NOW()
    """,
    (
        user_id,
        data["score"],
        data["total"],
        data["easy"],
        data["medium"],
        data["hard"],
        data.get("institute_rank", 0),
    ),
)

    )

    conn.commit()

    cur.close()

    conn.close()

    print(username, "GFG Updated")
