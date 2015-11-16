import random

class mathFlashQuestion(object):
    def __init__(self):
        self.top = 0
        self.bottom = 0
        self.answer = 0
        self.qtype = None
        self.sign = '+'
        self.ptsScale = 1.

    def getNextQuestion(self, cfg, qtype=None):
        if qtype is None:
            qtype = random.randrange(0,4)

        if qtype == 0:
            self.top = random.randrange(cfg.addRanges[0], cfg.addRanges[1]+1)
            self.bottom = random.randrange(cfg.addRanges[0], cfg.addRanges[1]+1)
            self.answer = self.top + self.bottom
            self.sign = '+'
            self.ptsScale = cfg.addScale
        elif qtype == 1:
            self.top = random.randrange(cfg.subtRanges[0], cfg.subtRanges[1]+1)
            self.bottom = random.randrange(cfg.subtRanges[0], cfg.subtRanges[1]+1)
            if self.top < self.bottom:
                tmp = self.top
                self.top = self.bottom
                self.bottom = tmp
            self.answer = self.top - self.bottom
            self.sign = '-'
            self.ptsScale = cfg.subtScale
        elif qtype == 2:
            self.top = random.randrange(cfg.multRanges[0], cfg.multRanges[1]+1)
            self.bottom = random.randrange(cfg.multRanges[0], cfg.multRanges[1]+1)
            self.answer = self.top * self.bottom
            self.sign = 'X '
            self.ptsScale = cfg.multScale
        elif qtype == 3:
            self.answer = max(1,random.randrange(cfg.divideRanges[0], cfg.divideRanges[1]+1))
            self.bottom = max(1,random.randrange(cfg.divideRanges[0], cfg.divideRanges[1]+1))
            self.top = self.answer * self.bottom
            self.sign = '/ '
            self.ptsScale = cfg.divideScale

        return self

class mathConfig(object):
    def __init__(self):
        self.doAddition = True
        self.doSubtraction = True
        self.doMultiply = False 
        self.doDivide = False
        self._qtypes = []

        self.addScale = 1.
        self.subtScale = 1.5
        self.multScale = 2.
        self.divideScale = 2.5

        self.addRanges = [0, 100]
        self.subtRanges = [0, 100]
        self.multRanges = [0, 10]
        self.divideRanges = [0, 10]

        self.maxTime = 30
        self.numQuestions = 10
        self.pointsPerSec = 10
        self.minPoints = 100

    def get_qtypes(self):
        qtypes = []
        if self.doAddition:
            qtypes.append(0)
        if self.doSubtraction:
            qtypes.append(1)
        if self.doMultiply:
            qtypes.append(2)
        if self.doDivide:
            qtypes.append(3)

        self._qtypes = qtypes

    def get_next_qtype(self):
        self.get_qtypes()
        idx = random.randrange(0,len(self._qtypes))
        return self._qtypes[idx]
