import pygame
import random

# MIT No Attribution
#
# Copyright 2023 Andru Jorj
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to 
# deal in the Software without restriction, including without limitation the 
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
# sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
# THE SOFTWARE.

# Game Initialization
pygame.init()
WIDTH, HEIGHT = 300, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dice")

# Colors
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (150, 150, 150)
BUTTON_HOVER_COLOR = (200, 200, 200)
BUTTON_PRESSED_COLOR = (80, 80, 80)

# Font
FONT = pygame.font.SysFont("Sans", 25)

# Dice Constants
DICE_SIZE = 210
DOT_RADIUS = 20
DOT_OFFSET = 50
DOT_SPACING = 26

# Animation Constants
ROLL_FRAMES = 400
FRAME_DELAY = 400

# Sound
rolling_sound = pygame.mixer.Sound("roll_sound.wav")

# Game State
dice_value = None
rolling = False
roll_frame = 0
button_pressed = False

# Roll the dice function
def roll_dice():
    global dice_value, rolling, roll_frame
    dice_value = random.randint(1, 6)
    rolling = True
    roll_frame = 100
    rolling_sound.play()  # Play the rolling sound

# Create a button class
class Button:
    def __init__(self, x, y, width, height, text, text_color, bg_color, hover_color, pressed_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.action = action
        self.is_hovered = False
        self.is_pressed = False

    def draw(self):
        if self.is_pressed:
            color = self.pressed_color
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.bg_color

        pygame.draw.rect(screen, color, self.rect)
        text_surface = FONT.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.is_hovered = True
            else:
                self.is_hovered = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.rect.collidepoint(event.pos):
                self.is_pressed = False
                self.action()
            else:
                self.is_pressed = False

# Create the roll button
button_width = 130
button_height = 30
button_x = (WIDTH - button_width) // 2
button_y = HEIGHT - 40
roll_button = Button(button_x, button_y, button_width, button_height, "Roll", BLACK, BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_PRESSED_COLOR, roll_dice)

# Game Loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        roll_button.handle_event(event)

    # Clear the screen
    screen.fill(GRAY)

    if roll_button.is_pressed and not rolling:
        roll_dice()

    if rolling:
        # Animation: Rolling the dice
        roll_frame += 1
        if roll_frame > ROLL_FRAMES:
            rolling = False

    # Draw the dice box
    dice_rect = pygame.Rect(WIDTH // 2 - DICE_SIZE // 2, HEIGHT // 2 - DICE_SIZE // 2, DICE_SIZE, DICE_SIZE)
    pygame.draw.rect(screen, WHITE, dice_rect)

    # Draw the dots on the dice
    if dice_value is not None:
        dot_color = BLACK
        dot_positions = {
            1: [(WIDTH // 2, HEIGHT // 2)],
            2: [(WIDTH // 2 - DOT_OFFSET, HEIGHT // 2 - DOT_OFFSET),
                (WIDTH // 2 + DOT_OFFSET, HEIGHT // 2 + DOT_OFFSET)],
            3: [(WIDTH // 2 - DOT_OFFSET, HEIGHT // 2 - DOT_OFFSET),
                (WIDTH // 2, HEIGHT // 2),
                (WIDTH // 2 + DOT_OFFSET, HEIGHT // 2 + DOT_OFFSET)],
            4: [(WIDTH // 2 - DOT_OFFSET, HEIGHT // 2 - DOT_OFFSET),
                (WIDTH // 2 + DOT_OFFSET, HEIGHT // 2 - DOT_OFFSET),
                (WIDTH // 2 - DOT_OFFSET, HEIGHT // 2 + DOT_OFFSET),
                (WIDTH // 2 + DOT_OFFSET, HEIGHT // 2 + DOT_OFFSET)],
            5: [(WIDTH // 2 - DOT_OFFSET, HEIGHT // 2 - DOT_OFFSET),
                (WIDTH // 2 + DOT_OFFSET, HEIGHT // 2 - DOT_OFFSET),
                (WIDTH // 2, HEIGHT // 2),
                (WIDTH // 2 - DOT_OFFSET, HEIGHT // 2 + DOT_OFFSET),
                (WIDTH // 2 + DOT_OFFSET, HEIGHT // 2 + DOT_OFFSET)],
            6: [(WIDTH // 2 - DOT_OFFSET, HEIGHT // 2 - DOT_OFFSET - DOT_SPACING),
                (WIDTH // 2 + DOT_OFFSET, HEIGHT // 2 - DOT_OFFSET - DOT_SPACING),
                (WIDTH // 2 - DOT_OFFSET, HEIGHT // 2),
                (WIDTH // 2 + DOT_OFFSET, HEIGHT // 2),
                (WIDTH // 2 - DOT_OFFSET, HEIGHT // 2 + DOT_OFFSET + DOT_SPACING),
                (WIDTH // 2 + DOT_OFFSET, HEIGHT // 2 + DOT_OFFSET + DOT_SPACING)]
        }

        # Draw the dots based on the dice value
        for pos in dot_positions[dice_value]:
            pygame.draw.circle(screen, dot_color, pos, DOT_RADIUS)

    # Draw the roll button
    roll_button.draw()

    # Update the display
    pygame.display.flip()

# Game Cleanup
pygame.quit()

