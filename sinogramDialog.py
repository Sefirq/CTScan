from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QErrorMessage, QVBoxLayout, QTextBrowser, QDialogButtonBox, QPushButton, QDialog, QMessageBox, QDesktopWidget, QMenuBar, QMainWindow, QAction, qApp, QFileDialog, QLabel, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QRect, Qt
from PyQt5 import QtCore
import math
from matplotlib import pyplot as plt

class SinogramDialog(QDialog):
    def __init__(self, image, alpha, detectors, width, parent=None):
        super(SinogramDialog, self).__init__(parent)
        self.image = image
        self.alpha = int(alpha)
        self.detectors = int(detectors)
        self.width = int(width)
        self.setWindowTitle("Sinogram")
        self.testButton = QPushButton("Click")
        self.testButton.clicked.connect(self.computeCoordsOfEmiter)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        #self.buttonBox.accepted.connect() <- what will happen on Ok
        self.buttonBox.rejected.connect(self.close) #<- what will happen on Cancel
        self.textBrowser = QTextBrowser(self)
        self.textBrowser.append("This is a QTextBrowser!")
        self.slider = QtWidgets.QSlider(Qt.Horizontal)
        self.slider.setFixedWidth(360)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.slider)
        self.verticalLayout.addWidget(self.testButton)
        self.verticalLayout.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.buttonBox)

    def computeCoordsOfEmiter(self):
        x, y = self.image.shape
        for angle in range(0, 360, self.alpha):
            iksy = list()
            iks = list()
            igreki = list()
            igrek = list()
            emiter_x = x/2 - x/2*math.cos(math.radians(angle))
            emiter_y = y/2 - y/2*math.sin(math.radians(angle))
            iks.append(emiter_x)
            igrek.append(emiter_y)
            print(str(emiter_x) + " " + str(emiter_y) + " dla" + str(angle) + " stopni")
            for detector in range(self.detectors):
                det_x = x / 2 - x / 2 * math.cos(
                    math.radians(angle + 180 - self.width / 2 + detector * self.width / (self.detectors - 1)))
                det_y = y / 2 - y / 2 * math.sin(
                    math.radians(angle + 180 - self.width / 2 + detector * self.width / (self.detectors - 1)))
                iksy.append(det_x)
                igreki.append(det_y)
                print(str(det_x) + " " + str(det_y) + " detektor numer " + str(detector))
            plt.scatter(iks, igrek, color="red")
            plt.scatter(iksy, igreki, color="blue")
            circle = plt.Circle([200, 200], radius=200, fill=False)
            ax = plt.gca()
            ax.set_xlim(-1, 400)
            ax.set_ylim(0, 400)
            ax.add_artist(circle)
            plt.show()
