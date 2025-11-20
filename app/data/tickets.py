"""
Ticket CRUD operations
This module provides create, read, update, delete functions for the 'tickets' table.
Assumes the following schema exists:

CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'open',
    priority TEXT DEFAULT 'medium',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

import sqlite3
from app.data.db import connect_database


def create_ticket(title, description, status="open", priority="medium"):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO tickets (title, description, status, priority)
        VALUES (?, ?, ?, ?)
        """,
        (title, description, status, priority)
    )
    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()
    return ticket_id


def get_all_tickets():
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_ticket_by_id(ticket_id):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def update_ticket(ticket_id, title=None, description=None, status=None, priority=None):
    conn = connect_database()
    cursor = conn.cursor()

    # Build dynamic updates
    fields = []
    values = []

    if title is not None:
        fields.append("title = ?")
        values.append(title)
    if description is not None:
        fields.append("description = ?")
        values.append(description)
    if status is not None:
        fields.append("status = ?")
        values.append(status)
    if priority is not None:
        fields.append("priority = ?")
        values.append(priority)

    # Nothing to update
    if not fields:
        conn.close()
        return False

    values.append(ticket_id)
    query = f"UPDATE tickets SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(query, tuple(values))
    conn.commit()
    conn.close()
    return True


def delete_ticket(ticket_id):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
    conn.commit()
    conn.close()
    return True