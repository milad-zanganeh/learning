import json
import sqlite3

from .config import DB_FILE

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT UNIQUE,
                translation TEXT,
                examples TEXT
            )
            """
        )
        conn.commit()

def word_exists(word: str) -> bool:
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT 1 FROM words WHERE word = ?", (word,))
        return c.fetchone() is not None

def insert_word(word: str, translation: str, examples) -> None:
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO words (word, translation, examples) VALUES (?, ?, ?)",
            (word, translation, json.dumps(examples, ensure_ascii=False)),
        )
        conn.commit()

