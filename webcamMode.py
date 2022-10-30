import sys
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import imutils
import imageProcessing
from PyQt5.QtCore import *
import cv2


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebcamWindow()
    window.show()
    sys.exit(app.exec_())
