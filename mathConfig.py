import random


class mathConfig(object):
    def __init__(self):
        self._qtypes = []

        self.settings = dict()
        self.settings['doAddition'] = True
        self.settings['doSubtraction'] = False
        self.settings['doMultiply'] = False 
        self.settings['doDivide'] = False

        self.settings['addScale'] = 1.
        self.settings['subtScale'] = 1.5
        self.settings['multScale']= 2.
        self.settings['divideScale'] = 2.5

        self.settings['addRanges'] = [0, 5]
        self.settings['subtRanges'] = [0, 5]
        self.settings['multRanges'] = [0, 5]
        self.settings['divideRanges'] = [0, 5]

        self.settings['maxTime'] = 30
        self.settings['numQuestions'] = 10
        self.settings['pointsPerSec'] = 10
        self.settings['minPoints'] = 100

        self.settings['level'] = 0
        self.settings['pointsForNextLevel'] = 10000
        self.settings['levelPoints'] = [0]

        self.settings['lastPlayer'] = False
        self.settings['levelAccuracy'] = [[0,0]]

    def __getitem__(self, key):
        return self.settings[key]

    def __setitem__(self, key, val):
        if key not in self.settings.keys():
            raise KeyError('Invalid setting: %s', key)
        self.settings[key] = val


