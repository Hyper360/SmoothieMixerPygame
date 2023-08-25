import pygame


class Button():
    def __init__(self, screen, x, y, width, height, img = None, spritesheet = None, text = "Enter text here", font = None, fontSize = 10, color = (255, 255, 255), bck = (0, 0, 0)):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text = text
        self.font = font
        self.img = img
        self.spritesheet = spritesheet
        self.pressed = [False, False]
        self.prev_mouse_pressed = [False, False]

        if self.img != None:
            self.imgSurface = pygame.image.load(self.img)
            self.imgRect = self.imgSurface.get_rect()
            self.imgRect.center = self.rect.center
        
        if self.spritesheet != None:
            self.spritesheet.x = self.x
            self.spritesheet.y = self.y

        self.fontSurface = pygame.font.Font(self.font, fontSize)
        self.fontTextSurface = self.fontSurface.render(self.text, True, color)
        self.fontTextRect = self.fontTextSurface.get_rect()
        self.fontTextRect.center = self.rect.center
        
        self.bckColor = bck

    def checkClicked(self):
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            if mouse_pressed[0] == True and not self.prev_mouse_pressed[0]:
                self.pressed[0] = True
            else:
                self.pressed[0] = False

            if mouse_pressed[2] == True and not self.prev_mouse_pressed[1]:
                self.pressed[1] = True
            else:
                self.pressed[1] = False
        else:
            self.pressed = [False, False]
                
        self.prev_mouse_pressed = [mouse_pressed[0], mouse_pressed[2]]
        
        return self.pressed
        
    def refreshText(self, text = None, color = (255, 255, 255)):
        if text == None:
            text = self.text
        self.fontTextSurface = self.fontSurface.render(text, True, color)
        self.fontTextRect = self.fontTextSurface.get_rect()
        self.fontTextRect.center = self.rect.center

    def draw(self, curTime = 0):
        self.checkClicked()
        pygame.draw.rect(self.screen, self.bckColor, self.rect, border_radius=5)
        if self.img != None:
            self.screen.blit(self.imgSurface, self.imgRect)
        if self.spritesheet != None:
            self.spritesheet.update(curTime)
        self.screen.blit(self.fontTextSurface, self.fontTextRect)