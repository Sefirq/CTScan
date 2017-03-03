import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QLabel
from PyQt5.QtGui import QIcon


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(600, 280, 800, 600)
        self.setWindowTitle('Tomograf')
        self.setWindowIcon(QIcon('/home/sefir/Dokumenty/IwM/Tomograf/ctscan.png'))
        browseButton = QPushButton('Browse...', self)
        browseButton.setToolTip("Click to browse for images")
        browseButton.resize(browseButton.sizeHint())
        browseButton.move(100, 500)

        self.show()

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