import pygame
import sys
import os

# Inicijalizacija
pygame.init()
pygame.mixer.init()

# Ekran
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
pygame.display.set_caption("Prototype")

# Boje - promenljive verovatno cemo traziti tacno koje boje su nam potrebene
blue = (0, 0, 128)
red = (192, 10, 0)
black = (0, 0, 0)
white = (255, 255, 255)
grey_56 = (143, 143, 143, 32)
grey_33 = (120, 120, 120)

# Desired paths
current_dir = os.path.dirname(__file__)
font_path = os.path.join(current_dir, 'Assets', 'Fonts', 'minecraftia', 'Minecraftia-Regular.ttf')
sound_one_path = os.path.join(current_dir, 'Assets', 'Soundtrack', 'faza1_fotelja', 'popravka_kauca.mp3')

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

        # Start button
        start_button = pygame.Rect(width / 2 - 150, height / 2 - 80, 300, 50)
        pygame.draw.rect(screen, grey_56, start_button)
        draw_text('Start Game', small_font, white, screen, width / 2, height / 2 - 50)

        # Instructions button
        instructions_button = pygame.Rect(width / 2 - 150, height / 2 + 25, 300, 50)
        pygame.draw.rect(screen, grey_56, instructions_button)
        draw_text('Instructions', small_font, white, screen, width / 2, height / 2 + 50)

        # Quit button
        quit_button = pygame.Rect(width / 2 - 150, height / 2 + 125, 300, 50)
        pygame.draw.rect(screen, grey_56, quit_button)
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
    player_size = 150
    player_x = width // 4
    player_y = height // 4
    player_speed = 20
    running = True

    # macka
    cat1 = pygame.image.load('Assets/Character/cat1.png').convert_alpha()
    cat2 = pygame.image.load('Assets/Character/bad_cat1.png').convert_alpha()
    cat1 = pygame.transform.scale(cat1, (50, 50))
    cat2 = pygame.transform.scale(cat2, (50, 50))
    cat_frames = [cat1, cat2]
    cat_frame_index = 0
    last_switch = pygame.time.get_ticks()
    switch_interval = 300  # milisekundi

    # karakter slike
    hero_idle = pygame.image.load('Assets/Character/hero.png').convert_alpha()
    hero_idle = pygame.transform.scale(hero_idle, (player_size, player_size))

    hero_walk = {
        "left": [pygame.image.load('Assets/Character/hero_left.png').convert_alpha(),
                 pygame.image.load('Assets/Character/hero_left_step.png').convert_alpha()],
        "right": [pygame.image.load('Assets/Character/hero_right.png').convert_alpha(),
                  pygame.image.load('Assets/Character/hero_right_step.png').convert_alpha()],
        "up": [pygame.image.load('Assets/Character/hero_back.png').convert_alpha(),
               pygame.image.load('Assets/Character/hero_back_step.png').convert_alpha()],
        "down": [pygame.image.load('Assets/Character/hero.png').convert_alpha(),
                 pygame.image.load('Assets/Character/hero_step.png').convert_alpha()]
    }

    for direction in hero_walk:
        hero_walk[direction] = [pygame.transform.scale(img, (player_size, player_size)) for img in hero_walk[direction]]

    hero_direction = "down"
    frame_index = 0
    last_frame_switch = pygame.time.get_ticks()
    frame_interval = 200

    while running:
        screen.fill(black)

        # Mapa
        map = pygame.image.load('Assets/Map/mapa.png')
        map = pygame.transform.scale(map, (4 / 3 * height, height))
        maprect = map.get_rect()
        maprect.center = (width // 2, height // 2)
        screen.blit(map, maprect)

        # Pravougaonici koji predstavljaju prostorije i hodnike
        rooms = [
            pygame.Rect(450 / 1920 * width, 370 / 1440 * height, 280 /  1920 * width, 100 / 1440 * height),  # Prostorija 1
            pygame.Rect(850 / 1920 * width, 370 / 1440 * height, 5 / 1920 * width, 5 / 1440 * height) ,       # hodnik
            pygame.Rect(950 / 1920 * width, 370 / 1440 * height, 530 / 1920 * width, 20 / 1440 * height),  # Prostorija 2
            pygame.Rect(1430 / 1920 * width, 600 / 1440 * height, 5 / 1920 * width, 380 / 1440 * height),    # stepenište
            pygame.Rect(1280 / 1920 * width, 1100 / 1440 * height, 240 / 1920 * width, 20 / 1440 * height),  # Prostorija 3
            pygame.Rect(1100 / 1920 * width, 1095 / 1440 * height, 50 / 1920 * width, 5 / 1440 * height) ,       # hodnik
            pygame.Rect(700 / 1920 * width, 1095 / 1440 * height, 250 / 1920 * width, 20 / 1440 * height),  # Prostorija 4
            pygame.Rect(600 / 1920 * width, 1095 / 1440 * height, 10 / 1920 * width, 5 / 1440 * height) ,       # hodnik
            pygame.Rect(400 / 1920 * width, 1095 / 1440 * height, 80 / 1920 * width, 20 / 1440 * height),  # Prostorija 5
        ]


        def is_in_room(x, y, size):
            player_rect = pygame.Rect(x, y, size, size)
            return any(room.colliderect(player_rect) for room in rooms)


        # Animacija mačke
        current_time = pygame.time.get_ticks()
        if current_time - last_switch >= switch_interval:
            cat_frame_index = (cat_frame_index + 1) % len(cat_frames)
            last_switch = current_time
        screen.blit(cat_frames[cat_frame_index], (width // 4 - 53, height // 4 - 50))

        # Ulaz i pomeranje
        keys = pygame.key.get_pressed()
        moving = False

        new_x, new_y = player_x, player_y

        if keys[pygame.K_LEFT]:
            new_x -= player_speed
            hero_direction = "left"
            moving = True
        elif keys[pygame.K_RIGHT]:
            new_x += player_speed
            hero_direction = "right"
            moving = True
        elif keys[pygame.K_UP]:
            new_y -= player_speed
            hero_direction = "up"
            moving = True
        elif keys[pygame.K_DOWN]:
            new_y += player_speed
            hero_direction = "down"
            moving = True

        if is_in_room(new_x, new_y, player_size):
            player_x, player_y = new_x, new_y

        # Granice
        #player_x = max(0, min(width - player_size, player_x))
        #player_y = max(0, min(height - player_size, player_y))

        # Hero animacija
        if moving:
            now = pygame.time.get_ticks()
            if now - last_frame_switch > frame_interval:
                frame_index = (frame_index + 1) % 2
                last_frame_switch = now
            hero_img = hero_walk[hero_direction][frame_index]
        else:
            hero_img = hero_idle

        screen.blit(hero_img, (player_x, player_y))

        # Eventi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        '''
        for room in rooms:
            pygame.draw.rect(screen, (0, 255, 0), room, 2)  # Zeleni obrubi
        '''


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
