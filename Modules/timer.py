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