import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *

from main_window import Ui_MainWindow
from moodle_window import Ui_MoodleWindow


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #Build the main window interface from main_window.py
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        

















if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Main()
    w.show()
    sys.exit(app.exec_())