import bcrypt
import sqlite3
from pathlib import Path

from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table

#  FIX: Define DATA_DIR so migrate_users_from_file works
DATA_DIR = Path("DATA")


def register_user(username, password, role='user'):
    """Register new user with password hashing."""
    # Hash password
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    # Insert into database
    insert_user(username, password_hash, role)
    return True, f"User '{username}' registered successfully."


def login_user(username, password):
    """Authenticate user."""
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."

    # Verify password
    stored_hash = user[2]  # password_hash column
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, "Login successful!"
    return False, "Incorrect password."


def migrate_users_from_file(conn, filepath=DATA_DIR / "users.txt"):
    """
    Migrate users from users.txt to the database.
    Example format of file:
        alice,$2b$12$abcd...
        bob,$2b$12$xyz...
    """
    if not filepath.exists():
        print(f"  File not found: {filepath}")
        print("   No users to migrate.")
        return 0

    cursor = conn.cursor()
    migrated_count = 0

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(',')
            if len(parts) < 2:
                print(f" Invalid line in users.txt: {line}")
                continue

            username = parts[0]
            password_hash = parts[1]

            try:
                cursor.execute(
                    "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                    (username, password_hash, 'user')
                )

                if cursor.rowcount > 0:
                    migrated_count += 1

            except sqlite3.Error as e:
                print(f"Error migrating user {username}: {e}")

    conn.commit()
    print(f" Migrated {migrated_count} users from {filepath.name}")
    return migrated_count
