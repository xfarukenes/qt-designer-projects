import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic

class Uygulama(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI dosyamızı okuyup bu pencereye (self) giydiriyoruz
        uic.loadUi("first_app.ui", self)

        self.yazdir_butonu.clicked.connect(self.selam_ver)
        
        
    def selam_ver(self):

        if self.isim_txtbox.text() == "":
            self.isim_label.setText("Lütfen bir isim giriniz.")      

        else:
            isim = self.isim_txtbox.text()
            self.isim_label.setText(f"Merhaba {isim}!")

        

app = QApplication(sys.argv)
pencere = Uygulama()
pencere.show()
sys.exit(app.exec())