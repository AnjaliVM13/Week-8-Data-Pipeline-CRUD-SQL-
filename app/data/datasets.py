import os
import pandas as pd

def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a database table using pandas.

    Args:
        conn: Database connection
        csv_path: Path to CSV file
        table_name: Name of the target table

    Returns:
        int: Number of rows loaded
    """

    # 1. Check if CSV file exists
    if not os.path.exists(csv_path):
        print(f" CSV not found: {csv_path}")
        return 0

    # 2. Read CSV using pandas
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f" Error reading CSV {csv_path}: {e}")
        return 0

    # If CSV is empty
    if df.empty:
        print(f" CSV is empty: {csv_path}")
        return 0

    # 3. Insert into SQL using to_sql
    try:
        df.to_sql(
            name=table_name,
            con=conn,
            if_exists='append',
            index=False
        )
    except Exception as e:
        print(f" Error inserting into table '{table_name}': {e}")
        return 0

    # 4. Print success message
    print(f" Loaded {len(df)} rows into '{table_name}' from {os.path.basename(csv_path)}")

    return len(df)

def load_all_csv_data(conn):
    """
    Load all CSV datasets into their respective tables.
    Returns the total number of rows inserted.
    """

    DATA_DIR = "DATA"

    csv_mapping = {
        "cyber_incidents": os.path.join(DATA_DIR, "cyber_incidents.csv"),
        "datasets_metadata": os.path.join(DATA_DIR, "datasets_metadata.csv"),
        "it_tickets": os.path.join(DATA_DIR, "it_tickets.csv")
    }

    total_rows = 0

    for table, csv_path in csv_mapping.items():
        print(f"\n Loading CSV: {csv_path} → Table: {table}")
        rows = load_csv_to_table(conn, csv_path, table)
        total_rows += rows

    print(f"\n TOTAL CSV ROWS LOADED: {total_rows}")
    return total_rows

