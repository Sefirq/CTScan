import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QDesktopWidget, QMenuBar, QMainWindow, QAction, qApp, QFileDialog, QLabel, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QRect, Qt
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
            #self.gv.show()



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
        self.showButton = QPushButton('Show', self)
        self.sButton = QPushButton('Lol', self)
        self.showButton.setToolTip("Click to see current image")
        self.showButton.resize(self.showButton.sizeHint())
        self.showButton.clicked.connect(self.showImage)
        self.picture = None
        self.image = None
        self.scene = QGraphicsScene()
        self.sscene = QGraphicsScene()

        self.grid = QtWidgets.QGridLayout(self)
        self.hbox = QtWidgets.QHBoxLayout()
        self.createGraphicView()
        self.gv2 = QGraphicsView(self.sscene, self)
        self.hbox.addWidget(self.showButton)
        self.hbox.addStretch(1)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.sButton)
        self.grid.addLayout(self.hbox, 0, 0, 1, 1)
        self.grid.addLayout(self.vbox, 1, 0, 1, 1)
        self.grid.addWidget(self.gv, 0, 1, 1, 1)
        self.grid.addWidget(self.gv2, 1, 1, 1, 1)
        self.setLayout(self.grid)

    def showImage(self):
        self.gv.show()


    def createGraphicView(self):
        self.gv = QGraphicsView(self.scene, self)
        self.gv.setGeometry(QRect(0, 0, 300, 300))
        #self.gv.setStyleSheet("background-color: rgb(50, 50, 50")
        #self.gv.setVisible(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())