
from PyQt5.QtWidgets import QWidget, QMainWindow, QInputDialog, QMessageBox
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import QTimer
import time
from ui_MathFlash import Ui_MathFlashWindow

from gameContainer import gameContainer
from flashCardWidget import flashCardWidget

import mathConfig
import json
import os, sys

class mainWidget(QMainWindow):
    def __init__(self):
        super(mainWidget, self).__init__()
        self.ui = Ui_MathFlashWindow()
        self.ui.setupUi(self)
        self.currentPlayer = ''
        self.currentPlayerData = None
        self.playerData = dict()
        self.loadSettings()
        
        self.ui.playerCombo.activated[int].connect(self.playerComboCall)
        self.ui.flashBtn.clicked.connect(self.flashBtnClicked)

    def populatePlayerCombo(self):
        self.ui.playerCombo.clear()
        idx = 0
        p = 0
        for k in self.playerData.keys():
            self.ui.playerCombo.addItem(k)
            if k == self.currentPlayer:
                idx = p
            p += 1
        self.ui.playerCombo.addItem('Add Player...')
        self.ui.playerCombo.setCurrentIndex(idx)

    def setupPlayer(self, name):
        if name=='':
            if len(self.playerData) == 0:
                return
            name = self.playerData.keys()[0]

        if name != self.currentPlayer:
            if self.currentPlayer in self.playerData.keys():
                self.playerData[self.currentPlayer] = self.currentPlayerData

            self.currentPlayer = name
            self.currentPlayerData = self.playerData[self.currentPlayer]

        self.displayPlayerStats()

    def displayPlayerStats(self):
        curLevel = self.currentPlayerData['level']
        self.ui.curLevelTxt.setText('%d' % (curLevel+1))

        self.ui.totalScoreTxt.setText('%d' % (self.currentPlayerData['levelPoints'][curLevel]))
        correct = self.currentPlayerData['levelAccuracy'][curLevel][0]
        wrong = self.currentPlayerData['levelAccuracy'][curLevel][1]
        if wrong > 0:
            self.ui.accuracyTxt.setText('%d/%d (%1.2f%%)' % (correct, correct+wrong, 100.*correct/(correct+wrong)))
        else:
            self.ui.accuracyTxt.setText('%d/%d (0%%)' % (correct, correct+wrong))

    def loadSettings(self):
        fname = os.path.abspath(os.path.expanduser('~/.mathflash/mathflash.json'))
        if not os.path.exists(fname):
            if not os.path.exists(os.path.dirname(fname)):
                os.makedirs(os.path.dirname(fname))
            stg = {'players': {}}
            json.dump(stg, open(fname,'w'))

        data = json.load(open(fname,'r'))
        pdata = data['players']
        self.playerData = dict()
        lastPlayer = ''
        for k, v in pdata.iteritems():
            cfg = mathConfig.mathConfig()
            if v['lastPlayer']:
                lastPlayer=k
            for kk, vv in v.iteritems():
                cfg[kk] = vv
            self.playerData[k] = cfg

        if lastPlayer != '':
            self.currentPlayer = lastPlayer
            self.currentPlayerData = self.playerData[self.currentPlayer]
        self.populatePlayerCombo()
        self.setupPlayer(lastPlayer)

    def saveSettings(self):
        fname = os.path.abspath(os.path.expanduser('~/.mathflash/mathflash.json'))
        if not os.path.exists(fname):
            if not os.path.exists(os.path.dirname(fname)):
                os.makedirs(os.path.dirname(fname))
        playStg = dict()
        for k, v in self.playerData.iteritems():
            playStg[k] = v.settings
        stg = {'players': playStg}
        json.dump(stg, open(fname,'w'))
            
    def playerComboCall(self, idx):
        if idx == self.ui.playerCombo.count()-1:
            newName, ok = QInputDialog.getText(self,'Add New Player','Enter a new player name')
            if newName == '' or not ok:
                return
            if newName in self.playerData.keys():
                QMessageBox.information(self, 'Player exists', 'The player %s already exists' % (newName))

            newCfg = mathConfig.mathConfig()
            newCfg['lastPlayer'] = True
            for k in self.playerData.keys():
                self.playerData[k]['lastPlayer'] = False
            self.playerData[newName] = newCfg
            self.populatePlayerCombo()
            self.setupPlayer(newName)
        else:
            newName = self.ui.playerCombo.itemText(idx)
            if newName == self.currentPlayer:
                return
            for k in self.playerData.keys():
                if newName == k:
                    self.playerData[newName]['lastPlayer'] = True
                else:
                    self.playerData[newName]['lastPlayer'] = False

            self.setupPlayer(newName)
        self.saveSettings()
    
    def flashBtnClicked(self):
        if self.currentPlayer == '':
            # TODO add dlg
            return

        cfg = self.playerData[self.currentPlayer]
        W = flashCardWidget(cfg)
        dlg = gameContainer(W, cfg)
        dlg.setModal(True)
        dlg.exec_()
        score = dlg.totalScore
        correct = W.correct
        wrong = W.wrong
        self.updatePlayerStats(score, correct, wrong, 'flashCards')

    def updatePlayerStats(self, score, correct, wrong, gameName):
        cfg = self.currentPlayerData
        curLevel = cfg['level']
        levelPoints = cfg['levelPoints']
        levelAccuracy = cfg['levelAccuracy']

        if type(levelPoints) is not list:
            levelPoints = [0]

        levelAccuracy[curLevel][0] += correct
        levelAccuracy[curLevel][1] += wrong
        levelPoints[curLevel] += score
        if levelPoints[curLevel] < cfg['pointsForNextLevel'] or (1.*correct/(correct+wrong) < 0.8):
            cfg['levelPoints'] = levelPoints
            cfg['levelAccuracy'] = levelAccuracy
            self.currentPlayerData = cfg
            self.saveSettings()
            self.displayPlayerStats()
            return

        while len(levelPoints) <= curLevel+1:
            levelPoints.append(0)
        while len(levelAccuracy) <= curLevel+1:
            levelAccuracy.append([0,0])
        curLevel += 1
        cfg['level'] = curLevel
        cfg['levelPoints'] = levelPoints
        cfg['levelAccuracy'] = levelAccuracy
        self.currentPlayerData = cfg
        self.saveSettings()
        QMessageBox.information(self, 'Next Level!','Congratulation! You have moved to Level %d!' % (curLevel+1))
        self.displayPlayerStats()