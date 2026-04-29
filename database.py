import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reponses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            age INTEGER NOT NULL,
            genre TEXT NOT NULL,
            niveau_etude TEXT NOT NULL,
            secteur TEXT NOT NULL,
            revenu_mensuel REAL,
            satisfaction INTEGER NOT NULL,
            commentaire TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_reponse(nom, age, genre, niveau_etude, secteur, revenu_mensuel, satisfaction, commentaire):
    conn = get_connection()
    conn.execute("""
        INSERT INTO reponses (nom, age, genre, niveau_etude, secteur, revenu_mensuel, satisfaction, commentaire)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (nom, age, genre, niveau_etude, secteur, revenu_mensuel, satisfaction, commentaire))
    conn.commit()
    conn.close()

def get_all_reponses():
    conn = get_connection()
    df = __import__('pandas').read_sql_query(
        "SELECT * FROM reponses ORDER BY created_at DESC", conn
    )
    conn.close()
    return df

def get_stats():
    conn = get_connection()
    cursor = conn.cursor()

    total = cursor.execute("SELECT COUNT(*) FROM reponses").fetchone()[0]
    age_moy = cursor.execute("SELECT ROUND(AVG(age),1) FROM reponses").fetchone()[0]
    sat_moy = cursor.execute("SELECT ROUND(AVG(satisfaction),2) FROM reponses").fetchone()[0]
    rev_moy = cursor.execute("SELECT ROUND(AVG(revenu_mensuel),0) FROM reponses WHERE revenu_mensuel IS NOT NULL").fetchone()[0]

    genre = __import__('pandas').read_sql_query(
        "SELECT genre, COUNT(*) as count FROM reponses GROUP BY genre", conn)
    secteur = __import__('pandas').read_sql_query(
        "SELECT secteur, COUNT(*) as count FROM reponses GROUP BY secteur ORDER BY count DESC", conn)
    niveau = __import__('pandas').read_sql_query(
        "SELECT niveau_etude, COUNT(*) as count FROM reponses GROUP BY niveau_etude", conn)
    satisfaction = __import__('pandas').read_sql_query(
        "SELECT satisfaction, COUNT(*) as count FROM reponses GROUP BY satisfaction ORDER BY satisfaction", conn)

    conn.close()
    return {
        "total": total,
        "age_moy": age_moy,
        "sat_moy": sat_moy,
        "rev_moy": rev_moy,
        "genre": genre,
        "secteur": secteur,
        "niveau": niveau,
        "satisfaction": satisfaction
    }
