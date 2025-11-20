import sqlite3
from pathlib import Path

# Location of your SQLite database
DB_PATH = Path("DATA") / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    """
    Connect to the SQLite database.
    Automatically creates the database file and folder if needed.

    Args:
        db_path: Path to the SQLite database file.

    Returns:
        sqlite3.Connection: Database connection object.
    """

    # Ensure the DATA/ directory exists
    db_path.parent.mkdir(exist_ok=True)

    # Connect to DB
    conn = sqlite3.connect(str(db_path))

    # Enable foreign keys (SQLite does NOT enable them by default)
    conn.execute("PRAGMA foreign_keys = ON;")

    return conn
