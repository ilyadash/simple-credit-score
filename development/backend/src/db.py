# =============================
# src/db.py
# =============================
# Minimal, explicit SQLite access layer using sqlite3.
# Suitable for a single-instance FastAPI service.

import os
import sqlite3
import pandas as pd
from contextlib import contextmanager

DB_PATH = os.getenv("DATABASE_PATH", "/data/credit.db")

def init_db() -> None:
    """Create tables if they do not exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS credit_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_age INTEGER,
                person_income REAL,
                person_home_ownership TEXT,
                person_emp_length REAL,
                loan_intent TEXT,
                loan_grade TEXT,
                loan_amnt REAL,
                loan_int_rate REAL,
                loan_percent_income REAL,
                cb_person_default_on_file TEXT,
                cb_person_cred_hist_length INTEGER,
                pred_class INTEGER,
                default_probability REAL,
                loan_status INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        conn.commit()

@contextmanager
def get_connection():
    """Context-managed SQLite connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

# -----------------------------
# CRUD helpers
# -----------------------------
def insert_credit_record(record: dict) -> int:
    """Insert a new credit record and return its ID."""
    columns = ",".join(record.keys())
    placeholders = ",".join(["?"] * len(record))
    values = list(record.values())

    sql = f"INSERT INTO credit_records ({columns}) VALUES ({placeholders})"

    with get_connection() as conn:
        cur = conn.execute(sql, values)
        return cur.lastrowid

def update_loan_status(record_id: int, loan_status: int) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE credit_records SET loan_status = ? WHERE id = ?",
            (loan_status, record_id),
        )

def update_loan_prediction(record_id: int, loan_status_pred: int, loan_status_pred_prob: float) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE credit_records SET loan_status_pred = ?, loan_status_pred_prob = ? WHERE id = ?",
            (loan_status_pred, loan_status_pred_prob, record_id),
        )

def fetch_credit_record(record_id: int) -> dict | None:
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT * FROM credit_records WHERE id = ?",
            (record_id,),
        )
        row = cur.fetchone()
        return dict(row) if row else None
    
def bulk_insert_credit_records(df: pd.DataFrame) -> None:
    """
    Bulk insert credit records in the database using a pandas DataFrame.
    Raises:
        ValueError: If required columns are missing from the DataFrame
    """
    # Verify required columns exist in the DataFrame
    required_columns = [
        'person_age', 'person_income', 'person_home_ownership',
        'person_emp_length', 'loan_intent', 'loan_grade',
        'loan_amnt', 'loan_int_rate', 'loan_status',
        'loan_percent_income', 'cb_person_default_on_file',
        'cb_person_cred_hist_length', 'default_probability',
        'pred_class'
    ]

    missing_columns = set(required_columns) - set(df.columns)
    match_columns = sorted(list(set(required_columns).intersection(set(df.columns))))
    df = df[match_columns]
    df.reindex(sorted(df.columns), axis='columns')

    if missing_columns:
        raise ValueError(f"DataFrame is missing required columns: {missing_columns}")

    # Convert DataFrame to list of dictionaries
    records = df.to_dict('records')

    with get_connection() as conn:
        for record in records:
            columns = ",".join(match_columns)
            placeholders = ",".join(["?"] * len(record))
            values = list(record.values())

            sql = f"INSERT INTO credit_records ({columns}) VALUES ({placeholders})"

            conn.execute(sql, values)
        conn.commit()

