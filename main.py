import sys
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import imutils
import imageProcessing
from PyQt5.QtCore import *
import cv2

class VideoThread(QThread):
    changePixmapSignal = pyqtSignal(np.ndarray)
    def __init__(self):
        super().__init__()
        self.runFlag = True

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self.runFlag:
            ret, cvImg = cap.read()
            if ret:
                self.changePixmapSignal.emit(cvImg)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self.runFlag = False
        self.wait()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("window.ui", self)
        self.tabWidget = self.findChild(QTabWidget, "tabWidget")
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
        self.originalWebcam = self.findChild(QLabel, "original_webcam")
        self.resultWebcam = self.findChild(QLabel, "result_webcam")
        self.startBtn = self.findChild(QPushButton, "startwebcam_pushButton")
        self.startBtn.clicked.connect(self.startVideo)

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

    def convertImage(self):
        if self.isBrowsed:
            image = imutils.resize(self.originalImage, width=640)
            self.result = imageProcessing.toGameBoyImage(image)
            self.displayImage(self.result, self.resultImg, QImage.Format_Grayscale8)
        else:
            self.isBrowsed = False
            self.convertBtn.setChecked(False)
            print("No image to convert")

    def setOriginal(self, image):
        self.originalImage = image
        image = imutils.resize(image, width=640)
        frame = imageProcessing.toRGB(image)
        self.displayImage(frame, self.originalImg, QImage.Format_RGB888)

    def displayImage(self, frame, destination, imgFormat):
        image = QImage(
            frame, frame.shape[1], frame.shape[0], frame.strides[0], imgFormat
        )
        destination.setPixmap(QPixmap.fromImage(image))


    def startVideo(self):
        print("cliicked")
        self.thread = VideoThread()
        self.thread.changePixmapSignal.connect(self.updateFrame)
        self.thread.start()

    def updateFrame(self, img):
        qtImg = self.convertToQt(img)
        self.originalWebcam.setPixmap(qtImg)

    def convertToQt(self, cvImg):
        """Convert from an opencv image to QPixmap"""
        rgbImage = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)
        flippedImage = cv2.flip(rgbImage,1)
        h, w, ch = flippedImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(flippedImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
