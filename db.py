import sqlite3
from datetime import datetime

DB_PATH = 'database/envanter.db'

def connect():
    return sqlite3.connect(DB_PATH)

def initialize_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS urunler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ad TEXT NOT NULL,
        birim TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS stok_giris (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        urun_id INTEGER,
        miktar REAL,
        birim_fiyat REAL,
        tarih TEXT DEFAULT CURRENT_TIMESTAMP,
        kalan_miktar REAL,
        FOREIGN KEY (urun_id) REFERENCES urunler(id)
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS stok_cikis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        urun_id INTEGER,
        miktar REAL,
        tarih TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (urun_id) REFERENCES urunler(id)
    )
    """)

    conn.commit()
    conn.close()
