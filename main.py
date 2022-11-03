import math
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import imageProcessing
from webcamMode import WebcamMode
import cv2

SCALED_WIDTH = 640
SCALED_HEIGHT = 480
TARGET_AREA = 64000.0


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("window.ui", self)
        self.tabWidget = self.findChild(QTabWidget, "tabWidget")
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.setTabText(0, "Static Image")
        self.tabWidget.setTabText(1, "Webcam")
        self.isBrowsed = False
        self.browseAction = self.findChild(QAction, "actionBrowse_Image")
        self.saveAsAction = self.findChild(QAction, "actionSave_As")
        self.newStaticImageAction = self.findChild(QAction, "actionStatic_Image")
        self.newLiveVideoAction = self.findChild(QAction, "actionLive_Video")
        self.convertBtn = self.findChild(QPushButton, "convert_pushButton")
        self.saveBtn = self.findChild(QPushButton, "save_pushButton")
        self.clearBtn = self.findChild(QPushButton, "clear_pushButton")
        self.originalImg = self.findChild(QLabel, "original_image")
        self.resultImg = self.findChild(QLabel, "result_image")

        # Webcam
        self.originalWebcam = self.findChild(QLabel, "original_webcam")
        self.resultWebcam = self.findChild(QLabel, "result_webcam")
        self.startBtn = self.findChild(QPushButton, "startwebcam_pushButton")
        self.convertWebcamBtn = self.findChild(QPushButton, "convertwebcam_pushButton")
        self.secondTab = WebcamMode(self)

        # Detect tab change
        self.tabWidget.currentChanged.connect(self.tabChanged)

        # Menu action
        self.browseAction.triggered.connect(self.browseImage)
        self.saveAsAction.triggered.connect(self.saveImage)
        self.newStaticImageAction.triggered.connect(self.insertTab)
        self.newLiveVideoAction.triggered.connect(self.insertTab)

        # Button Event
        self.saveBtn.clicked.connect(self.saveImage)
        self.clearBtn.clicked.connect(self.clearAll)
        tabs = self.tabWidget
        tabs.tabCloseRequested.connect(lambda index: tabs.removeTab(index))

        # Convert image
        self.convertBtn.clicked.connect(self.convertImage)

    def tabChanged(self):
        print("Tab was changed to: ", self.tabWidget.currentIndex())

    def insertTab(self):
        tabName = self.sender()
        self.tabWidget.addTab(QWidget(), tabName.text())

    def browseImage(self):
        self.isBrowsed = True
        self.file = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        if self.file:
            self.image = cv2.imread(self.file)
            self.setOriginal(self.image)
            self.isBrowsed = True
        else:
            self.isBrowsed = False

    def saveImage(self):
        if self.isBrowsed:
            filename = QFileDialog.getSaveFileName(
                filter="JPG(*.jpg);;PNG(*.png);;TIFF(*.tiff);;BMP(*.bmp)"
            )[0]
            if filename:
                cv2.imwrite(filename, self.result)
                print(f"Imaged saved as: {filename}")
            else:
                print("Provide image name")
        else:
            self.isBrowsed = False
            self.saveBtn.setChecked(False)
            print("No image to save")

    def clearAll(self):
        self.image = ""
        self.file = ""
        self.isBrowsed = False
        self.result = ""
        self.convertBtn.setChecked(False)
        self.originalImage = ""
        self.originalImg.clear()
        self.resultImg.clear()

    def resizeImage(self, inputImage):
        ratio = float(inputImage.shape[1]) / float(inputImage.shape[0])
        resizedHeight = int(math.sqrt(TARGET_AREA / ratio) + 0.5)
        resizedWidth = int((resizedHeight * ratio) + 0.5)
        image = cv2.resize(inputImage, (resizedWidth, resizedHeight))
        return image

    def convertImage(self):
        if self.isBrowsed:
            resizedImage = self.resizeImage(self.originalImage)
            self.result = imageProcessing.toGameBoyImage(resizedImage)
            self.displayImage(self.result, self.resultImg, QImage.Format_Grayscale8)
        else:
            self.isBrowsed = False
            self.convertBtn.setChecked(False)
            print("No image to convert")

    def setOriginal(self, image):
        self.originalImage = image
        image = self.resizeImage(self.originalImage)
        frame = imageProcessing.toRGB(image)
        self.displayImage(frame, self.originalImg, QImage.Format_RGB888)

    def displayImage(self, frame, destination, imgFormat):
        image = QImage(
            frame, frame.shape[1], frame.shape[0], frame.strides[0], imgFormat
        )
        destination.setPixmap(QPixmap.fromImage(image))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
