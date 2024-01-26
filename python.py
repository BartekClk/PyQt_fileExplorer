from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
from PyQt6.QtCore import Qt
import sys
import os

class File_dialog(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("untitled.ui", self)
        self.ui = uic.loadUi("untitled.ui", self)

        self.left_arrow = self.ui.left_arrow
        self.right_arrow = self.ui.right_arrow
        self.label = self.ui.image
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.openFile = self.ui.actionOpen
        self.openFolder = self.ui.actionOpen_folder
        self.images_path = []
        self.actual_image = 0
        self.status_bar = self.ui.statusbar
        self.status_bar.showMessage("Otwórz zdjęcie")

        self.openFile.triggered.connect(lambda: self.open_file())

        self.left_arrow.setEnabled(False)
        self.right_arrow.setEnabled(False)

        self.right_arrow.clicked.connect(lambda: self.scrollRight())
        self.left_arrow.clicked.connect(lambda: self.scrollLeft())

        self.show()

    def open_file(self):
        filename, ok = QFileDialog.getOpenFileName(self, "Wybierz plik", "", "Images (*.png *.jpg *.jpeg *.svg)")
        
        if filename:
            image_path = os.path.abspath(filename)
            folder_path = os.path.dirname(image_path)
            
            self.images_path = []

            for file in os.listdir(folder_path):
                if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".svg"):
                    self.images_path.append(os.path.join(folder_path, file))
            self.load_image(self.images_path[0])
            if len(self.images_path) > 1:
                self.left_arrow.setEnabled(True)
                self.right_arrow.setEnabled(True)
            else:
                self.left_arrow.setEnabled(False)
                self.right_arrow.setEnabled(False)
            self.updateStatusBar()

    def load_image(self, file_path):
        pixmap = QPixmap(file_path)
        pixmap_ratio = pixmap.width()/pixmap.height()
        if pixmap_ratio == 1:
            self.label.setPixmap(pixmap.scaled(self.label.width(), self.label.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        elif pixmap_ratio > 1:
            self.label.setPixmap(pixmap.scaledToWidth(self.label.width(), Qt.TransformationMode.SmoothTransformation))
        else:
            self.label.setPixmap(pixmap.scaledToHeight(self.label.height(), Qt.TransformationMode.SmoothTransformation))

    def scrollRight(self):
        if self.actual_image == len(self.images_path)-1:
            self.actual_image = 0
        else:
            self.actual_image += 1
        self.load_image(self.images_path[self.actual_image])
        self.updateStatusBar()

    def scrollLeft(self):
        if self.actual_image == 0:
            self.actual_image = len(self.images_path)-1
        else:
            self.actual_image -= 1
        self.load_image(self.images_path[self.actual_image])
        self.updateStatusBar()

    def updateStatusBar(self):
        self.status_bar.showMessage("Zdjęcie "+str(self.actual_image+1)+"/"+str(len(self.images_path))+"   "+os.path.basename(self.images_path[self.actual_image]))

app=QApplication(sys.argv)
file_dialog=File_dialog()
sys.exit(app.exec())