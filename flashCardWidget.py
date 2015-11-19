from PyQt5.QtWidgets import QWidget, QDialog, QFrame
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import QTimer, pyqtSignal
import time
from ui_flashCardsGame import Ui_flashCardGame
from gameWidget import gameWidget
import mathConfig
import random

class mathFlashQuestion(object):
    def __init__(self):
        self.top = 0
        self.bottom = 0
        self.answer = 0
        self.qtype = None
        self.sign = '+'
        self.ptsScale = 1.

    def get_qtypes(self, cfg):
        qtypes = []
        qtypes.append(0)
        cfg['doAddition'] = True
        if cfg['level'] >= 5:
            qtypes.append(1)
        if cfg['level'] >= 10:
            qtypes.append(2)
        if cfg['level'] >= 15:
            qtypes.append(3)
        
        return qtypes

    def get_next_qtype(self, cfg):
        qtypes = self.get_qtypes(cfg)
        idx = random.randrange(0,len(qtypes))
        return qtypes[idx]
    
    def getNextQuestion(self, cfg):
        qtype = self.get_next_qtype(cfg)
        level = cfg['level']
        if qtype == 0:
            self.top = random.randrange(cfg['addRanges'][0], cfg['addRanges'][1]*(level+1)+1)
            self.bottom = random.randrange(cfg['addRanges'][0], cfg['addRanges'][1]*(level+1)+1)
            self.answer = self.top + self.bottom
            self.sign = '+'
            self.ptsScale = cfg['addScale']
        elif qtype == 1:
            self.top = random.randrange(cfg['subtRanges'][0], cfg['subtRanges'][1]*(level+1)+1)
            self.bottom = random.randrange(cfg['subtRanges'][0], cfg['subtRanges'][1]*(level+1)+1)
            if self.top < self.bottom:
                tmp = self.top
                self.top = self.bottom
                self.bottom = tmp
            self.answer = self.top - self.bottom
            self.sign = '-'
            self.ptsScale = cfg['subtScale']
        elif qtype == 2:
            self.top = random.randrange(cfg['multRanges'][0], cfg['multRanges'][1]*(level-10+1)+1)
            self.bottom = random.randrange(cfg['multRanges'][0], cfg['multRanges'][1]*(level-10+1)+1)
            self.answer = self.top * self.bottom
            self.sign = 'X '
            self.ptsScale = cfg['multScale']
        elif qtype == 3:
            self.answer = max(1,random.randrange(cfg['divideRanges'][0], cfg['divideRanges'][1]*(level-10+1)+1))
            self.bottom = max(1,random.randrange(cfg['divideRanges'][0], cfg['divideRanges'][1]*(level-10+1)+1))
            self.top = self.answer * self.bottom
            self.sign = '/ '
            self.ptsScale = cfg['divideScale']

        return self

class flashCardWidget(gameWidget):
    def __init__(self, cfg):
        super(flashCardWidget, self ).__init__(cfg)

        self.ui = Ui_flashCardGame()
        self.ui.setupUi(self)
        self.questionGen = mathFlashQuestion()

        self.done = False

        self.ui.ansBox.returnPressed.connect(self.getAnswer)        
        self.ui.ansBox.setEnabled(False)

    def startGame(self):
        if self.runState == 0:
            fnt = self.ui.ansBox.font()
            fnt.setPointSize(80)
            self.ui.ansBox.setFont(fnt)
            self.curScore = 0
            self.questionsAsked = 0
            self.correct = 0
            self.wrong = 0
            self.runState = 1
            self.ui.ansBox.setEnabled(True)
            self.setupNextQuestion()
        elif self.runState == 2:
            if not self.done:
                self.done = True
                return
            
    def setupNextQuestion(self):
        self.curScore = self.cfg['maxTime']*self.cfg['pointsPerSec']
        self.startTime = time.time()
        nextq = self.questionGen.getNextQuestion(self.cfg)
        self.ui.valATxt.setText('%d' % nextq.top)
        self.ui.valBTxt.setText('%s%d' % (nextq.sign, nextq.bottom))
        self.ui.ansBox.setText('')

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

        if self.questionsAsked < self.cfg['numQuestions']:
            self.setupNextQuestion()
        else:
            self.finish()

    def correctAnswer(self):         
        self.correct += 1
        t = self.cfg['maxTime']
        t -= time.time() - self.startTime
        pts = max(self.cfg['minPoints'], int(t*self.cfg['pointsPerSec']*self.questionGen.ptsScale))
        self.totalScore += pts
        self.updateScore[int].emit(self.totalScore)
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

    def finishGame(self):
        fnt = self.ui.feedbackLabel.font()
        fnt.setPointSize(20)
        self.ui.feedbackLabel.setFont(fnt)
        self.ui.feedbackLabel.setText('Great Job! You got %d/%d right!' % (self.correct, self.correct+self.wrong))

        pal = self.ui.feedbackLabel.palette()
        pal.setColor(self.ui.feedbackLabel.foregroundRole(), QColor(0,0,255))
        self.ui.feedbackLabel.setPalette(pal)
        self.ui.ansBox.setEnabled(False)
        self.runState = 2
