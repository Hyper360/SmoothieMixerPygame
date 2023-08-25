import pygame
import os
import sys
from Modules.buttonGenerator import Button
from Modules.orderGenerator import Order, OrderTimer
from Modules.draw_text import blit_text
from Modules.gameExternals import *
from Modules.spritesheet import *
from Modules.musicPlayer import MusicPlayer
from Modules.quest import Quest


pygame.init()
pygame.mixer.init()

class Game():
    def __init__(self):
        # Directories
        self.state = "menu"
        self.curDir = os.path.dirname(os.path.abspath(__file__))
        self.musicDir = os.path.join(self.curDir, "Music")
        self.soundDir = os.path.join(self.curDir, "Sound")
        self.fontDir = os.path.join(self.curDir, "Fonts")
        self.imageDir = os.path.join(self.curDir, "Images")
        self.patronDir = os.path.join(self.imageDir, "Patrons")

        # Initializing Display
        pygame.display.set_caption("Smoothie Mixer")
        pygame.display.set_icon(pygame.image.load(os.path.join(self.imageDir, "icon.png")))
        self.screen = pygame.display.set_mode((1200, 800))
        self.clock = pygame.time.Clock()
        self.fullscreen = False
        self.delSig = False

        self.menuBackground = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "CoverBarImage.png")), (1200, 800))
        self.tutorialBackground = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "Tutorial.png")), (1200, 800))
        self.background = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "bar.png")), (1200, 800))
        self.background.set_alpha(200)

        self.windSound = pygame.mixer.Sound(os.path.join(self.soundDir, "Wind_Sound.mp3"))
        self.windChannel = pygame.mixer.Channel(0)
        self.windSoundPlaying = False

        self.rainSound = pygame.mixer.Sound(os.path.join(self.soundDir, "Rain_Sounds.mp3"))
        self.rainChannel = pygame.mixer.Channel(1)
        self.rainSoundPlaying = False

        self.chatterSound = pygame.mixer.Sound(os.path.join(self.soundDir, "Restaurant_Noise.mp3"))
        self.chatterChannel = pygame.mixer.Channel(2)
        self.chatterSoundPlaying = False

        self.bellSound = pygame.mixer.Sound(os.path.join(self.soundDir, "Bell_Sound.mp3"))
        self.bellChannel = pygame.mixer.Channel(2)
        
        self.musicPlayer = MusicPlayer(self.musicDir, 0.9)

        self.blender = SpritesheetRenderer(self.screen, 0, 0, 384, 64, 64, 64, 6, os.path.join(self.imageDir, "blenderon.png"), 250, 1.5)

        # Initializing buttons
        self.startButton = Button(self.screen, 500, 400, 200, 200, text = "START", font = os.path.join(self.fontDir, "AlienEncounters.ttf"), fontSize=50, bck=(190, 100, 30))
        self.blueButton = Button(self.screen, 0, 600, 100, 100, text="Blue +1", font = os.path.join(self.fontDir, "CascadiaMono.ttf"), fontSize=25, bck=(100, 100, 250), img= os.path.join(self.imageDir, "blueberry.png"))
        self.redButton = Button(self.screen, 110, 600, 100, 100, text="Red +1", font = os.path.join(self.fontDir, "CascadiaMono.ttf"), fontSize=25, bck=(250, 100, 100), img = os.path.join(self.imageDir, "redberry.png"))
        self.greenButton = Button(self.screen, 220, 600, 100, 100, text="Green +1", font = os.path.join(self.fontDir, "CascadiaMono.ttf"), fontSize=20, bck=(100, 250, 100), img= os.path.join(self.imageDir, "greenberry.png"))
        self.yellowButton = Button(self.screen, 330, 600, 100, 100, text="Yellow +1", font = os.path.join(self.fontDir, "CascadiaMono.ttf"), fontSize=20, bck=(255, 255, 150), img= os.path.join(self.imageDir, "lemon.png"))
        self.purpleButton = Button(self.screen, 440, 600, 100, 100, text="Purple +1", font = os.path.join(self.fontDir, "CascadiaMono.ttf"), fontSize=20, bck=(220, 155, 255), img= os.path.join(self.imageDir, "purpleberry.png"))
        self.enterButton = Button(self.screen, 550, 700, 100, 100, spritesheet=self.blender, text = "Return order", font = os.path.join(self.fontDir, "CascadiaMono.ttf"), fontSize=20, bck=(50, 50, 200))
        self.order = Order(self.screen, 20, os.path.join(self.fontDir, "CascadiaMono.ttf"), os.path.join(self.imageDir, "tray.png"), self.patronDir)
        self.blue = 0
        self.red = 0
        self.green = 0
        self.yellow = 0
        self.purple = 0

        # Initializing Storage Buttons
        self.blueStorage = 20
        self.blueStorageButton = Button(self.screen, 660, 600, 100, 100, text=f"Blue = {self.blueStorage}", font = os.path.join(self.fontDir, "CascadiaMono.ttf"), fontSize=20, img = os.path.join(self.imageDir, "crate.png"))
        self.redStorage = 20
        self.redStorageButton = Button(self.screen, 770, 600, 100, 100, text=f"Red = {self.redStorage}", font = os.path.join(self.fontDir, "CascadiaMono.ttf"), fontSize=20, img = os.path.join(self.imageDir, "crate.png"))
        self.greenStorage = 20
        self.greenStorageButton = Button(self.screen, 880, 600, 100, 100, text=f"Green = {self.greenStorage}", font = os.path.join(self.fontDir, "CascadiaMono.ttf"), fontSize=15, img = os.path.join(self.imageDir, "crate.png"))
        self.yellowStorage = 20
        self.yellowStorageButton = Button(self.screen, 990, 600, 100, 100, text=f"Yellow = {self.yellowStorage}", font = os.path.join(self.fontDir, "CascadiaMono.ttf"), fontSize=15, img = os.path.join(self.imageDir, "crate.png"))
        self.purpleStorage = 20
        self.purpleStorageButton = Button(self.screen, 1100, 600, 100, 100, text=f"Purple = {self.purpleStorage}", font = os.path.join(self.fontDir, "CascadiaMono.ttf"), fontSize=15, img = os.path.join(self.imageDir, "crate.png"))

        # Cash Multiplier
        self.cash = 0
        self.cashTimer = Timer(13000)
        self.cashMultiplier = 1
        self.streak = 1
    
    def mainMenu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.fullscreen == True:
                        self.screen = pygame.display.set_mode((1200, 800))
                        self.fullscreen = False

                    elif self.fullscreen == False:
                        self.screen = pygame.display.set_mode((1200, 800), flags=pygame.FULLSCREEN)
                        self.fullscreen = True
                    

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.menuBackground, (0, 0))

        self.startButton.draw()
        if getButtonPress(self.startButton):
            self.windChannel.stop()
            self.startButton.rect.y -= 250
            self.startButton.refreshText()
            pygame.mixer.music.load(os.path.join(self.soundDir, "Briefing.mp3"))
            pygame.mixer.music.play()
            self.state = "tutorial"

        if self.windSoundPlaying == False:
            self.windChannel.play(self.windSound, -1)
            self.windChannel.set_volume(0.4)
            self.windSoundPlaying = True
        else:
            pass

        pygame.display.flip()
        self.clock.tick(60)

    def controlScreen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.fullscreen == True:
                        self.screen = pygame.display.set_mode((1200, 800))
                        self.fullscreen = False

                    elif self.fullscreen == False:
                        self.screen = pygame.display.set_mode((1200, 800), flags=pygame.FULLSCREEN)
                        self.fullscreen = True

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.tutorialBackground, (0, 0))

        self.startButton.draw()
        if getButtonPress(self.startButton):
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            self.state = "level"

        pygame.display.flip()
        self.clock.tick(60)

    def level(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.musicPlayer.skip()
                if event.key == pygame.K_ESCAPE:
                    if self.fullscreen == True:
                        self.screen = pygame.display.set_mode((1200, 800))
                        self.fullscreen = False

                    elif self.fullscreen == False:
                        self.screen = pygame.display.set_mode((1200, 800), flags=pygame.FULLSCREEN)
                        self.fullscreen = True

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        self.curTime = pygame.time.get_ticks()

        # Drawing of the buttons and Order
        self.blueButton.draw()
        self.redButton.draw()
        self.greenButton.draw()
        self.yellowButton.draw()
        self.purpleButton.draw()
        
        self.blueStorageButton.draw()
        self.redStorageButton.draw()
        self.greenStorageButton.draw()
        self.yellowStorageButton.draw()
        self.purpleStorageButton.draw()

        self.enterButton.draw(self.curTime)
        self.order.draw(self.curTime)

        # Refresh the text for the storage
        self.blueStorageButton.refreshText(f"Blue = {self.blueStorage}")
        self.redStorageButton.refreshText(f"Red = {self.redStorage}")
        self.greenStorageButton.refreshText(f"Green = {self.greenStorage}")
        self.yellowStorageButton.refreshText(f"Yellow = {self.yellowStorage}")
        self.purpleStorageButton.refreshText(f"Purple = {self.purpleStorage}")

        # Checking if the buttons were pressed
        self.blue, self.blueStorage = increment(self.blueButton, self.blue, 10, 1, self.blueStorage, 1) if self.blueStorage > 0 else (self.blue, 0)
        self.red, self.redStorage = increment(self.redButton, self.red, 10, 1, self.redStorage, 1) if self.redStorage > 0 else (self.red, 0)
        self.green, self.greenStorage = increment(self.greenButton, self.green, 10, 1, self.greenStorage, 1) if self.greenStorage > 0 else (self.green, 0)
        self.yellow, self.yellowStorage = increment(self.yellowButton, self.yellow, 10, 1, self.yellowStorage, 1) if self.yellowStorage > 0 else (self.yellow, 0)
        self.purple, self.purpleStorage = increment(self.purpleButton, self.purple, 10, 1, self.purpleStorage, 1) if self.purpleStorage > 0 else (self.purple, 0)

        if self.cash >= 20:
            self.blueStorage, self.cash = increment(self.blueStorageButton, self.blueStorage, 50, 5, self.cash, 20) 
            self.redStorage, self.cash = increment(self.redStorageButton, self.redStorage, 50, 5, self.cash, 20)
            self.greenStorage, self.cash = increment(self.greenStorageButton, self.greenStorage, 50, 5, self.cash, 20)
            self.yellowStorage, self.cash = increment(self.yellowStorageButton, self.yellowStorage, 50, 5, self.cash, 20)
            self.purpleStorage, self.cash = increment(self.purpleStorageButton, self.purpleStorage, 50, 5, self.cash, 20)
        
        # Checking endgame conditions
        self.cashTimer.update(self.curTime)
        
        if self.enterButton.pressed[0] == True:
            
            # Cash multiplier being checked
            if self.cashTimer.signal == False:
                self.cashMultiplier += 0.1
            else:
                self.cashMultiplier = 1

            if [self.blue, self.red, self.green, self.yellow, self.purple] == list(self.order.optionsDict.values()):
                self.cash += round(5 * self.streak * self.cashMultiplier, 2)
                self.streak += 1
                self.order.patron.changeDialogue(True)
            else:
                self.cashMultiplier = 1
                self.cash -= 25
                self.streak = 1
                self.order.patron.changeDialogue(False)

            self.order.slideOrd = [0, 1]
            self.order.timer = OrderTimer(3000)
            self.bellChannel.play(self.bellSound) 
            self.blue = 0
            self.red = 0
            self.green = 0
            self.yellow = 0
            self.purple = 0
            self.cashTimer.reset(self.curTime)
        
        if self.cash < 0:
            self.state = "gameover"

        # Text
        blit_text(self.screen, "Blue = {}".format(self.blue), (self.blueButton.rect.centerx, self.blueButton.rect.top - 20), pygame.font.Font(os.path.join(self.fontDir, "CascadiaMono.ttf"), 15), (0, 0, 200))
        blit_text(self.screen, "Red = {}".format(self.red), (self.redButton.rect.centerx, self.redButton.rect.top - 20), pygame.font.Font(os.path.join(self.fontDir, "CascadiaMono.ttf"), 15), (200, 0, 0))
        blit_text(self.screen, "Green = {}".format(self.green), (self.greenButton.rect.centerx, self.greenButton.rect.top - 20), pygame.font.Font(os.path.join(self.fontDir, "CascadiaMono.ttf"), 15), (0, 200, 0))
        blit_text(self.screen, "Yellow = {}".format(self.yellow), (self.yellowButton.rect.centerx, self.yellowButton.rect.top - 20), pygame.font.Font(os.path.join(self.fontDir, "CascadiaMono.ttf"), 15), (255, 255, 100))
        blit_text(self.screen, "Purple = {}".format(self.purple), (self.purpleButton.rect.centerx, self.purpleButton.rect.top - 20), pygame.font.Font(os.path.join(self.fontDir, "CascadiaMono.ttf"), 15), (255, 100, 255))

        blit_text(self.screen, f"${self.cash}", (0, 760), pygame.font.Font(os.path.join(self.fontDir, "ImprintMT.ttf"), 40), (0, 150, 0))
        
        # Sounds
        if self.rainSoundPlaying == False:
            self.rainChannel.play(self.rainSound, -1)
            self.rainChannel.set_volume(0.3)
            self.rainSoundPlaying = True
        else:
            pass
        
        if self.chatterSoundPlaying == False:
            self.chatterChannel.play(self.chatterSound, -1)
            self.chatterChannel.set_volume(1.0)
            self.chatterSoundPlaying = True
        else:
            pass
        
        self.musicPlayer.play()
        self.musicPlayer.displayCurrentSong(self.screen, os.path.join(self.fontDir, "Bell.ttf"), 20, (255, 255, 255), 0, 0)

        pygame.display.flip()
        self.clock.tick(60)
    
    def gameOver(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.delSig = True
        self.screen.fill((0, 0, 0))

        blit_text(self.screen, "You are now unemployed\n(Back to working at McDonald's)\nPress R to restart", (0, 0), pygame.font.Font(os.path.join(self.fontDir, "Bell.ttf"), 60), (255, 0, 0))

        pygame.display.flip()
        self.clock.tick(60)
        
    def manager(self):
        if self.state == "menu":
            self.mainMenu()
        elif self.state == "tutorial":
            self.controlScreen()
        elif self.state == "level":
            self.level()
        elif self.state == "gameover":
            self.gameOver()

Session = Game()
while True:
    Session.manager()
    if Session.delSig == True:
        Session = Game()