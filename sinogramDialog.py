from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QErrorMessage, QVBoxLayout, QTextBrowser, QDialogButtonBox, QPushButton, QDialog, QMessageBox, QDesktopWidget, QMenuBar, QMainWindow, QAction, qApp, QFileDialog, QLabel, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QRect, Qt
from PyQt5 import QtCore
import math
from matplotlib import pyplot as plt
import numpy as np  # np.append(some_array, column, axis=1) appends a column to array

class SinogramDialog(QDialog):
    def __init__(self, image, alpha, detectors, width, parent=None):
        super(SinogramDialog, self).__init__(parent)
        self.image = image
        print(self.image[200][200])
        self.alpha = float(alpha)
        self.detectors = int(detectors)
        self.width = int(width)
        self.sinogram = np.zeros((1, self.detectors))
        print(self.sinogram)
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
        plt.show()

    def computeSinogram(self):
        x, y = self.image.shape
        angle = 0
        #for angle in range(0, 180+self.alpha, self.alpha):
        while angle < 180+self.alpha:
            sums = list()
            detectors_x_list = list()
            detectors_y_list = list()
            emiter_x = x/2 - x/2*math.cos(math.radians(angle))
            emiter_y = y/2 - y/2*math.sin(math.radians(angle))
            #print(str(emiter_x) + " " + str(emiter_y) + " dla " + str(angle) + " stopni")
            for detector in range(self.detectors):
                det_x = x / 2 - x / 2 * math.cos(
                     math.radians(angle + 180 - self.width / 2 + detector * self.width / (self.detectors - 1)))
                det_y = y / 2 - y / 2 * math.sin(
                    math.radians(angle + 180 - self.width / 2 + detector * self.width / (self.detectors - 1)))
                detectors_x_list.append(det_x)
                detectors_y_list.append(det_y)
                print(str(det_x) + " " + str(det_y) + " detektor numer " + str(detector))
                sums.append(self.bresenhamComputeSum(int(emiter_x), int(emiter_y), int(det_x), int(det_y)))
            if angle == 0:
                self.sinogram[0, :] = list(reversed(sums))
            else:
                temp = np.zeros((1, self.detectors))
                temp[0, :] = list(reversed(sums))
                self.sinogram = np.append(self.sinogram, temp, axis=0)
            angle += self.alpha
            self.plotEmitersAndDecoders(x, y, emiter_x, emiter_y, detectors_x_list, detectors_y_list)
        self.sinogram = self.sinogram*1.0/np.max(self.sinogram)*255
        plt.imshow(self.sinogram, cmap="gray")
        ax = plt.gca()
        plt.show()

    def bresenhamComputeSum(self, x_start, y_start, x_end, y_end):
        x = x_start
        y = y_start
        limit = self.image.shape[0] - 1
        if x_start < x_end:
            xi = 1
            dx = x_end - x_start
        else:
            xi = -1
            dx = x_start - x_end
        if y_start < y_end:
            yi = 1
            dy = y_end - y_start
        else:
            yi = -1
            dy = y_start - y_end
        sumOfPixels = int(self.image[min(limit, y)][min(limit, x)])
        if dx > dy:
            ai = (dy - dx) * 2
            bi = dy * 2
            d = bi - dx
            while not x == int(x_end):
                if d >= 0:
                    x += xi
                    y += yi
                    d += ai
                else:
                    d += bi
                    x += xi
                # print(self.image[y - 1][x - 1])
                sumOfPixels += int(self.image[min(limit, y)][min(limit, x)])
        else:
            ai = (dx - dy) * 2
            bi = dx * 2
            d = bi - dy
            while not y == int(y_end):
                if d >= 0:
                    x += xi
                    y += yi
                    d += ai
                else:
                    d += bi
                    y += yi
                #print(self.image[y-1][x-1])
                sumOfPixels += int(self.image[min(limit, y)][min(limit, x)])
        #print("---------")
        #print(sumOfPixels)
        return sumOfPixels  # sum of brightnesses of pixels on a line between emiter and chosen decoder
