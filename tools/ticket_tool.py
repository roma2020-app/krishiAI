import sqlite3
from datetime import datetime

conn = sqlite3.connect(
    "database/app.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer TEXT,
    problem TEXT,
    status TEXT
)
""")

conn.commit()


def create_ticket(farmer, problem):

    cursor.execute(
        """
        INSERT INTO tickets (
            farmer,
            problem,
            status
        )
        VALUES (?, ?, ?)
        """,
        (
            farmer,
            problem,
            "Pending"
        )
    )

    conn.commit()

    ticket_id = cursor.lastrowid

    return {
        "ticket_id": ticket_id,
        "status": "Created",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
