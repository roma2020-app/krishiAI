import sqlite3

conn=sqlite3.connect(
    "database/app.db",
    check_same_thread=False
)

cursor=conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS tickets(

id INTEGER PRIMARY KEY,

farmer TEXT,

problem TEXT,

status TEXT

)

""")

conn.commit()

def create_ticket(
    farmer,
    problem
):
    """
    Create RSK support ticket.
    """

    cursor.execute(

        """

        INSERT INTO tickets(

        farmer,

        problem,

        status

        )

        VALUES(

        ?,

        ?,

        ?

        )

        """,

        (

            farmer,

            problem,

            "Pending"

        )

    )

    conn.commit()

    return{

        "status":"Created"

    }