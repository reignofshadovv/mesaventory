from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sqlite3
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db import connect
from utils.completer import urun_ad_completer
from utils.combo_completer import urun_combobox_ve_completer

class StokCikisTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.ad_input = QLineEdit()
        self.ad_input.setCompleter(urun_ad_completer())
        self.ad_input = urun_combobox_ve_completer()
        self.miktar_input = QLineEdit()
        kaydet_btn = QPushButton("Stoktan Düş (FIFO Satış)")
        kaydet_btn.clicked.connect(self.satis_yap)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ürün Adı:"))
        layout.addWidget(self.ad_input)
        layout.addWidget(QLabel("Satılan Miktar:"))
        layout.addWidget(self.miktar_input)
        layout.addWidget(kaydet_btn)

        self.setLayout(layout)

    def satis_yap(self):
        ad = self.ad_input.text().strip()
        try:
            miktar = float(self.miktar_input.text())
        except ValueError:
            QMessageBox.warning(self, "Hata", "Miktar sayısal olmalı.")
            return

        if not ad or miktar <= 0:
            QMessageBox.warning(self, "Hata", "Tüm alanlar doğru girilmeli.")
            return

        conn = connect()
        cur = conn.cursor()

        # Ürün var mı kontrolü
        cur.execute("SELECT id FROM urunler WHERE ad = ?", (ad,))
        urun = cur.fetchone()
        if not urun:
            QMessageBox.warning(self, "Hata", "Bu ürün bulunamadı.")
            return

        urun_id = urun[0]

        # FIFO: en eski girişten başlayarak kalan stoklardan düş
        cur.execute("""
            SELECT id, kalan_miktar FROM stok_giris
            WHERE urun_id = ? AND kalan_miktar > 0
            ORDER BY tarih ASC
        """, (urun_id,))
        stoklar = cur.fetchall()

        kalan = miktar
        for stok_id, kalan_miktar in stoklar:
            if kalan <= 0:
                break
            dusulecek = min(kalan_miktar, kalan)
            cur.execute("""
                UPDATE stok_giris
                SET kalan_miktar = kalan_miktar - ?
                WHERE id = ?
            """, (dusulecek, stok_id))
            kalan -= dusulecek

        if kalan > 0:
            conn.rollback()
            QMessageBox.warning(self, "Yetersiz Stok", f"Yeterli stok yok. Eksik miktar: {kalan}")
            return

        # Satış kaydı
        cur.execute("""
            INSERT INTO stok_cikis (urun_id, miktar) VALUES (?, ?)
        """, (urun_id, miktar))

        conn.commit()
        conn.close()

        QMessageBox.information(self, "Başarılı", "Stoktan FIFO ile düşüldü.")

        self.ad_input.clear()
        self.miktar_input.clear()
