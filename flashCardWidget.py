from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import QTimer
import time
from ui_flashCardsGame import Ui_flashCardGame
import mathConfig

class flashCardWidget(QWidget):
    def __init__(self, cfg):
        super(flashCardWidget, self).__init__()

        self.cfg = cfg
        self.ui = Ui_flashCardGame()
        self.ui.setupUi(self)
        self.questionGen = mathConfig.mathFlashQuestion()
        self.ui.ansBox.returnPressed.connect(self.getAnswer)
        self.qtypes = self.cfg.get_qtypes()

        self.totalScore = 0
        self.curScore = 0
        self.questionsAsked = 0
        self.runState = 0
        self.correct = 0
        self.wrong = 0
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.updateTimer)
        self.startTime = time.time()
        self.ui.startBtn.clicked.connect(self.startBtnPressed)

    def startBtnPressed(self):
        if self.runState == 0:
            fnt = self.ui.ansBox.font()
            fnt.setPointSize(80)
            self.ui.ansBox.setFont(fnt)
            self.curScore = 0
            self.questionsAsked = 0
            self.correct = 0
            self.wrong = 0
            self.runState = 1
            self.setupNextQuestion()
            
    def updateTimer(self):
        dt = time.time() - self.startTime 
        if dt > self.cfg.maxTime:
            self.timer.stop()
        self.curScore = max(self.cfg.minPoints, int((self.cfg.maxTime-dt)*self.cfg.pointsPerSec))
        self.ui.curScoreTxt.setText('%d' % self.curScore)

    def setupNextQuestion(self):
        self.curScore = self.cfg.maxTime*self.cfg.pointsPerSec
        self.startTime = time.time()
        qt = self.cfg.get_next_qtype()
        nextq = self.questionGen.getNextQuestion(self.cfg, qt)
        self.ui.valATxt.setText('%d' % nextq.top)
        self.ui.valBTxt.setText('%s%d' % (nextq.sign, nextq.bottom))
        self.ui.ansBox.setText('')

        self.ui.curScoreTxt.setText('%d' % (self.cfg.pointsPerSec*self.cfg.maxTime))
        self.timer.start()
       
    def getAnswer(self):
        if self.runState != 1:
            return
        self.timer.stop()
        ansTxt = self.ui.ansBox.text()
        ansNum = int(ansTxt)
        if ansNum == self.questionGen.answer:
            self.correctAnswer()
        else:
            self.wrongAnswer()
        self.questionsAsked += 1

        if self.questionsAsked < self.cfg.numQuestions:
            self.setupNextQuestion()
        else:
            self.finish()

    def finish(self):
        fnt = self.ui.ansBox.font()
        fnt.setPointSize(40)
        self.ui.ansBox.setFont(fnt)
        self.ui.feedbackLabel.setText('Great Job! You got %d/%d right!' % (self.correct, self.correct+self.wrong))

        pal = self.ui.feedbackLabel.palette()
        pal.setColor(self.ui.feedbackLabel.foregroundRole(), QColor(0,0,255))
        self.ui.feedbackLabel.setPalette(pal)
        self.runState = 0

    def correctAnswer(self):         
        self.correct += 1
        t = self.cfg.maxTime
        t -= time.time() - self.startTime
        pts = max(self.cfg.minPoints, int(t*self.cfg.pointsPerSec*self.questionGen.ptsScale))
        self.totalScore += pts
        self.ui.totalScoreTxt.setText('%d' % self.totalScore)
        pal = self.ui.feedbackLabel.palette()
        pal.setColor(self.ui.feedbackLabel.foregroundRole(), QColor(0,255,0))
        self.ui.feedbackLabel.setText('Correct!')
        self.ui.feedbackLabel.setPalette(pal)

    def wrongAnswer(self):
        self.wrong += 1
        pal = self.ui.feedbackLabel.palette()
        pal.setColor(self.ui.feedbackLabel.foregroundRole(), QColor(255,0,0))
        self.ui.feedbackLabel.setText('Wrong!')
        self.ui.feedbackLabel.setPalette(pal)
