import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Firework class
class Firework(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = random.uniform(5, 10)
        self.angle = random.uniform(0, 2 * math.pi)

    def update(self):
        self.rect.x += self.speed * 2 * math.cos(self.angle)
        self.rect.y += self.speed * 2 * math.sin(self.angle)
        self.speed -= 0.2

# Text class for dynamic text animation
class AnimatedText(pygame.sprite.Sprite):
    def __init__(self, x, y, message, font, colors):
        super().__init__()
        self.font = font
        self.colors = colors
        self.image = self.render_text(message, self.colors[0])
        self.rect = self.image.get_rect(center=(x, y))
        self.color_index = 0
        self.timer = FPS * 2  # Change color every 2 seconds

    def render_text(self, message, color):
        return self.font.render(message, True, color)

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.timer = FPS * 2
            self.color_index = (self.color_index + 1) % len(self.colors)
            self.image = self.render_text(text_message, self.colors[self.color_index])

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("New Year Fireworks")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Fireworks and Text groups
fireworks = pygame.sprite.Group()
animated_text = pygame.sprite.Group()

# Font
font = pygame.font.Font(None, 36)

# Animated Text variables
text_message = "The year 2023 has come to an end. Welcome to 2024."
text_colors = [WHITE, RED, GREEN, BLUE, YELLOW]
text_sprite = AnimatedText(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, text_message, font, text_colors)
animated_text.add(text_sprite)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Generate random fireworks
    if random.random() < 0.05:
        firework = Firework(random.randint(50, SCREEN_WIDTH - 50), SCREEN_HEIGHT, random.choice([RED, GREEN, BLUE, YELLOW]))
        fireworks.add(firework)

    # Update fireworks
    fireworks.update()

    # Draw background
    screen.fill(BLACK)

    # Draw fireworks
    fireworks.draw(screen)

    # Remove off-screen fireworks
    for firework in fireworks.copy():
        if firework.rect.bottom < 0:
            fireworks.remove(firework)

    # Update and draw the animated text
    animated_text.update()
    animated_text.draw(screen)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
