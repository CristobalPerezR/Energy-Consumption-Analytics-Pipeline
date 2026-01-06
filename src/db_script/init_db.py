import sqlite3
import os

def init_db(db_name:str):
    db_dir = os.path.join("data", "database")
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, f"{db_name}.db")
    
    conn = None

    try:
        conn = sqlite3.connect(db_path)
        with open("sql/schema.sql") as f:
            schema = f.read()
        conn.executescript(schema)
        conn.commit()
        print(f"Database initialized at {db_path}")
    except Exception as e:
        raise RuntimeError(f"Database initialization error: {e}")
    finally:
        if conn:
            conn.close()