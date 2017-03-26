import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QErrorMessage, QVBoxLayout, QTextBrowser, QDialogButtonBox, QPushButton, QDialog, QMessageBox, QDesktopWidget, QMenuBar, QMainWindow, QAction, qApp, QFileDialog, QLabel, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QRect, Qt
from PyQt5 import QtCore, QtGui
from scipy import misc
from sinogramDialog import SinogramDialog


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
        self.setWindowIcon(QIcon('static/images/ctscan.png'))
        self.formWidget = FormWidget(self)
        self.setCentralWidget(self.formWidget)
        #showButton.move(100, 600)
        self.fileLabel = QLabel('', self)
        self.fileLabel.move(0, 12)
        self.showMaximized()
        exitAction = QAction(QIcon('static/images/exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        openAction = QAction(QIcon('static/images/open.png'), '&Open', self)
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
        filename = QFileDialog.getOpenFileName(self, "Select graphic file", "/home", "Images (*.png *.xpm *.jpg) ;; All files (*.*)", options=QFileDialog.DontUseNativeDialog)[0]
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
            self.formWidget.saveImage(self.image)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class FormWidget(QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.sinogramButton = QPushButton('Generate sinogram', self)
        self.sButton = QPushButton('Lol', self)
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
        self.alpha.setTabChangesFocus(True)
        self.alpha.setToolTip("Type angle of single iteration in degrees")
        self.detectors = QtWidgets.QTextEdit()
        self.detectors.setDisabled(True)
        self.detectors.setFixedHeight(25)
        self.detectors.setTabChangesFocus(True)
        self.detectors.setToolTip("Type number of detectors in the cone of emiter")
        self.width = QtWidgets.QTextEdit()
        self.width.setDisabled(True)
        self.width.setFixedHeight(25)
        self.width.setTabChangesFocus(True)
        self.width.setToolTip("Type width of cone of the emiter in degrees")
        self.sinogramButton.setToolTip("Click to generate sinogram")
        self.sinogramButton.resize(self.sinogramButton.sizeHint())
        self.sinogramButton.clicked.connect(self.newWindowWithSinogram)
        self.sinogramButton.setDisabled(True)
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
            self.sinogram = SinogramDialog(self.image, self.alpha.toPlainText(), self.detectors.toPlainText(), self.width.toPlainText())
            self.sinogram.showMaximized()
        else:
            self.error = QMessageBox.critical(None, "Error", "One of the values is wrong", QMessageBox.Ok)

    def saveImage(self, img):
        self.image = img

    def areGoodFields(self):
        try:
            _ = float(self.alpha.toPlainText())
            _ = int(self.detectors.toPlainText())
            _ = int(self.width.toPlainText())
        except ValueError:
            return False
        #if int(self.alpha.toPlainText()) not in range(1, 360):
            #return False
        if int(self.detectors.toPlainText()) <= 0:
            return False
        if int(self.width.toPlainText()) not in range(1, 360):
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