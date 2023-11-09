import sys
import view

from PyQt5.QtWidgets import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = QMainWindow()
    ui = view.Ui_MainWindow()
    ui.setupUi(w)
    w.resize(320, 240)
    w.show()
    sys.exit(app.exec())
