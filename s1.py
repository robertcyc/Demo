from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer,QThread
from PyQt5.QtGui import QTextCursor
from ui import Ui_MainWindow
import time
import sys

class myWindows(QtWidgets.QMainWindow):
    def __init__(self):
    #++++++++++++++++++++++++++++++++
     #+ Create the windows form
     #++++++++++++++++++++++++++++++++
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        #++++++++++++++++++++++++++++++++++++++++++++++


def main():
    app=QtWidgets.QApplication([])
    application=myWindows()
    application.show()
    sys.exit(app.exec())

# script starts from here

if __name__=="__main__":
    main()