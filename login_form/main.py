import sys
import os
import json
from PyQt6.QtWidgets import *
from PyQt6 import uic
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class LoginForm(QMainWindow):
    def __init__(self):
        super().__init__()
        # .ui dosyasını yüklüyoruz
        uic.loadUi("registration_app.ui", self)

        # 1. Slider değişimini etikete bağlayalım
        self.age_slider.valueChanged.connect(self.update_age)

        # kaydet butonuna tıklanınca save_data fonksiyonunu çalıştır
        self.save_button.clicked.connect(self.save_data)
        
        # sil butonuna tıklanınca delete_data fonksiyonunu çalıştır
        self.delete_button.clicked.connect(self.delete_data)

        # PDF oluştur butonuna tıklanınca export_table_to_pdf_reportlab fonksiyonunu çalıştır
        self.print_button.clicked.connect(self.export_table_to_pdf_reportlab)

        # JSON kaydet butonuna tıklanınca save_table_to_json fonksiyonunu çalıştır. Verileri jsona kaydet
        self.json_save_button.clicked.connect(self.save_table_to_json)

        # JSON yükle butonuna tıklanınca load_table_from_json fonksiyonunu çalıştır. JSONdan verileri tabloya yükle
        self.json_load_button.clicked.connect(self.load_table_from_json)

        # checkboxların ikisi aynı anda seçilmesin
        self.chbox_man.toggled.connect(self.handle_gender_checkbox)
        self.chbox_women.toggled.connect(self.handle_gender_checkbox)


    # Slider değeri değiştiğinde yaşın olduğu labelı güncelleyen fonksiyon
    def update_age(self):
        value = self.age_slider.value()
        self.lbl_age.setText(str(value))



    # Cinsiyet checkboxları birbirini etkilesin, biri seçilince diğeri seçilmesin
    def handle_gender_checkbox(self):

        if self.chbox_man.isChecked():
            self.chbox_women.setChecked(False)

        elif self.chbox_women.isChecked():
            self.chbox_man.setChecked(False)



    # VERİLERİ KAYDETME
    # Verileri tabloya ekleyen fonksiyon
    def save_data(self):

        # Ad ve soyad kontrolü
        name = self.name_input.text()
        name = name.upper() # Adı büyük harfe çeviriyoruz
        self.name_input.setText(name)

        if not name:
            QMessageBox.warning(self, "Uyarı", "Lütfen adınızı giriniz.")
            return
        
      
        surname = self.surname_input.text()
        surname = surname.upper() # Soyadı büyük harfe çeviriyoruz
        self.surname_input.setText(surname)

        if not surname:
            QMessageBox.warning(self, "Uyarı", "Lütfen soyadınızı giriniz.")
            return
        

        

        # Cinsiyet kontrolü
        # Eğer her iki checkbox da seçili değilse kullanıcıyı uyar
        if not self.chbox_man.isChecked() and not self.chbox_women.isChecked():
            QMessageBox.warning(self, "Uyarı", "Lütfen cinsiyetinizi seçiniz.")
            return

        gender = ""

        if self.chbox_man.isChecked():
            gender = "ERKEK"

        elif self.chbox_women.isChecked():
            gender = "KADIN"



        # Adres kontrolü       
        address = self.address_input.toPlainText()
        address = address.upper() # Adresi büyük harfe çeviriyoruz
        self.address_input.setPlainText(address)

        if not address:
            QMessageBox.warning(self, "Uyarı", "Lütfen adresinizi giriniz.")
            return
        

        # Yaş kontrolü
        age = self.age_slider.value()
        if age == 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen yaşınızı seçiniz.")
            return
        



        # Tabloya yeni satır ekleme
        rw_count = self.tableWidget_data.rowCount()
        self.tableWidget_data.insertRow(rw_count)

        
        # Sütunlara verileri yerleştirme
        self.tableWidget_data.setItem(rw_count, 0, QTableWidgetItem(name))
        self.tableWidget_data.setItem(rw_count, 1, QTableWidgetItem(surname))
        self.tableWidget_data.setItem(rw_count, 2, QTableWidgetItem(gender))
        self.tableWidget_data.setItem(rw_count, 3, QTableWidgetItem(address))
        self.tableWidget_data.setItem(rw_count, 4, QTableWidgetItem(str(age)))


        # Formu temizleyelim (Opsiyonel)
        self.name_input.clear()
        self.surname_input.clear()
        self.address_input.clear()
        self.age_slider.setValue(0)
        self.chbox_man.setChecked(False)
        self.chbox_women.setChecked(False)



    # VERİLERİ SİLME
    def delete_data(self):
        selected_row = self.tableWidget_data.currentRow()
    
    # Eğer bir satır seçilmişse (seçilmemişse -1 döner)
        if selected_row != -1:
        # Kullanıcıya onay sorusu sormak iyi bir pratiktir
            confirm = QMessageBox.question(self, "Onay", "Bu kaydı silmek istediğinize emin misiniz?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
            if confirm == QMessageBox.StandardButton.Yes:
                self.tableWidget_data.removeRow(selected_row)

        else:
        # Hiçbir yer seçilmemişse kullanıcıyı uyaralım
            QMessageBox.warning(self, "Hata", "Lütfen silmek istediğiniz satıra tıklayın!")


    # VERİLERİ PDF OLARAK KAYDETME
    def export_table_to_pdf_reportlab(self):
        try:
            pdfmetrics.registerFont(TTFont("TRFont", r"fonts\segoeui.ttf"))
        except:
            QMessageBox.warning(self, "Uyarı", "Hata Font Yüklenemedi. PDF oluşturulamadı.")
            return
        

        # Eğer tablo boşsa kullanıcıyı uyar ve PDF oluşturmayı iptal et
        if self.tableWidget_data.rowCount() == 0:
            QMessageBox.information(self, "Bilgi", "Tablo boş. PDF oluşturulmadı.")
            return


        # PDF kaydetme dialogu açalım
        path, _ = QFileDialog.getSaveFileName(
            self,
            "PDF Kaydet",
            "kayitlar.pdf",
            "PDF Files (*.pdf)"
        )

        # Eğer kullanıcı kaydetme işlemini iptal ettiyse path boş olur, bu durumda PDF oluşturmayı iptal et
        if not path:
            return


        # PDF sayfası (tablo genişse landscape daha iyi)
        doc = SimpleDocTemplate(
            path,
            pagesize=landscape(A4),
            leftMargin=24, rightMargin=24, topMargin=24, bottomMargin=24
        )

       
        styles = getSampleStyleSheet()

        title_style = styles["Title"]
        title_style.fontName = "TRFont"

        body_style = styles["BodyText"]
        body_style.fontName = "TRFont"

        elements = []

        # PDF başlığı ekleyelim
        elements.append(Paragraph("KAYITLAR", styles["Title"]))

        # Başlık ile tablo arasında biraz boşluk olsun
        elements.append(Spacer(1, 12))



        # 1) Başlıkları al
        col_count = self.tableWidget_data.columnCount()
        headers = []
        for c in range(col_count):
            h = self.tableWidget_data.horizontalHeaderItem(c)
            headers.append(h.text() if h else f"Sütun {c+1}")


        # 2) Satırları al
        data = [headers]
        for r in range(self.tableWidget_data.rowCount()):
            row = []
            for c in range(col_count):
                item = self.tableWidget_data.item(r, c)
                row.append(item.text() if item else "")
            data.append(row)


        wrapped = []
        for row in data:
            wrapped.append([Paragraph(str(cell), body_style) for cell in row])
        



        # 4) Tabloyu oluştur
        table = Table(wrapped, repeatRows=1)  # repeatRows: her sayfada başlık tekrarlar
        
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))



        # İsteğe bağlı: zebra satır
        for i in range(1, len(wrapped)):
            if i % 2 == 0:
                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, i), (-1, i), colors.HexColor("#fafafa"))
                ]))

        elements.append(table)

        try:
            doc.build(elements)
            QMessageBox.information(self, "Başarılı", f"PDF oluşturuldu:\n{path}")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"PDF oluşturulamadı:\n{e}")


    # VERİLERİ JSON OLARAK KAYDETME
    def get_json_path(self) -> str:
    # Programın çalıştığı klasöre kaydeder
        return os.path.join(os.getcwd(), "kayitlar.json")


    def save_table_to_json(self):
        path = self.get_json_path()

        if self.tableWidget_data.rowCount() == 0:
            QMessageBox.information(self, "Bilgi", "Tablo boş. JSON kaydedilmedi.")
            return

        # Tablo verilerini alalım
        rows = self.tableWidget_data.rowCount()
        cols = self.tableWidget_data.columnCount()


        # Sütun başlıklarını anahtar olarak kullan
        headers = []
        for c in range(cols):
            h = self.tableWidget_data.horizontalHeaderItem(c)
            headers.append(h.text() if h else f"Sütun {c+1}")


        data = []
        for r in range(rows):
            obj = {}
            for c in range(cols):
                item = self.tableWidget_data.item(r, c)
                obj[headers[c]] = item.text() if item else ""
            data.append(obj)


        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            QMessageBox.information(self, "Başarılı", f"JSON kaydedildi:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"JSON kaydedilemedi:\n{e}")


    # JSON dosyasından tabloya veri yükleme
    def load_table_from_json(self):
        path = self.get_json_path()

        # JSON dosyası yoksa kullanıcıyı uyar ve yükleme işlemini iptal et
        if not os.path.exists(path):
            QMessageBox.warning(self, "Hata", f"JSON dosyası bulunamadı:\n{path}\n\nÖnce 'JSON KAYDET' yapın.")
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"JSON okunamadı:\n{e}")
            return

        # JSON verisi bir liste (array) olmalı, değilse kullanıcıyı uyar ve yükleme işlemini iptal et
        if not isinstance(data, list):
            QMessageBox.warning(self, "Hata", "JSON formatı liste ([]) olmalı.")
            return
        

        # Tabloyu temizle
        self.tableWidget_data.setRowCount(0)

        # JSON'daki her nesneyi tabloya ekleyelim. JSON'daki anahtarlar sütun başlıklarıyla eşleşmeli
        cols = self.tableWidget_data.columnCount()
        headers = []
        for c in range(cols):
            h = self.tableWidget_data.horizontalHeaderItem(c)
            headers.append(h.text() if h else f"Sütun {c+1}")

        for obj in data:
            if not isinstance(obj, dict):
                continue

            r = self.tableWidget_data.rowCount()
            self.tableWidget_data.insertRow(r)

            for c in range(cols):
                key = headers[c]
                val = obj.get(key, "")
                self.tableWidget_data.setItem(r, c, QTableWidgetItem(str(val)))

        QMessageBox.information(self, "Başarılı", "JSON verileri tabloya yüklendi.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginForm()
    window.show()
    sys.exit(app.exec())