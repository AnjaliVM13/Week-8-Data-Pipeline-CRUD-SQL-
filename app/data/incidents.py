import pandas as pd
from app.data.db import connect_database

def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):
    """
    Insert a new cyber incident into the database.
    
    Args:
        conn: Database connection
        date: Incident date (YYYY-MM-DD)
        incident_type: Type of incident
        severity: Severity level
        status: Current status
        description: Incident description
        reported_by: Username of reporter (optional)
        
    Returns:
        int: ID of the inserted incident
    """
    cursor = conn.cursor()

    query = """
    INSERT INTO cyber_incidents
    (date, incident_type, severity, status, description, reported_by)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    cursor.execute(query, (date, incident_type, severity, status, description, reported_by))
    conn.commit()

    return cursor.lastrowid


def get_all_incidents(conn):
    """
    Retrieve all incidents from the database.

    Returns:
        pandas.DataFrame: All incidents
    """
    query = "SELECT * FROM cyber_incidents"
    df = pd.read_sql_query(query, conn)
    return df


def update_incident_status(conn, incident_id, new_status):
    """
    Update the status of an incident.
    
    Returns:
        int: Number of rows updated
    """
    cursor = conn.cursor()
    query = "UPDATE cyber_incidents SET status = ? WHERE id = ?"

    cursor.execute(query, (new_status, incident_id))
    conn.commit()

    return cursor.rowcount


def delete_incident(conn, incident_id):
    """
    Delete an incident from the database.
    
    Returns:
        int: Number of rows deleted
    """
    cursor = conn.cursor()
    query = "DELETE FROM cyber_incidents WHERE id = ?"

    cursor.execute(query, (incident_id,))
    conn.commit()

    return cursor.rowcount


def get_incidents_by_type_count(conn):
    """
    Count incidents by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df


def get_high_severity_by_status(conn):
    """
    Count high severity incidents by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df


def get_incident_types_with_many_cases(conn, min_count=5):
    """
    Find incident types with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df


# Optional diagnostics (kept for development, not required for production)
if __name__ == "__main__":
    conn = connect_database()

    print("\n Incidents by Type:")
    print(get_incidents_by_type_count(conn))

    print("\n High Severity Incidents by Status:")
    print(get_high_severity_by_status(conn))

    print("\n Incident Types with Many Cases (>5):")
    print(get_incident_types_with_many_cases(conn, min_count=5))

    conn.close()
