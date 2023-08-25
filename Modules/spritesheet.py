import pygame

class Timer():
    def __init__(self, time):
        self.called = pygame.time.get_ticks()
        self.time = time
        self.signal = False
    
    def reset(self, current_time):
        self.signal = False
        self.called = current_time

    def update(self, current_time):
        if current_time - self.called >= self.time:
            self.signal = True
            self.called = current_time

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, color, scale):
        image = pygame.Surface((width, height))
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image
    

class SpritesheetRenderer():
    def __init__(self, screen, x, y, width, height, framewidth, frameheight, frames, file, speed, scale):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.file = file
        self.speed = speed
        self.frameNum = frames
        self.curFrame = 0
        self.animationFrames = []
        self.timer = Timer(self.speed)
        self.imageSurface = pygame.transform.scale(pygame.image.load(file), (width, height))
        self.spritesheet = SpriteSheet(self.imageSurface)

        for i in range(frames):
            self.animationFrames.append(self.spritesheet.get_image(i, framewidth, frameheight, (0, 0, 0), scale))
    
    
    def update(self, curTime):
        self.timer.update(curTime)
        if self.timer.signal:
            self.curFrame += 1
            if self.curFrame > len(self.animationFrames) - 1:
                self.curFrame = 0
            self.timer.reset(curTime)

        self.screen.blit(self.animationFrames[self.curFrame], (self.x, self.y))
        