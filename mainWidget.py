
from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import QTimer
import time
from ui_MathFlash import Ui_MathFlashWindow
import mathConfig
import json

class mainWidget(QMainWindow):
    def __init__(self):
        super(mainWidget, self).__init__()
        self.cfg = mathConfig.mathConfig()
        self.ui = Ui_MathFlashWindow()
        self.ui.setupUi(self)

        self.playerData = dict()
        
        self.ui.playerCombo.currentIndexChanged[int].connect(self.playerComboCall)


    def playerComboCall(self, idx):
        print idx
        pass
    
