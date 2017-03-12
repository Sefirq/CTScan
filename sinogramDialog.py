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
        self.testButton.clicked.connect(self.computeSinogram)
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

    def computeSinogram(self):
        x, y = self.image.shape
        for angle in range(0, 360, self.alpha):
            detectors_x_list = list()
            detectors_y_list = list()
            emiter_x = x/2 - x/2*math.cos(math.radians(angle))
            emiter_y = y/2 - y/2*math.sin(math.radians(angle))
            iks = emiter_x
            igrek = emiter_y
            print(str(emiter_x) + " " + str(emiter_y) + " dla" + str(angle) + " stopni")
            for detector in range(self.detectors):
                det_x = x / 2 - x / 2 * math.cos(
                    math.radians(angle + 180 - self.width / 2 + detector * self.width / (self.detectors - 1)))
                det_y = y / 2 - y / 2 * math.sin(
                    math.radians(angle + 180 - self.width / 2 + detector * self.width / (self.detectors - 1)))
                detectors_x_list.append(det_x)
                detectors_y_list.append(det_y)
                print(str(det_x) + " " + str(det_y) + " detektor numer " + str(detector))
            plt.scatter(iks, igrek, color="red")
            plt.scatter(detectors_x_list, detectors_y_list, color="blue")
            circle = plt.Circle([x/2, y/2], radius=x/2, fill=False, color='green')
            for (x2, y2) in zip(detectors_x_list, detectors_y_list):
                plt.plot([iks, x2], [igrek, y2], color='gray', linestyle='dashed', linewidth=2)
            ax = plt.gca()
            ax.set_xlim(-1, x+1)
            ax.set_ylim(-1, y+1)
            ax.imshow(self.image, cmap='gray')
            ax.add_artist(circle)
            plt.show()
