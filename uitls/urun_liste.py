import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db import connect

def urun_listesi_getir():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT ad FROM urunler ORDER BY ad ASC")
    urunler = [row[0] for row in cur.fetchall()]
    conn.close()
    return urunler
