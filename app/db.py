import sqlite3
from pathlib import Path
DB_PATH=Path(__file__).resolve().parent.parent/'app.db'
def connect():
    con=sqlite3.connect(DB_PATH); con.row_factory=sqlite3.Row; return con
def init_db():
    with connect() as con:
        con.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, role TEXT NOT NULL DEFAULT "user")')
        con.commit()
