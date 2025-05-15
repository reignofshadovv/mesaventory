from PyQt5.QtWidgets import QComboBox, QCompleter
from PyQt5.QtCore import QStringListModel
from utils.urun_liste import urun_listesi_getir

def urun_combobox_ve_completer():
    urunler = urun_listesi_getir()

    combo = QComboBox()
    combo.setEditable(True)
    combo.addItems(urunler)

    completer = QCompleter(urunler)
    completer.setCaseSensitivity(False)
    combo.setCompleter(completer)

    return combo
