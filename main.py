import sys

import sys

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg

from panel import MainWindow
from logger import logger

if __name__ == '__main__':
    app = qtw.QApplication([])
    app.setWindowIcon(qtg.QIcon('vmon-logo.jpg'))
    app.setApplicationName("vmon")
    app.setApplicationDisplayName("vmon")
    app.setDesktopFileName("vmon")
    window = MainWindow()
    window.show()
    logger.info("Launching Application")
    sys.exit(app.exec_())