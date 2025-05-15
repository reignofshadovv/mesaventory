from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db import connect
from utils.completer import urun_ad_completer
from utils.combo_completer import urun_combobox_ve_completer

class StokOzetTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.ad_input = QLineEdit()
        self.ad_input.setCompleter(urun_ad_completer())
        self.ad_input = urun_combobox_ve_completer()
        self.sorgula_btn = QPushButton("Stok Durumunu Göster")
        self.sorgula_btn.clicked.connect(self.stok_ozeti_getir)

        self.stok_label = QLabel("")
        self.maliyet_label = QLabel("")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ürün Adı:"))
        layout.addWidget(self.ad_input)
        layout.addWidget(self.sorgula_btn)
        layout.addWidget(QLabel("Kalan Miktar:"))
        layout.addWidget(self.stok_label)
        layout.addWidget(QLabel("FIFO Ortalama Maliyet:"))
        layout.addWidget(self.maliyet_label)

        self.setLayout(layout)

    def stok_ozeti_getir(self):
        ad = self.ad_input.text().strip()

        if not ad:
            QMessageBox.warning(self, "Hata", "Lütfen ürün adı girin.")
            return

        conn = connect()
        cur = conn.cursor()

        cur.execute("SELECT id FROM urunler WHERE ad = ?", (ad,))
        urun = cur.fetchone()
        if not urun:
            QMessageBox.warning(self, "Hata", "Ürün bulunamadı.")
            self.stok_label.setText("")
            self.maliyet_label.setText("")
            return

        urun_id = urun[0]

        cur.execute("""
            SELECT kalan_miktar, birim_fiyat
            FROM stok_giris
            WHERE urun_id = ? AND kalan_miktar > 0
        """, (urun_id,))
        satirlar = cur.fetchall()
        conn.close()

        if not satirlar:
            self.stok_label.setText("0")
            self.maliyet_label.setText("Stok Yok")
            return

        toplam_miktar = sum([s[0] for s in satirlar])
        toplam_deger = sum([s[0] * s[1] for s in satirlar])
        ort_maliyet = toplam_deger / toplam_miktar if toplam_miktar else 0

        self.stok_label.setText(f"{toplam_miktar:.2f}")
        self.maliyet_label.setText(f"{ort_maliyet:.2f} ₺")
