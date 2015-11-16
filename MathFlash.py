from PyQt5.QtWidgets import QApplication, QDialog
from mainWidget import mainWidget
import mathConfig
import sys

def main():
    app = QApplication(sys.argv)
    window = mainWidget()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
