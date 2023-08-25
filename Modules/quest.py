import pygame

class Quest():
    def __init__(self):
        self.currentQuest = None
        self.score = 0
        self.target = 0
        self.state = False
    
    def addScore(self):
        self.score += 1
        return self.score
    
    def assignQuest(self, questInd, target = 0):
        self.target = target
        self.quests = [self.patronQuest()]
        self.currentQuest = self.quests[questInd]

    def patronQuest(self):
        if self.score >= self.target:
            self.state = False
            return "Quest Completed!"
        
        return "Quest in progress ({}/{})".format(self.score, self.target)
    
    def update(self):
        self.currentQuest