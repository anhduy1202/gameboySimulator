import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import imutils
from windowpy import Ui_MainWindow
from PyQt5.QtCore import *
import cv2

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("window.ui",self)
        self.browseBtn = self.findChild(QPushButton, "browse_pushButton")
        self.convertBtn = self.findChild(QPushButton, "convert_pushButton")
        self.originalImg = self.findChild(QLabel, "original_image")
        self.resultImg = self.findChild(QLabel, "result_image")
        # Browse image
        self.browseBtn.clicked.connect(self.browseImage)
        # Convert image
        self.convertBtn.clicked.connect(self.convertImage)

    def browseImage(self):
        self.file = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        self.image = cv2.imread(self.file)
        self.setOriginal(self.image)

    def convertImage(self):
        image = imutils.resize(self.originalImage, width=640)
        print(image)
        grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        self.displayImage(grayscale, self.resultImg, QImage.Format_Grayscale8)

    def setOriginal(self, image):
        self.originalImage = image
        image = imutils.resize(image, width=640)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.displayImage(frame, self.originalImg, QImage.Format_RGB888)

    def displayImage(self, frame, destination, imgFormat):
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], imgFormat)
        destination.setPixmap(QPixmap.fromImage(image))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())