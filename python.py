from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
from PyQt6.QtCore import Qt
import sys
import os
import math

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
        self.pixmap = QPixmap()
        self.pixmap_ratio = 0
        self.label_avg = 0
        self.resized = False

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
        pixmap = self.pixmap
        pixmap.load(file_path)
        pixmap_ratio = pixmap.width()/pixmap.height()
        scale_factor = 0.8

        self.pixmap = pixmap
        self.pixmap_ratio = pixmap_ratio

        self.label_avg = (self.label.width()+self.label.height())/2

        if pixmap_ratio == 1:
            self.label.setPixmap(pixmap.scaled(int(self.label.width()*scale_factor), int(self.label.height()*scale_factor), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        elif pixmap_ratio > 1:
            self.label.setPixmap(pixmap.scaledToWidth(int(self.label.width()*scale_factor), Qt.TransformationMode.SmoothTransformation))
        else:
            self.label.setPixmap(pixmap.scaledToHeight(int(self.label.height()*scale_factor), Qt.TransformationMode.SmoothTransformation))


    def scrollRight(self):
        if self.actual_image == len(self.images_path)-1:
            self.actual_image = 0
        else:
            self.actual_image += 1
        self.load_image(self.images_path[self.actual_image])
        self.updateStatusBar()
    
    def resizeEvent(self, event):
        scale_factor = 0.8
        if abs(self.label_avg - (self.label.width()+self.label.height())/2) > 20 and self.resized == False:
            self.resized = True
            print("resize "+str((self.label.width()+self.label.height())/2))
            self.label_avg = (self.label.width()+self.label.height())/2
            if self.images_path:
                self.pixmap.load(self.images_path[self.actual_image])
            self.resized = False

        if self.images_path:
                
            if self.pixmap_ratio == 1:
                self.label.setPixmap(self.pixmap.scaled(int(self.label.width()*scale_factor), int(self.label.height()*scale_factor), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            elif self.pixmap_ratio > 1:
                self.label.setPixmap(self.pixmap.scaledToWidth(int(self.label.width()*scale_factor)))
            else:
                self.label.setPixmap(self.pixmap.scaledToHeight(int(self.label.height()*scale_factor)))


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