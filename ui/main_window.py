from PyQt5.QtWidgets import QApplication, QTabWidget, QWidget, QVBoxLayout
from ui.stok_giris_tab import StokGirisTab
from ui.stok_cikis_tab import StokCikisTab
from ui.stok_ozet_tab import StokOzetTab

class MainWindow(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FIFO Envanter Takibi")

        self.stokGirisTab = StokGirisTab()
        self.stokCikisTab = StokCikisTab()
        self.stokOzetTab = StokOzetTab()

        self.addTab(self.stokGirisTab, "Stok Girişi")
        self.addTab(self.stokCikisTab, "Stok Çıkışı")
        self.addTab(self.stokOzetTab, "Stok Özeti")
