from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog, QMainWindow
from PyQt6.QtGui import QIcon
from PyQt6 import uic
import sys
import os

class File_dialog(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("untitled.ui", self)
        self.ui = uic.loadUi("untitled.ui", self)

        left_arrow = self.ui.left_arrow
        left_arrow.setStyleSheet("background-color: ; border: none;")
        left_arrow.setIcon(QIcon("left-arrow.png"))


        print(left_arrow)

        # self.ui.open.clicked.connect(self.showFile)

        self.show()

    # def openFile(self):
    #     filename, ok = QFileDialog.getOpenFileName(self, "Wybierz plik", "", "Images (*.png *.jpg *.jpeg)")
    #     if filename:
    #         path = os.path.abspath(filename)
    #         self.ui.lineEdit.setText(path)

    # def showFile(self):
    #     path = self.ui.lineEdit.text()
    #     flags = os.O_RDWR | os.O_CREAT
    #     mode = 0o666
    #     if path != "":
    #         os.open(path, flags, mode)

    # def zaloguj(self):
    #     login = self.ui.login.text()
    #     password = self.ui.password.text()
    #     if login == "admin" and password == "admin":
    #         print("Zalogowano")
    #     else:
    #         print("Błędny login lub hasło")

app=QApplication(sys.argv)
file_dialog=File_dialog()
sys.exit(app.exec())