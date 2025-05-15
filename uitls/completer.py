from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import QStringListModel
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db import connect

def urun_ad_completer():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT ad FROM urunler")
    urunler = [row[0] for row in cur.fetchall()]
    conn.close()

    model = QStringListModel()
    model.setStringList(urunler)

    completer = QCompleter()
    completer.setModel(model)
    completer.setCaseSensitivity(False)
    return completer
