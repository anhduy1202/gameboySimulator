from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
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


class WebcamMode(QWidget):
    def __init__(self, MainWindow):
        QWidget.__init__(self)
        self.originalWebcam = MainWindow.originalWebcam
        MainWindow.startBtn.clicked.connect(self.startVideo)

    def startVideo(self):
        self.thread = VideoThread()
        self.thread.changePixmapSignal.connect(self.updateFrame)
        self.thread.start()

    def updateFrame(self, img):
        qtImg = self.convertToQt(img)
        self.originalWebcam.setPixmap(qtImg)

    def convertToQt(self, cvImg):
        """Convert from an opencv image to QPixmap"""
        rgbImage = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)
        flippedImage = cv2.flip(rgbImage, 1)
        h, w, ch = flippedImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(
            flippedImage.data, w, h, bytesPerLine, QImage.Format_RGB888
        )
        p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
