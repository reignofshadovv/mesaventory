from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from db import connect
from utils.completer import urun_ad_completer
from utils.combo_completer import urun_combobox_ve_completer

class StokGirisTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Arayüz bileşenleri
        self.ad_input = QLineEdit()
        self.ad_input.setCompleter(urun_ad_completer())
        self.ad_input = urun_combobox_ve_completer()
        self.miktar_input = QLineEdit()
        self.fiyat_input = QLineEdit()
        self.birim_input = QLineEdit()

        kaydet_btn = QPushButton("Stok Girişi Kaydet")
        kaydet_btn.clicked.connect(self.kaydet)

        # Arayüz yerleşimi
        layout = QVBoxLayout()

        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Ürün Adı:"))
        form_layout.addWidget(self.ad_input)

        form_layout.addWidget(QLabel("Birim: (örneğin: kg, adet)"))
        form_layout.addWidget(self.birim_input)

        form_layout.addWidget(QLabel("Miktar:"))
        form_layout.addWidget(self.miktar_input)

        form_layout.addWidget(QLabel("Birim Fiyat:"))
        form_layout.addWidget(self.fiyat_input)

        layout.addLayout(form_layout)
        layout.addWidget(kaydet_btn)

        self.setLayout(layout)

    def kaydet(self):
        ad = self.ad_input.text().strip()
        birim = self.birim_input.text().strip()
        try:
            miktar = float(self.miktar_input.text())
            fiyat = float(self.fiyat_input.text())
        except ValueError:
            QMessageBox.warning(self, "Hata", "Miktar ve fiyat sayısal olmalıdır.")
            return

        if not ad or miktar <= 0 or fiyat <= 0:
            QMessageBox.warning(self, "Hata", "Tüm alanlar doğru şekilde doldurulmalı.")
            return

        conn = connect()
        cur = conn.cursor()

        # Ürün var mı kontrol et, yoksa ekle
        cur.execute("SELECT id FROM urunler WHERE ad = ?", (ad,))
        result = cur.fetchone()
        if result:
            urun_id = result[0]
        else:
            cur.execute("INSERT INTO urunler (ad, birim) VALUES (?, ?)", (ad, birim))
            urun_id = cur.lastrowid

        # Stok girişi kaydı + kalan miktar (FIFO için)
        cur.execute("""
            INSERT INTO stok_giris (urun_id, miktar, birim_fiyat, kalan_miktar)
            VALUES (?, ?, ?, ?)
        """, (urun_id, miktar, fiyat, miktar))

        conn.commit()
        conn.close()

        QMessageBox.information(self, "Başarılı", "Stok girişi kaydedildi.")

        def comboboxu_guncelle(combo):
            from utils.urun_liste import urun_listesi_getir
            urunler = urun_listesi_getir()
            combo.clear()
            combo.addItems(urunler)

            completer = QCompleter(urunler)
            completer.setCaseSensitivity(False)
            combo.setCompleter(completer)

        # Temizle
        self.ad_input.clear()
        self.birim_input.clear()
        self.miktar_input.clear()
        self.fiyat_input.clear()
