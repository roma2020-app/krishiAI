import sqlite3
import tempfile
import os
from datetime import datetime

DB_PATH = os.path.join(tempfile.gettempdir(), "app.db")

conn = sqlite3.connect(
    DB_PATH,
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
