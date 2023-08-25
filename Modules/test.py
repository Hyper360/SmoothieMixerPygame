import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sprite Example")

# Define a basic sprite class
class MySprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        pass

# Create sprite instances
sprite1 = MySprite(100, 100)
sprite2 = MySprite(200, 200)

# Create a sprite group and add sprites to it
all_sprites = pygame.sprite.Group()
all_sprites.add(sprite1, sprite2)

# Main loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update sprites
    all_sprites.update()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw sprites
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
