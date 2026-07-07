import sqlite3

conn = sqlite3.connect("database/app.db",check_same_thread=False)

cursor=conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS farmers(
id INTEGER PRIMARY KEY,
user_id TEXT,
village TEXT,
crop TEXT,
soil TEXT
)
""")

conn.commit()


def save_farmer(user_id,village,crop,soil):

    cursor.execute(
    """
    INSERT INTO farmers(user_id,village,crop,soil)
    VALUES(?,?,?,?)
    """,
    (user_id,village,crop,soil)
    )

    conn.commit()

    return "Saved"


def get_farmer(user_id):

    cursor.execute(
    """
    SELECT village,crop,soil
    FROM farmers
    WHERE user_id=?
    ORDER BY id DESC
    LIMIT 1
    """,
    (user_id,)
    )

    return cursor.fetchone()