import pygame
import random
import os

class OrderTimer():
    def __init__(self, time):
        self.called = pygame.time.get_ticks()
        self.time = time
        self.signal = False

    def update(self, current_time):
        if current_time - self.called >= self.time:
            self.signal = True
            self.called = current_time

class PatronObject():
    def __init__(self, screen, imgPath, fontOBJ):
        self.screen = screen
        self.patronImgSurface = pygame.transform.scale_by(pygame.image.load(imgPath), 4)
        self.patronImgRect = self.patronImgSurface.get_rect()
        self.correctOrder = None

        self.startDialogues = ["Howdy!", "Give me a good one eh'?", "So this is how you Canadians do yer buisiness.", "...", "You think you can do this?", "Just make the damn drink. I'm not in the mood.", 
                          "Trump or Biden 2024? I'm voting Ye.", "Spreddie Gibbs", "Make it well, or you will be making less then minimum wage scrub"]

        self.incorrectDialogues = ["WTF IS THIS??!!", "Dispicable.", "Oh hell naw", "You damned Commie!", "I'm reporting you to your manager >:(", "You should kill yourself NOW!", "Stupid. (In French)", 
                                   "Are you dyslexic?", "Gawd damn 4th Grader.", "Down voted.", ":(", "Never gonna give you up, Never gonna let you down, Never gonna run around and desert you, Never gonna make you cry, Never gonna say goodbye, Never gonna tell a lie and hurt you"]
        
        self.correctDialogues = ["Nice!", "Thanks pardner!", "You should get a raise.", "...", "Blessed patriot of these United... oh your Canadian right?", "This looks good!", ":)", 
                                 "Looks Heavenly, keep it up.", "Oh! Tres bien, Merci Beaucoup! (In English)", "I was going to say something in Spanish, but my spanish teacher got deported",
                                 "Thanks, now ima go bust Trump out of jail.", "Could have been faster...", "Kendrick > Drake and Cole", "Thanks!, I will drink this faster than I drank your Mom!",
                                 "Amazin'", "You've got a friend in me...", "POG!"]

        self.font = fontOBJ
        self.dialogueSurface = self.font.render(self.startDialogues[random.randrange(0, len(self.startDialogues))], True, (0, 0, 0))
        self.dialogueRect = self.dialogueSurface.get_rect()
        
    def changeDialogue(self, correctOrderBool):
        if correctOrderBool == True:
            self.dialogueSurface = self.font.render(self.correctDialogues[random.randrange(0, len(self.correctDialogues))], True, (0, 0, 0))
        elif correctOrderBool == False:
            self.dialogueSurface = self.font.render(self.incorrectDialogues[random.randrange(0, len(self.incorrectDialogues))], True, (0, 0, 0))
        self.dialogueRect = self.dialogueSurface.get_rect()

    def draw(self, centerx, centery):
        self.patronImgRect.centerx = centerx
        self.patronImgRect.centery = centery + 200
        self.dialogueRect.centerx = self.patronImgRect.centerx
        self.dialogueRect.y = self.patronImgRect.bottom


        self.screen.blit(self.patronImgSurface, self.patronImgRect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.dialogueRect)
        self.screen.blit(self.dialogueSurface, self.dialogueRect)

class Order():
    def __init__(self, screen, speed, font, img, patronDir):
        # In istializing screen, speed rectangle and colors
        self.screen = screen
        self.speed = speed
        self.rect = pygame.Rect(0, 0, 200, 100)

        self.blue = self.green = self.red = self.yellow = self.purple = 0

        # Creating dictionary for each color and the order amounds
        self.optionsDict = {
            "Blue" : self.blue,
            "Red" : self.red,
            "Green" : self.green,
            "Yellow" : self.yellow,
            "Purple" : self.purple
        }
        # Creating list of the order keys
        self.optionsList = [key for key in self.optionsDict.keys()]

        # Generating random amount of colors and creating set to avoid duplicates
        numofChoices = random.randint(1, 5)
        self.order = set()

        # for the amount of colors, geenerate random value for each
        for i in range(numofChoices):
            self.order.add(random.choice(self.optionsList))

        # And for each item in the order add it to text to display final order
        self.text = ""
        for order in self.order:
            val = random.randrange(1, 8)
            self.optionsDict[order] = val
            self.text += order + f" = {val}, "


        # text stuff
        self.fontSurface = pygame.font.Font(font, 20)
        self.fontTextSurface = self.fontSurface.render(self.text, True, (255, 255, 255))
        self.fontTextRect = self.fontTextSurface.get_rect()
        self.fontTextRect.center = self.rect.center
        
        # Image Stuff
        self.imgSurface = pygame.image.load(img)
        self.imgRect = self.imgSurface.get_rect()
        self.imgRect.center = self.rect.center
        
        # Patron Image Stuff
        self.patronImgList = [os.path.join(patronDir, img) for img in os.listdir(patronDir)]
        self.patron = PatronObject(self.screen, self.patronImgList[random.randrange(0, len(self.patronImgList))], self.fontSurface)

        self.slideOrd = [1,0]
        self.timer = None

    def reset(self):
        self.rect = pygame.Rect(0, 0, 200, 100)

        self.blue = self.green = self.red = self.yellow = self.purple = 0
        self.optionsDict = {
            "Blue" : self.blue,
            "Red" : self.red,
            "Green" : self.green,
            "Yellow" : self.yellow,
            "Purple" : self.purple
        }

        self.optionsList = [key for key in self.optionsDict.keys()]
        numofChoices = random.randint(1, 5)
        self.order = set()
        for i in range(numofChoices):
            self.order.add(random.choice(self.optionsList))

        self.text = ""
        for order in self.order:
            val = random.randrange(1, 8)
            self.optionsDict[order] = val
            self.text += order + f" = {val}, "

        self.patron = PatronObject(self.screen, self.patronImgList[random.randrange(0, len(self.patronImgList))], self.fontSurface)
        self.fontTextSurface = self.fontSurface.render(self.text, True, (255, 255, 255))
        self.fontTextRect = self.fontTextSurface.get_rect()
        self.timer = None

    def slide(self):
        if self.slideOrd == [1,0]:
            if self.rect.centerx != self.screen.get_width() / 2:
                self.rect.x += self.speed
            else:
                self.slideOrd = [0, 0]
        elif self.slideOrd == [0,1]:
            if self.timer.signal:
                if self.rect.x <= self.screen.get_width():
                    self.rect.x += self.speed
                else:
                    self.slideOrd = [1, 0]
                    self.reset()
    
    def draw(self, curTime):
        # Positioning of the attributes
        self.fontTextRect.center = self.rect.center
        self.imgRect.center = self.rect.center

        # Checking order movement
        self.slide()
        if self.timer != None:
            self.timer.update(curTime)

        # Putting everything on the screen
        pygame.draw.rect(self.screen, (100, 100, 100), self.rect, border_radius=4)
        self.screen.blit(self.imgSurface, self.imgRect)
        self.screen.blit(self.fontTextSurface, self.fontTextRect)
        self.patron.draw(self.rect.centerx, self.rect.centery)

