import pygame
import os

class MusicPlayer():
    def __init__(self, musicDir, volume):
        self.musiclist = [] 
        for song in os.listdir(musicDir):
            self.musiclist.append(os.path.join(musicDir, song))
        self.musicInd = 0
        self.curSong = None
        pygame.mixer.music.set_volume(volume)
    
    def play(self):
        if pygame.mixer.music.get_busy() != True:
            if self.musicInd < len(self.musiclist) - 1:
                self.musicInd += 1
            else:
                self.musicInd = 0
            pygame.mixer.music.unload()
            pygame.mixer.music.load(self.musiclist[self.musicInd])
            pygame.mixer.music.play()
            
        else:
            pass
        
        self.curSong = self.musiclist[self.musicInd]
    
    def skip(self):
        if pygame.mixer.music.get_busy() == True:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            self.play()
        else:
            pass
    
    def displayCurrentSong(self, screen, font, fontSize, fontColor, x, y):
        font = pygame.font.Font(font, fontSize)

        filePath = os.path.basename(self.curSong)
        fileName = os.path.splitext(filePath)[0]

        fontSurface = font.render(fileName, True, fontColor)
        screen.blit(fontSurface, (x, y))
