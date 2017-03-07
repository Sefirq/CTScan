import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QErrorMessage, QVBoxLayout, QTextBrowser, QDialogButtonBox, QPushButton, QDialog, QMessageBox, QDesktopWidget, QMenuBar, QMainWindow, QAction, qApp, QFileDialog, QLabel, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QRect, Qt
from PyQt5 import QtCore
from scipy import misc

class Scene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #self.resize(1000, 800)
        #self.center()
        self.setWindowTitle('Tomograf')
        self.setWindowIcon(QIcon('/home/sefir/Dokumenty/IwM/Tomograf/CTScan/ctscan.png'))
        self.formWidget = FormWidget(self)
        self.setCentralWidget(self.formWidget)
        #showButton.move(100, 600)
        self.fileLabel = QLabel('', self)
        self.fileLabel.move(0, 12)
        self.showMaximized()
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        openAction = QAction(QIcon('open.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open an image file')
        openAction.triggered.connect(self.browseFiles)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

    def center(self):
        fg = self.frameGeometry()
        centr = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(centr)
        self.move(fg.topLeft())



    def browseFiles(self, event):
        filename = QFileDialog.getOpenFileName(self, "Select graphic file", "/home", "Images (*.png, *.jpg)")[0]
        if(len(filename) > 0):
            self.fileLabel.setText("Loaded " + filename)
            width = self.fileLabel.fontMetrics().boundingRect(self.fileLabel.text()).width()
            self.fileLabel.setFixedWidth(width+10)
            self.formWidget.picture = QPixmap(filename)
            self.formWidget.scene.clear()
            self.formWidget.scene.addItem(QGraphicsPixmapItem(self.formWidget.picture))
            self.formWidget.gv.setSceneRect(QGraphicsPixmapItem(self.formWidget.picture).boundingRect())
            self.formWidget.gv.fitInView(QGraphicsPixmapItem(self.formWidget.picture).boundingRect(), Qt.KeepAspectRatio)
            self.formWidget.gv.setVisible(True)
            self.image = misc.imread(filename, mode="L")#, flatten=True) <- IMAGE IN 8bit greyscale
            self.img = QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.shape[1],
                              QImage.Format_Grayscale8)
            self.pict = QPixmap(self.img)
            self.formWidget.sscene.clear()
            self.formWidget.sscene.addPixmap(self.pict)
            self.formWidget.gv2.fitInView(QGraphicsPixmapItem(self.pict).boundingRect(),
                                         Qt.KeepAspectRatio)
            print(self.formWidget.image)
            self.formWidget.sinogramButton.setDisabled(False)
            self.formWidget.detectors.setDisabled(False)
            self.formWidget.alpha.setDisabled(False)
            self.formWidget.width.setDisabled(False)
            self.formWidget.setStyleSheet("QLabel {color: rgb(10, 10, 10)}")
            #self.gv.show()



    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class SinogramDialog(QDialog):
    def __init__(self, parent=None):
        super(SinogramDialog, self).__init__(parent)
        self.setWindowTitle("Sinogram")
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        #self.buttonBox.accepted.connect() <- what will happen on Ok
        self.buttonBox.rejected.connect(self.close) #<- what will happen on Cancel
        self.textBrowser = QTextBrowser(self)
        self.textBrowser.append("This is a QTextBrowser!")
        self.slider = QtWidgets.QSlider(Qt.Horizontal)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.slider)
        self.verticalLayout.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.buttonBox)

class FormWidget(QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.sinogramButton = QPushButton('Generate sinogram', self)
        self.sButton = QPushButton('Lol', self)
        self.sinogramButton.setToolTip("Click to generate sinogram")
        self.sinogramButton.resize(self.sinogramButton.sizeHint())
        self.sinogramButton.clicked.connect(self.newWindowWithSinogram)
        self.sinogramButton.setDisabled(True)
        self.picture = None
        self.image = None
        self.scene = QGraphicsScene()
        self.sscene = QGraphicsScene()
        self.grid = QtWidgets.QGridLayout(self)
        self.hbox = QtWidgets.QHBoxLayout()
        self.createGraphicView()
        self.gv2 = QGraphicsView(self.sscene, self)
        self.alpha = QtWidgets.QTextEdit()
        self.alpha.setDisabled(True)
        self.alpha.setFixedHeight(25)
        self.alpha.setToolTip("Type angle of single iteration in degrees")
        self.detectors = QtWidgets.QTextEdit()
        self.detectors.setDisabled(True)
        self.detectors.setFixedHeight(25)
        self.detectors.setToolTip("Type number of detectors in the cone of emiter")
        self.width = QtWidgets.QTextEdit()
        self.width.setDisabled(True)
        self.width.setFixedHeight(25)
        self.width.setToolTip("Type width of cone of the emiter in degrees")
        self.alphaLabel = QLabel("Angle alpha")
        self.detectorsLabel = QLabel("Number of detectors n")
        self.widthLabel = QLabel("Width of cone")
        self.formVBox = QtWidgets.QVBoxLayout()
        self.formVBox.addStretch(1)
        self.formVBox.addWidget(self.alphaLabel)
        self.formVBox.addWidget(self.alpha)
        self.formVBox.addWidget(self.detectorsLabel)
        self.formVBox.addWidget(self.detectors)
        self.formVBox.addWidget(self.widthLabel)
        self.formVBox.addWidget(self.width)
        self.formVBox.addWidget(self.sinogramButton)
        self.setStyleSheet("QLabel {color: rgb(200, 200, 200)}")
        self.hbox.addLayout(self.formVBox)
        self.hbox.addStretch(1)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.sButton)
        self.grid.addLayout(self.hbox, 0, 0, 1, 1)
        self.grid.addLayout(self.vbox, 1, 0, 1, 1)
        self.grid.addWidget(self.gv, 0, 1, 1, 1)
        self.grid.addWidget(self.gv2, 1, 1, 1, 1)
        self.setLayout(self.grid)

    @QtCore.pyqtSlot()
    def newWindowWithSinogram(self):

        if(self.areGoodFields()):
            self.sinogram = SinogramDialog()
            self.sinogram.exec()
        else:
            self.error = QMessageBox.critical(None, "Error", "One of the values is wrong", QMessageBox.Ok)

    def areGoodFields(self):
        try:
            x = int(self.alpha.toPlainText())
            x = int(self.detectors.toPlainText())
            x = int(self.width.toPlainText())
        except ValueError:
            return False
        if int(self.alpha.toPlainText()) not in range(1, 360):
            return False
        if int(self.detectors.toPlainText()) <= 0:
            return False
        if int(self.width.toPlainText()) not in range(1, 180):
            return False
        return True


    def createGraphicView(self):
        self.gv = QGraphicsView(self.scene, self)
        self.gv.setGeometry(QRect(0, 0, 300, 300))
        #self.gv.setStyleSheet("background-color: rgb(50, 50, 50")
        #self.gv.setVisible(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())