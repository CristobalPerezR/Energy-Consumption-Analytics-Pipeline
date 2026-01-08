import sqlite3
from typing import Optional
import pandas as pd
import os

DB_DIR = os.path.join("data", "database")
DB_PATH = os.path.join(DB_DIR, "household_power.db")

def get_connection(db_path:str = DB_PATH) -> sqlite3.Connection:
    return sqlite3.connect(db_path)

def execute_script(conn: sqlite3.Connection, script_path: str):
    with open(script_path) as f:
        script = f.read()
    conn.executescript(script)

def fetch_query(conn: sqlite3.Connection, query:str):
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

def insert_dataframe(conn: sqlite3.Connection, df:pd.DataFrame, table_name:str):
    df.to_sql(table_name, conn, if_exists="append", index=False)
    