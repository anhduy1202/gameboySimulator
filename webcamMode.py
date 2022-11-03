from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import imageProcessing
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
        self.resultWebcam = MainWindow.resultWebcam
        self.hasStarted = False
        self.powerBtn = MainWindow.startBtn
        self.convertBtn = MainWindow.convertWebcamBtn
        self.isConverted = False
        self.powerBtn.clicked.connect(self.startVideo)
        self.convertBtn.clicked.connect(self.convertVideo)

    def startVideo(self):
        if not self.hasStarted:
            self.hasStarted = True
            self.powerBtn.setText("Stop")
            self.thread = VideoThread()
            self.thread.changePixmapSignal.connect(self.updateFrame)
            self.thread.start()
        else:
            self.hasStarted = False
            self.powerBtn.setText("Start")
            self.thread.stop()

    def convertVideo(self):
        print("Clicked")
        """
         The code should somewhat similar to startVideo() but be careful that we don't want to
         use the same self.thread so name it something else perhaps :> and also make sure that 
         when we click stop, both of the video should stop, not just one
         
         The self.isConverted variable acts as a condition to decide when we want to convert our video
         for the run() in VideoThread class ( perhaps pass it as argument to use it ? )
        """
        self.isConverted = True

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
