import pygame
import sys
import os

# Inicijalizacija
pygame.init()

# Ekran
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
pygame.display.set_caption("Prototype")

# Boje - promenljive verovatno cemo traziti tacno koje boje su nam potrebene
blue = (0, 0, 128)
red = (192, 10, 0)
black = (0, 0, 0)
white = (255, 255, 255)

# Font
# Treba se odluchiti za font moj trenutni predlog (Aurora by StorytypeStudio ili neki drugi to cemo i Marka da pitamo)
current_dir = os.path.dirname(__file__)
font_path = os.path.join(current_dir, 'Assets', 'Fonts', 'deutsch_gothic', 'Deutsch.ttf')

try:
    font = pygame.font.Font(font_path, 74)
    small_font = pygame.font.Font(font_path, 36)
except pygame.error as e:
    print(f"Error loading font: {e}")
    # Fallback to default font
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)


# Glavni izbornik funkcije
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


def main_menu():
    while True:
        screen.fill(black)
        draw_text('Main Menu', font, white, screen, width / 2, height / 2 - 175)

        # Buttons
        start_button = pygame.Rect(width / 2 - 100, height / 2 - 75, 200, 50)
        pygame.draw.rect(screen, red, start_button)
        draw_text('Start Game', small_font, white, screen, width / 2, height / 2 - 50)

        instructions_button = pygame.Rect(width / 2 - 100, height / 2 + 25, 200, 50)
        pygame.draw.rect(screen, red, instructions_button)
        draw_text('Instructions', small_font, white, screen, width / 2, height / 2 + 50)

        quit_button = pygame.Rect(width / 2 - 100, height / 2 + 125, 200, 50)
        pygame.draw.rect(screen, red, quit_button)
        draw_text('Quit', small_font, white, screen, width / 2, height / 2 + 150)

        mx, my = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if start_button.collidepoint((mx, my)):
            if click:
                game()
        if instructions_button.collidepoint((mx, my)):
            if click:
                instructions()
        if quit_button.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        pygame.display.flip()


def game():
    # Originalni kvadrat
    player_size = 50
    player_x = width // 2
    player_y = height // 2
    player_speed = 5
    running = True

    while running:
        screen.fill(blue)
        pygame.draw.rect(screen, red, (player_x, player_y, player_size, player_size))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed

        player_x = max(0, min(width - player_size, player_x))
        player_y = max(0, min(height - player_size, player_y))

        pygame.display.flip()
        pygame.time.delay(30)


def instructions():
    while True:
        screen.fill(black)
        draw_text('Instructions', font, white, screen, width / 2, 100)
        draw_text('Use arrow keys to move the square', small_font, white, screen, width / 2, 200)
        draw_text('Press ESC to return to menu', small_font, white, screen, width / 2, 250)

        back_button = pygame.Rect(width / 2 - 100, 350, 200, 50)
        pygame.draw.rect(screen, red, back_button)
        draw_text('Back', small_font, white, screen, width / 2, 375)

        mx, my = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if back_button.collidepoint((mx, my)):
            if click:
                break

        pygame.display.flip()


main_menu()
