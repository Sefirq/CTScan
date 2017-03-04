import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QDesktopWidget, QMenuBar, QMainWindow, QAction, qApp, QFileDialog, QLabel, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QRect

class Scene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        self.center()
        self.setWindowTitle('Tomograf')
        self.setWindowIcon(QIcon('/home/sefir/Dokumenty/IwM/Tomograf/CTScan/ctscan.png'))
        showButton = QPushButton('Show', self)
        showButton.setToolTip("Click to see current image")
        showButton.resize(showButton.sizeHint())
        showButton.move(100, 500)
        showButton.clicked.connect(self.showImage)
        self.fileLabel = QLabel('', self)
        self.fileLabel.move(0, 12)
        self.picture = None
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 0, 0)
        self.gv = QGraphicsView(self.scene)
        #self.gv.setGeometry(QRect(50, 50, 400, 200))
        self.gv.setScene(self.scene)
        self.gv.setWindowTitle("Image loaded")
        self.show()
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

    def showImage(self):
        self.gv.show()

    def browseFiles(self, event):
        filename = QFileDialog.getOpenFileName(self, "Select graphic file", "/home", "Images (*.png, *.jpg)")[0]
        if(len(filename) > 0):
            self.fileLabel.setText("Loadad " + filename)
            width = self.fileLabel.fontMetrics().boundingRect(self.fileLabel.text()).width()
            self.fileLabel.setFixedWidth(width+10)
            self.picture = QPixmap(filename)
            self.scene.clear()
            self.scene.addItem(QGraphicsPixmapItem(self.picture))
            self.gv.setSceneRect(QGraphicsPixmapItem(self.picture).boundingRect())
            self.gv.fitInView(QGraphicsPixmapItem(self.picture).boundingRect())
            self.gv.show()



    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())