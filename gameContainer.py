from PyQt5 import QtCore, QtGui, QtWidgets

class gameContainer(QtWidgets.QDialog):
    def __init__(self, gameUI, cfg):
        super(gameContainer, self).__init__()
        self.setupUI(gameUI)
        self.totalScore = 0
        self.currentScore = 0
        self.done = False
        self.startBtn.pressed.connect(gameUI.start)
        self.gameUI.updateScore[int].connect(self.updateScore)
        self.gameUI.updateCurrentScore[int].connect(self.updateCurrentScore)
        self.gameUI.started.connect(self.startGame)
        self.gameUI.finished.connect(self.finishGame)

    def updateScore(self, score):
        self.totalScore = score
        self.totalScoreTxt.setText('%d' % self.totalScore)

    def updateCurrentScore(self, score):
        self.currentScore = score
        self.curScoreTxt.setText('%d' % self.currentScore)

    def startGame(self):
        self.startBtn.setEnabled(False)
        self.startBtn.pressed.disconnect()

    def finishGame(self):
        self.startBtn.setEnabled(True)
        self.startBtn.setText('Finish')
        self.startBtn.pressed.connect(self.acceptAndExit)

    def acceptAndExit(self):
        if not self.done:
            self.done = True
            return
        self.accept()
    def setupUI(self, gameUI):
        self.gameUI = gameUI

        self.setObjectName("gameContainer")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scoreFrame = QtWidgets.QFrame(self)
        self.scoreFrame.setMaximumSize(QtCore.QSize(225, 16777215))
        self.scoreFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.scoreFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.scoreFrame.setObjectName("scoreFrame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scoreFrame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.scoreFrame)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setUnderline(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.curScoreTxt = QtWidgets.QLabel(self.scoreFrame)
        font = QtGui.QFont()
        font.setPointSize(40)
        self.curScoreTxt.setFont(font)
        self.curScoreTxt.setObjectName("curScoreTxt")
        self.verticalLayout_2.addWidget(self.curScoreTxt)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(self.scoreFrame)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setUnderline(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.totalScoreTxt = QtWidgets.QLabel(self.scoreFrame)
        font = QtGui.QFont()
        font.setPointSize(40)
        self.totalScoreTxt.setFont(font)
        self.totalScoreTxt.setObjectName("totalScoreTxt")
        self.verticalLayout_2.addWidget(self.totalScoreTxt)
        self.startBtn = QtWidgets.QPushButton(self.scoreFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.startBtn.sizePolicy().hasHeightForWidth())
        self.startBtn.setSizePolicy(sizePolicy)
        self.startBtn.setMinimumSize(QtCore.QSize(0, 60))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(1, 1, 1))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(1, 1, 1))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(148, 148, 148))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.startBtn.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.startBtn.setFont(font)
        self.startBtn.setObjectName("startBtn")
        self.verticalLayout_2.addWidget(self.startBtn)

        self.horizontalLayout.addWidget(self.gameUI)
        self.horizontalLayout.addWidget(self.scoreFrame)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("gameContainer", "Game"))
        self.label.setText(_translate("gameContainer", "Score"))
        self.curScoreTxt.setText(_translate("gameContainer", "0"))
        self.label_2.setText(_translate("gameContainer", "Total Score"))
        self.totalScoreTxt.setText(_translate("gameContainer", "0"))
        self.startBtn.setText(_translate("gameContainer", "Start!"))
