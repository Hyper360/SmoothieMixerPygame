import pygame

def blit_text(surface, text, pos, font, color=pygame.Color(255, 255, 255)):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        #Color changing mid-sentence brought to you by Chat-GPT!!!
        for word in line:
            if "<red>" in word:
                word = word.replace("<red>", "") #Replacing the word <red> with empty string
                word_surface = font.render(word, 0, pygame.Color(255, 0, 0))  # Render the word in red seperate.
            elif "<yellow>" in word:
                word = word.replace("<yellow>", "") #Replacing the word <red> with empty string
                word_surface = font.render(word, 0, pygame.Color(255, 255, 0))  # Render the word in red seperate.
            elif "<blue>" in word:
                word = word.replace("<yellow>", "") #Replacing the word <red> with empty string
                word_surface = font.render(word, 0, pygame.Color(0, 0, 255))  # Render the word in red seperate.
            else:
                word_surface = font.render(word, 0, color)  # Render the word with the default color.
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.