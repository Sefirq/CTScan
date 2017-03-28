from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QErrorMessage, QVBoxLayout, QTextBrowser, QDialogButtonBox, QPushButton, QDialog, QMessageBox, QDesktopWidget, QMenuBar, QMainWindow, QAction, qApp, QFileDialog, QLabel, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QRect, Qt
from PyQt5 import QtCore
import math
from matplotlib import pyplot as plt
import numpy as np  # np.append(some_array, column, axis=1) appends a column to array

from logic import SinogramLogic

class SinogramDialog(QDialog):
    def __init__(self, image, alpha, detectors, width, parent=None):
        super(SinogramDialog, self).__init__(parent)
        self.image = image
        self.alpha = float(alpha)
        self.detectors = int(detectors)
        self.width = int(width)
        self.sinogram = np.zeros((1, self.detectors))
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

    def plotEmitersAndDecoders(self, x, y, iks, igrek, detectors_x_list, detectors_y_list):
        plt.scatter(iks, igrek, color="red")
        plt.scatter(detectors_x_list, detectors_y_list, color="blue")
        circle = plt.Circle([x / 2, y / 2], radius=x / 2, fill=False, color='green')
        for (x2, y2) in zip(detectors_x_list, detectors_y_list):
            plt.plot([iks, x2], [igrek, y2], color='gray', linestyle='dashed', linewidth=2)
        ax = plt.gca()
        ax.set_xlim(-1, x + 1)
        ax.set_ylim(-1, y + 1)
        ax.imshow(self.image, cmap='gray')
        ax.add_artist(circle)
        # plt.show()
        plt.savefig('wiz.png')

    def computeSinogram(self, progress):
        sinogram = SinogramLogic(self.image, self.alpha, self.detectors, self.width)
        sg, invsg = sinogram.image_processing(self.image, self.alpha, progress, self.detectors, self.width)


