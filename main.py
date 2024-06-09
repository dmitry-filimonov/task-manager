from PyQt5.QtWidgets import QApplication
import sys
from app.ui import MainWindow

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

