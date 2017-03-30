from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QTextEdit, QWidget, QErrorMessage, QVBoxLayout, QTextBrowser, QDialogButtonBox, QPushButton, QDialog, QMessageBox, QDesktopWidget, QMenuBar, QMainWindow, QAction, qApp, QFileDialog, QLabel, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QRect, Qt
from PyQt5 import QtCore
from DICOMSaver import save_to_dicom_file
import math
import numpy as np
from matplotlib import pyplot as plt
from logic import SinogramLogic


class SinogramDialog(QDialog):
    def __init__(self, image, alpha, detectors, width, parent=None):
        super(SinogramDialog, self).__init__(parent)
        self.image = image
        self.alpha = float(alpha)
        self.detectors = int(detectors)
        self.width = int(width)
        self.scene = QGraphicsScene()
        self.sscene = QGraphicsScene()
        self.sinogram = np.zeros((1, self.detectors))
        self.setWindowTitle("Sinogram")
        self.slider = QtWidgets.QSlider(Qt.Horizontal)
        self.slider.setFixedWidth(360)
        self.slider.setRange(0, 100)
        self.slider.valueChanged.connect(self.valuechange)
        self.slabel = QLabel("")
        self.testButton = QPushButton("Click")
        self.testButton.clicked.connect(lambda: self.computeSinogram(self.slider.value()))
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        # self.buttonBox.accepted.connect() <- what will happen on Ok
        self.buttonBox.rejected.connect(self.close) # <- what will happen on Cancel
        self.gv = QGraphicsView(self.scene, self)
        self.gv.setGeometry(QRect(0, 0, 300, 300))
        self.gvresult = QGraphicsView(self.sscene, self)
        self.gvresult.setGeometry(QRect(0, 0, 300, 300))
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.verticalform = QtWidgets.QVBoxLayout(self)
        self.patient_sex = QTextEdit()
        self.patient_sex.setFixedWidth(200)
        self.patient_sex.setFixedHeight(25)
        self.patient_sex_label = QLabel("Type patient's sex (M F)")
        self.patient_sex_label.setFixedHeight(25)
        self.patient_name = QTextEdit()
        self.patient_name.setFixedWidth(200)
        self.patient_name.setFixedHeight(25)
        self.patient_name_label = QLabel("Type patient's name (Name^Surname)")
        self.patient_name_label.setFixedHeight(25)
        self.patients_ID = QTextEdit()
        self.patients_ID.setFixedWidth(200)
        self.patients_ID.setFixedHeight(25)
        self.patients_ID_label = QLabel("Type patient's ID")
        self.patients_ID_label.setFixedHeight(25)
        self.comment = QTextEdit()
        self.comment.setFixedWidth(200)
        self.comment.setFixedHeight(25)
        self.comment_label = QLabel("Type your comment")
        self.comment_label.setFixedHeight(25)
        self.date = QTextEdit()
        self.date.setFixedWidth(200)
        self.date.setFixedHeight(25)
        self.date_label = QLabel("Type date of photo (YYYYMMDD)")
        self.date_label.setFixedHeight(25)
        self.time = QTextEdit()
        self.time.setFixedWidth(200)
        self.time.setFixedHeight(25)
        self.time_label = QLabel("Type time of photo (HHMMSS.MMMMM")
        self.time_label.setFixedHeight(25)
        self.dicom_button = QPushButton("Save result to DICOM")
        self.dicom_button.setFixedHeight(25)
        self.dicom_button.clicked.connect(self.save_to_dicom)
        self.verticalform.addWidget(self.patient_name_label)
        self.verticalform.addWidget(self.patient_name)
        self.verticalform.addWidget(self.patients_ID_label)
        self.verticalform.addWidget(self.patients_ID)
        self.verticalform.addWidget(self.patient_sex_label)
        self.verticalform.addWidget(self.patient_sex)
        self.verticalform.addWidget(self.comment_label)
        self.verticalform.addWidget(self.comment)
        self.verticalform.addWidget(self.date_label)
        self.verticalform.addWidget(self.date)
        self.verticalform.addWidget(self.time_label)
        self.verticalform.addWidget(self.time)
        self.verticalform.addWidget(self.dicom_button)
        self.verticalform.addStretch(1)
        self.horizontalLayout.addLayout(self.verticalform)
        self.horizontalLayout.addWidget(self.gv)
        self.horizontalLayout.addWidget(self.gvresult)
        self.verticalLayout.addWidget(self.slider)
        self.verticalLayout.addWidget(self.slabel)
        self.verticalLayout.addWidget(self.testButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.buttonBox)
        self.sinogramLogic = SinogramLogic(self.image, self.alpha, self.detectors, self.width)

    def save_to_dicom(self):
        save_to_dicom_file(self.invsg, "dicom_output.dcm", self.patient_name.toPlainText(), self.patients_ID.toPlainText(), self.patient_sex.toPlainText(),
                           self.comment.toPlainText(), self.date.toPlainText(), self.time.toPlainText())
        self.info = QMessageBox.information(self, "File saved", "File saved to .dcm", QMessageBox.Ok)


    def valuechange(self):
        self.slabel.setText(str(self.slider.value())+"%")
        # sg = self.sinograms[self.slider.value()]
        # invsg = self.invsinograms[self.slider.value()]
        # self.img = QImage(sg.astype(np.uint8), sg.shape[1], sg.shape[0], sg.shape[1], QImage.Format_Grayscale8)
        # self.pict = QPixmap(self.img)
        # print(type(self.pict))
        # self.scene.clear()
        # self.scene.addPixmap(self.pict)
        # self.gv.fitInView(QGraphicsPixmapItem(self.pict).boundingRect(), Qt.KeepAspectRatio)
        # self.gv.setScene(self.scene)
        # self.img2 = QImage(invsg.astype(np.uint8), invsg.shape[1], invsg.shape[0], invsg.shape[1], QImage.Format_Grayscale8)
        # self.pict2 = QPixmap(self.img2)
        # self.sscene.clear()
        # self.sscene.addPixmap(self.pict2)
        # self.gvresult.fitInView(QGraphicsPixmapItem(self.pict2).boundingRect(), Qt.KeepAspectRatio)
        # self.gvresult.setScene(self.sscene)

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
        progress = progress*1.0/100
        sinogram = SinogramLogic(self.image, self.alpha, self.detectors, self.width)
        print("ok")
        sg, invsg = sinogram.image_processing(self.image, self.alpha, progress, self.detectors, self.width)
        print(sg.shape, type(sg), invsg.shape, type(invsg))
        sg = sg*1.0/np.max(sg)*255  # normalize
        self.invsg = invsg*1.0/np.max(invsg)*255  # normalize
        plt.imshow(sg, cmap="gray")
        plt.savefig('foo.png')
        self.img = QImage(sg.astype(np.uint8), sg.shape[1], sg.shape[0], sg.shape[1], QImage.Format_Grayscale8)
        self.pict = QPixmap(self.img)
        print(type(self.pict))
        self.scene.clear()
        self.scene.addPixmap(self.pict)
        self.gv.fitInView(QGraphicsPixmapItem(self.pict).boundingRect(), Qt.KeepAspectRatio)
        self.gv.setScene(self.scene)
        self.img2 = QImage(self.invsg.astype(np.uint8), self.invsg.shape[1], self.invsg.shape[0], self.invsg.shape[1], QImage.Format_Grayscale8)
        self.pict2 = QPixmap(self.img2)
        self.sscene.clear()
        self.sscene.addPixmap(self.pict2)
        self.gvresult.fitInView(QGraphicsPixmapItem(self.pict2).boundingRect(), Qt.KeepAspectRatio)
        self.gvresult.setScene(self.sscene)
        plt.imshow(sg, cmap="gray")
        plt.savefig('result.png')


