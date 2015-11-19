from PyQt5.QtWidgets import QWidget, QDialog, QFrame, QTableWidgetItem
from PyQt5.QtGui import QColor, QPalette
import time
from ui_footballBoxScores import Ui_footballBoxScoreGame
from gameWidget import gameWidget
import mathConfig
import random
import nflgame
import datetime
import time

class fbBoxScore(object):
    def __init__(self):
        self.homeTeam = ''
        self.awayTeam = ''
        self.gameDate = None
        self.gameTime = ''
        self.homeScores = []
        self.awayScores = []
        self.homeFinalScore = 0
        self.awayFinalScore = 0

        self._firstYear = 2009
        self._thisYear = datetime.date.today().year
        self._firstWeek = 1
        self._lastWeek = 17

    def getNextQuestion(self, cfg):
        while True:
            week = random.randrange(self._firstWeek, self._lastWeek+1)
            year = random.randrange(self._firstYear, self._thisYear+1)
            print year, week
            try:
                games = nflgame.games(year, week=week)
                g = random.randrange(0, len(games))
                game = games[g]
                if game.score_away_q5 > 0 or game.score_home_q5 > 0:
                    continue

                self.homeTeam = game.home
                self.awayTeam = game.away
                self.gameDate = datetime.datetime(game.schedule['year'], game.schedule['month'], game.schedule['day'])
                self.gameTime = game.schedule['time']

                self.homeScores = [game.score_home_q1, game.score_home_q2, game.score_home_q3, game.score_home_q4]
                self.awayScores = [game.score_away_q1, game.score_away_q2, game.score_away_q3, game.score_away_q4]
                self.homeFinalScore = game.score_home
                self.awayFinalScore = game.score_away

                break
            except:
                pass
        return self

class fbBoxScoreWidget(gameWidget):
    def __init__(self, cfg):
        super(fbBoxScoreWidget, self ).__init__(cfg)

        self.ui = Ui_footballBoxScoreGame()
        self.ui.setupUi(self)
        self.fbQuestion = fbBoxScore()

        self.done = False

        #self.ui.ansBox.returnPressed.connect(self.getAnswer)
        #self.ui.ansBox.setEnabled(False)

    def startGame(self):
        if self.runState == 0:
            self.curScore = 0
            self.questionsAsked = 0
            self.homeAnswer = None
            self.awayAnswer = None
            self.homeTry = None
            self.awayTry = None
            self.correct = 0
            self.wrong = 0
            self.runState = 1

            self.setupNextQuestion()
        elif self.runState == 2:
            if not self.done:
                self.done = True
                return
            
    def setupNextQuestion(self):
        self.curScore = self.cfg['maxTime']*self.cfg['pointsPerSec']
        self.startTime = time.time()
        nextq = self.fbQuestion.getNextQuestion(self.cfg)

        self.ui.gameInfoLabel.setText('%s at %s on %s at %s' % (nextq.awayTeam, nextq.homeTeam, nextq.gameDate.strftime('%b %d, %Y'), nextq.gameTime))
        try:
            self.ui.scoreTable.cellChanged.disconnect()
        except:
            pass
        self.ui.scoreTable.setVerticalHeaderLabels([nextq.homeTeam, nextq.awayTeam])
        hq = random.randrange(0,4)
        aq = random.randrange(0,4)
        for q in range(4):
            if q != hq:
                self.ui.scoreTable.item(0,q).setText('%d' % nextq.homeScores[q])
            else:
                self.ui.scoreTable.item(0,q).setText('')
                self.homeAnswer = nextq.homeScores[q]

            if q != aq:
                self.ui.scoreTable.item(1,q).setText('%d' % nextq.awayScores[q])
            else:
                self.ui.scoreTable.item(1,q).setText('')
                self.awayAnswer = nextq.awayScores[q]

        self.ui.scoreTable.item(0,4).setText('%d' % nextq.homeFinalScore)
        self.ui.scoreTable.item(1,4).setText('%d' % nextq.awayFinalScore)

        self.homeTry = None
        self.awayTry = None

        self.ui.scoreTable.cellChanged.connect(self.checkCell)
        #self.timer.start()

    def checkCell(self, row, col):
        self.ui.feedbackLabel.setText('')
        try:
            val = int(self.ui.scoreTable.item(row, col).text())
        except:
            return
        if row == 0:
            self.homeTry = val
        elif row == 1:
            self.awayTry = val

        if self.homeTry is not None and self.awayTry is not None:
            self.checkAnswer()

    def checkAnswer(self):
        if self.runState != 1:
            return
        self.timer.stop()

        if self.homeAnswer == self.homeTry and self.awayAnswer == self.awayTry:
            self.ui.feedbackLabel.setText('Great!')
            self.correctAnswer()
        elif self.homeAnswer != self.homeTry and self.awayAnswer == self.awayTry:
            self.ui.feedbackLabel.setText('Nice try! The missing %s score was %d' % (self.fbQuestion.homeTeam, self.homeAnswer))
            self.wrongAnswer()
        elif self.homeAnswer == self.homeTry and self.awayAnswer != self.awayTry:
            self.ui.feedbackLabel.setText('Nice try! The missing %s score was %d' % (self.fbQuestion.awayTeam, self.awayAnswer))
            self.wrongAnswer()
        else:
            self.ui.feedbackLabel.setText('Nice try! The missing scores were %d and %d' % (self.homeAnswer, self.awayAnswer))
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
        pts = max(self.cfg['minPoints'], int(t*self.cfg['pointsPerSec']))
        self.totalScore += pts
        self.updateScore[int].emit(self.totalScore)
        pal = self.ui.feedbackLabel.palette()
        pal.setColor(self.ui.feedbackLabel.foregroundRole(), QColor(0,255,0))
        self.ui.feedbackLabel.setPalette(pal)

    def wrongAnswer(self):
        self.wrong += 1
        pal = self.ui.feedbackLabel.palette()
        pal.setColor(self.ui.feedbackLabel.foregroundRole(), QColor(255,0,0))
        self.ui.feedbackLabel.setPalette(pal)

    def finishGame(self):
        fnt = self.ui.feedbackLabel.font()
        fnt.setPointSize(20)
        self.ui.feedbackLabel.setFont(fnt)
        self.ui.feedbackLabel.setText('Great Job! You got %d/%d right!' % (self.correct, self.correct+self.wrong))

        pal = self.ui.feedbackLabel.palette()
        pal.setColor(self.ui.feedbackLabel.foregroundRole(), QColor(0,0,255))
        self.ui.feedbackLabel.setPalette(pal)
        self.runState = 2
