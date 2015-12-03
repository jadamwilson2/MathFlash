from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import QTimer, pyqtSignal
import time

class gameWidget(QWidget):
    updateScore = pyqtSignal(int, name='updateScore')
    updateCurrentScore = pyqtSignal(int, name='updateCurrentScore')

    started = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, cfg):
        super(gameWidget, self).__init__()

        self.cfg = cfg
        self.totalScore = 0
        self.curScore = 0
        self.questionsAsked = 0
        self.runState = 0
        self.correct = 0
        self.wrong = 0

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.setSingleShot(False)

        self.startTime = time.time()

        self.timer.timeout.connect(self.updateTimer)
        
    def updateTimer(self):
        dt = time.time() - self.startTime
        if self.cfg['level'] < 4:
            dt = 0
        if dt > self.cfg['maxTime']:
            self.timer.stop()
        curScore = max(self.cfg['minPoints'], int((self.cfg['maxTime']-dt)*self.cfg['pointsPerSec']))
        self.updateCurrentScore.emit(curScore)

    def startGame(self):
    	raise RuntimeError('Game objects must implement start')

    def start(self):
        startScore = self.cfg['pointsPerSec']*self.cfg['maxTime']
        self.updateCurrentScore.emit(startScore)
        self.started.emit()
        self.startGame()

    def finishGame(self):
        raise RuntimeError('Game objects must implement finishGame')

    def finish(self):
        self.timer.stop()
        self.finished.emit()
        self.finishGame()
