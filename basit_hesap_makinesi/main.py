import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI dosyamızı okuyup bu pencereye (self) giydiriyoruz
        uic.loadUi("calculator_app.ui", self)

        self.topla_butonu.clicked.connect(self.Topla)
        self.cikar_butonu.clicked.connect(self.Cikar)       
        self.carp_butonu.clicked.connect(self.Carp)
        self.bol_butonu.clicked.connect(self.Bol)

    def Topla(self):
        sayi1 = int(self.sayi1_input.text())
        sayi2 = int(self.sayi2_input.text())
        sonuc = sayi1 + sayi2
        self.sonuc_label.setText(f"Sonuç: {sonuc}")

    def Cikar(self):
        sayi1 = int(self.sayi1_input.text())
        sayi2 = int(self.sayi2_input.text())
        sonuc = sayi1 - sayi2
        self.sonuc_label.setText(f"Sonuç: {sonuc}")
    
    def Carp(self):
        sayi1 = int(self.sayi1_input.text())
        sayi2 = int(self.sayi2_input.text())
        sonuc = sayi1 * sayi2
        self.sonuc_label.setText(f"Sonuç: {sonuc}")
    
    def Bol(self):
        sayi1 = int(self.sayi1_input.text())
        sayi2 = int(self.sayi2_input.text())
        if sayi2 == 0:
            self.sonuc_label.setText("Sıfıra bölme hatası!")
        else:
            sonuc = sayi1 / sayi2
            self.sonuc_label.setText(f"Sonuç: {sonuc}")

              

app = QApplication(sys.argv)
window = MainApp()
window.show()
sys.exit(app.exec())