from random import randint
import pygame
import ctypes
import math
import os


# Window Properties

class system:
    
    try:
        user32 = ctypes.windll.user32
        WINDOW_WIDTH, WINDOW_HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    except:
        WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720  

    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Swarm")

    FPS = 60
    CLOCK = pygame.time.Clock()

    pygame.font.init()
    score_font = pygame.font.Font(os.path.join("assets", "images", "8bit.TTF"), 30) 


# Environment Properties

    GROUND_WIDTH, GROUND_HEIGHT = WINDOW_WIDTH + 200, 204
    GROUND_X, GROUND_Y = -100, WINDOW_HEIGHT - 75
    ground = pygame.Rect(GROUND_X, GROUND_Y, GROUND_WIDTH, GROUND_HEIGHT)

    P_WIDTH, P_HEIGHT = (math.floor(WINDOW_WIDTH / 2.833) + 100), math.floor(WINDOW_HEIGHT / 12)
    P1_X, P_Y = -100, (math.floor(WINDOW_HEIGHT / 1.8))
    platform1 = pygame.Rect(P1_X, P_Y, P_WIDTH, P_HEIGHT)

    P2_X = (WINDOW_WIDTH - P_WIDTH) + 100
    platform2 = pygame.Rect(P2_X, P_Y, P_WIDTH, P_HEIGHT)

    P3_WIDTH = math.floor(WINDOW_WIDTH / 2.833)
    P3_X, P3_Y = (WINDOW_WIDTH - P3_WIDTH) // 2, (math.floor(WINDOW_HEIGHT / 3.6))
    platform3 = pygame.Rect(P3_X, P3_Y, P3_WIDTH, P_HEIGHT)

    PLATFORMS = [ground, platform1, platform2, platform3]


# Assets

    COLORS = {"WHITE": (255, 255, 255), "BLACK": (0, 0, 0), "RED": (255, 0, 0), "GREEN": (0, 255, 0), "BLUE": (0, 0, 255), "DARK RED": (150, 0, 0)}
    BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "background.png")), (2000, 2000))

    ENEMY_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "enemy.png")), (math.floor(WINDOW_WIDTH / 20.25), math.floor(WINDOW_HEIGHT / 6.25)))

    BULLET_WIDTH, BULLET_HEIGHT = 40, 5
    BULLET_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "bullet.png")), (BULLET_WIDTH, BULLET_HEIGHT))

    GROUND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "platform2.png")), (GROUND_WIDTH, GROUND_HEIGHT))
    PLATFORM_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "platform2.png")), (P_WIDTH, P_HEIGHT))

    BUTTON_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "button.png")), (800, 100))


# Player Properties

class player:
    
    def __init__(self):

        self.ingame = False

        self.SPEED  = math.floor(system.WINDOW_WIDTH / 170)
        self.BULLET_SPEED = math.floor(system.WINDOW_WIDTH / 68)

        RECT_WIDTH, RECT_HEIGHT = math.floor(system.WINDOW_WIDTH / 80.952), math.floor(system.WINDOW_HEIGHT / 6.25)
        self.RECT_X, self.RECT_Y = system.WINDOW_WIDTH // 2, system.WINDOW_HEIGHT // 2

        self.rect = pygame.Rect(self.RECT_X, self.RECT_Y, RECT_WIDTH, RECT_HEIGHT)

        self.face = True
        self.jump_counter = 0

        self.kills = 0
        self.max_bullets = 1
        self.bullets = []

        self.score = 0
        
        IMAGE1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "player1.png")), (RECT_WIDTH * 4, RECT_HEIGHT))
        IMAGE2 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "player2.png")), (RECT_WIDTH * 4, RECT_HEIGHT))
        IMAGE3 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "player3.png")), (RECT_WIDTH * 4, RECT_HEIGHT))
        IMAGE4 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "player4.png")), (RECT_WIDTH * 4, RECT_HEIGHT))
        IMAGE5 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "player5.png")), (RECT_WIDTH * 4, RECT_HEIGHT))
        
        self.image_num = 4
        self.IMAGES = [IMAGE1, IMAGE2, IMAGE3, IMAGE4, IMAGE5, ]


# Defining Primary Functions

def game_over(character):

    character.max_bullets = 1
    character.rect.x, character.rect.y = character.RECT_X, character.RECT_Y

    mouse_over = 0
    
    with open("score.txt", "r+") as score_file:
        highscore = int(score_file.readline().strip())

        if highscore < character.score:

            score_file.seek(0)
            score_file.truncate()

            score_file.write(f"{character.score}")
            highscore = character.score

    system().WINDOW.fill(system().COLORS["WHITE"])
    
    title_font = pygame.font.Font(os.path.join("assets", "images", "8bit.TTF"), 80) 
    title = title_font.render("GAME OVER", False, system().COLORS["DARK RED"])
    system().WINDOW.blit(title, (math.floor((system.WINDOW_WIDTH / 2) - 350), math.floor(system.WINDOW_HEIGHT / 5.142)))

    score_text = system().score_font.render(f"Score  {character.score}", False, system().COLORS["BLACK"])
    system().WINDOW.blit(score_text, (math.floor(system.WINDOW_WIDTH / 2.46), math.floor(system.WINDOW_HEIGHT / 3.1)))

    highscore_text = system().score_font.render(f"Highscore  {highscore}", False, system().COLORS["BLACK"])
    system().WINDOW.blit(highscore_text, (math.floor(system.WINDOW_WIDTH / 2.46), math.floor(system.WINDOW_HEIGHT / 2.6))) #585, 325

    BUTTON_WIDTH = 800
    BUTTON_HEIGHT = 100
    BUTTON_X = math.floor((system.WINDOW_WIDTH / 2) - (BUTTON_WIDTH / 2))

    button1 = pygame.Rect(BUTTON_X, math.floor(system.WINDOW_HEIGHT / 2.25), BUTTON_WIDTH, BUTTON_HEIGHT)
    button2 = pygame.Rect(BUTTON_X, math.floor(system.WINDOW_HEIGHT / 1.5), BUTTON_WIDTH, BUTTON_HEIGHT)

    button_font = pygame.font.Font(os.path.join("assets", "images", "8bit.TTF"), 40)

    system().WINDOW.blit(system().BUTTON_IMAGE, (button1.x, button1.y))
    system().WINDOW.blit(system().BUTTON_IMAGE, (button2.x, button2.y))

    button1_text = button_font.render("Play", False, system().COLORS["WHITE"])
    system().WINDOW.blit(button1_text, (math.floor(system.WINDOW_WIDTH / 2.2), math.floor(system.WINDOW_HEIGHT / 2.11)))

    button2_text = button_font.render("Exit", False, system().COLORS["WHITE"])
    system().WINDOW.blit(button2_text, (math.floor(system.WINDOW_WIDTH / 2.2), math.floor(system.WINDOW_HEIGHT / 1.44)))
        
    pygame.display.update()

    character.score = 0
    while not character.ingame:
        system().CLOCK.tick(system().FPS)

        mx, my = pygame.mouse.get_pos()

        if button1.collidepoint((mx, my)):
            mouse_over = 1
        elif button2.collidepoint((mx, my)):
            mouse_over = 2
        else:
            mouse_over = 0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

                if event.key == pygame.K_RETURN:
                    character.ingame = True

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1 and mouse_over == 1:
                    character.ingame = True
                elif event.button == 1 and mouse_over == 2:
                    pygame.quit()

    game(character)


def draw(character, enemies, platforms, time):

    system().WINDOW.blit(system().BACKGROUND, (0, 0))

    score_text = system().score_font.render(f"Score  {character.score}", False, system().COLORS["WHITE"])
    system().WINDOW.blit(score_text, (2, 0))

    for bullet in character.bullets:
        system().WINDOW.blit(system().BULLET_IMAGE, (bullet[0].x, bullet[0].y))

    for platform in platforms:
        system().WINDOW.blit(pygame.transform.scale(system().PLATFORM_IMAGE, (platform.width, platform.height)), (platform.x, platform.y))

    for enemy in enemies:

        if enemy[1]:
            system().WINDOW.blit(system().ENEMY_IMAGE, (enemy[0].x, enemy[0].y))
        else:
            system().WINDOW.blit(pygame.transform.flip(system().ENEMY_IMAGE, True, False), (enemy[0].x, enemy[0].y))

    if not character.face:
        system().WINDOW.blit(pygame.transform.flip(character.IMAGES[character.image_num], True, False), (character.rect.x - (character.rect.width * 3), character.rect.y), )
    else:
        system().WINDOW.blit(character.IMAGES[character.image_num], (character.rect.x, character.rect.y), )

    pygame.display.update()


def handle_enemies(enemies, character, platforms):

    for n in enemies:
        
        enemy = n[0]
        platform_y = [n.y for n in platforms if enemy.x + enemy.width > n.x and enemy.x < n.x + n.width and n.y >= enemy.y + enemy.height]

        try:
            min_y = min(platform_y)
        except ValueError:
            min_y = 825 

        if enemy.y + enemy.height + character.SPEED <= min_y:    
            enemy.y += character.SPEED
        elif enemy.y + enemy.height < min_y:
            enemy.y += 1

        if character.rect.x < enemy.x:    # LEFT

            enemy.x -= math.floor(system.WINDOW_WIDTH / 425)
            n[1] = False

        if character.rect.x > enemy.x:    # RIGHT

            enemy.x += math.floor(system.WINDOW_WIDTH / 425)
            n[1] = True

        if enemy.colliderect(character):

            character.ingame = False
            game_over(character)

        for bullet in character.bullets:

            if enemy.colliderect(bullet[0]):

                character.bullets.remove(bullet)
                enemies.remove(n)
                
                character.kills += 1
                character.score += 50


def produce_enemies(num, character):

    enemies = []

    positions = {1: (-20, system.WINDOW_HEIGHT // 1.4), 2: (system().WINDOW_WIDTH + 20, system.WINDOW_HEIGHT // 1.4), 
    3: (-20, system.WINDOW_HEIGHT // 2.571), 4:(system().WINDOW_WIDTH + 20, system.WINDOW_HEIGHT // 2.571), 5: (system().WINDOW_WIDTH // 2, -70)}

    for n in range(0, num):

        position = positions[randint(1, 5)]
        enemies.append([pygame.Rect(position[0], position[1], character.rect.width, character.rect.height), True])

    num = randint(num, math.floor(num * 1.5))

    return enemies
    

def player_movement(keys, character, platforms):

    platform_y = [n.y for n in platforms if character.rect.x + character.rect.width > n.x and character.rect.x < n.x + n.width and n.y >= character.rect.y + character.rect.height]
    min_y = min(platform_y)

    if character.rect.y + character.rect.height + character.SPEED <= min_y:    
        character.rect.y += character.SPEED
    elif character.rect.y + character.rect.height < min_y:
        character.rect.y += 1

    if keys[pygame.K_a] and character.rect.x - character.SPEED >= 0 or keys[pygame.K_LEFT] and character.rect.x - character.SPEED >= 0:    # LEFT

        character.rect.x -= character.SPEED
        character.face = False

    if keys[pygame.K_d] and character.rect.x + character.SPEED <= system().WINDOW_WIDTH - character.rect.width or keys[pygame.K_RIGHT] and character.rect.x - character.SPEED >= 0:    # RIGHT

        character.rect.x += character.SPEED
        character.face = True

    if character.jump_counter > 0:

        n = system.WINDOW_HEIGHT / 7200
        character.rect.y -= (character.jump_counter ** 2) * n


def handle_bullets(character):

    for bullet in character.bullets:

        if bullet[1]:

            if bullet[0].x > system().WINDOW_WIDTH + 5:
                character.bullets.remove(bullet)
            else:
                bullet[0].x += character.BULLET_SPEED

        else:
            if bullet[0].x < -5:
                character.bullets.remove(bullet)
            else:
                bullet[0].x -= character.BULLET_SPEED


def game(character):

    SPAWN_ENEMIES = True

    platforms = system().PLATFORMS
    enemies = []

    if SPAWN_ENEMIES:
        enemies = produce_enemies(3, character)

    time = 60

    character.ingame = True
    while character.ingame:
        system().CLOCK.tick(system().FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                character.ingame = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    character.ingame = False

                if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:

                    for platform in platforms:

                        if character.rect.y + character.rect.height == platform.y:
                           character.jump_counter = 23

                if event.key == pygame.K_LSHIFT and len(character.bullets) < character.max_bullets or event.key == pygame.K_RSHIFT and len(character.bullets) < character.max_bullets:
                    
                    bullet = pygame.Rect(character.rect.x, character.rect.y + character.rect.height/2 - 15, 10, 5)

                    if character.face != False:
                        character.bullets.append((bullet, True))
                    else:
                        character.bullets.append((bullet, False))


            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pressed()

                if mouse[0] and len(character.bullets) < character.max_bullets:
                    
                    bullet = pygame.Rect(character.rect.x, character.rect.y + character.rect.height/2 - 15, 10, 5)

                    if character.face != False:
                        character.bullets.append((bullet, True))
                    else:
                        character.bullets.append((bullet, False))

        keys = pygame.key.get_pressed()
        handle_enemies(enemies, character, platforms)
        
        spawn_num = 900 - (character.score // 50)
        num = randint(1, 900)
        if num >= spawn_num and SPAWN_ENEMIES and len(enemies) <= 20:    
            enemies.extend(produce_enemies(1, character))

        if character.kills == 15:
            
            character.kills = 0
            character.max_bullets += 1

        player_movement(keys, character, platforms)
        handle_bullets(character)

        if character.jump_counter > 0:
            character.jump_counter -= 1

        draw(character, enemies, platforms, time)
        
        time -= 1
        if time <= 0:
            time = 60

    pygame.quit()


def main_menu():

    character = player()
    mouse_over = 0

    system().WINDOW.fill(system().COLORS["WHITE"])
    
    title_font = pygame.font.Font(os.path.join("assets", "images", "8bit.TTF"), 80) 
    title = title_font.render("SWARM", False, system().COLORS["BLACK"])
    system().WINDOW.blit(title, (math.floor((system.WINDOW_WIDTH / 2) - 230), math.floor(system.WINDOW_HEIGHT / 5.142)))

    BUTTON_WIDTH = 800
    BUTTON_HEIGHT = 100
    BUTTON_X = math.floor((system.WINDOW_WIDTH / 2) - (BUTTON_WIDTH / 2))

    button1 = pygame.Rect(BUTTON_X, math.floor(system.WINDOW_HEIGHT / 2.25), BUTTON_WIDTH, BUTTON_HEIGHT)
    button2 = pygame.Rect(BUTTON_X, math.floor(system.WINDOW_HEIGHT / 1.5), BUTTON_WIDTH, BUTTON_HEIGHT)

    button_font = pygame.font.Font(os.path.join("assets", "images", "8bit.TTF"), 40)

    system().WINDOW.blit(system().BUTTON_IMAGE, (button1.x, button1.y))
    system().WINDOW.blit(system().BUTTON_IMAGE, (button2.x, button2.y))

    button1_text = button_font.render("Play", False, system().COLORS["WHITE"])
    system().WINDOW.blit(button1_text, (math.floor(system.WINDOW_WIDTH / 2.2), math.floor(system.WINDOW_HEIGHT / 2.11)))

    button2_text = button_font.render("Exit", False, system().COLORS["WHITE"])
    system().WINDOW.blit(button2_text, (math.floor(system.WINDOW_WIDTH / 2.2), math.floor(system.WINDOW_HEIGHT / 1.44)))
        
    pygame.display.update()


    while not character.ingame:
        system().CLOCK.tick(system().FPS)

        mx, my = pygame.mouse.get_pos()

        if button1.collidepoint((mx, my)):
            mouse_over = 1
        elif button2.collidepoint((mx, my)):
            mouse_over = 2
        else:
            mouse_over = 0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

                if event.key == pygame.K_RETURN:
                    character.ingame = True

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1 and mouse_over == 1:
                    character.ingame = True
                elif event.button == 1 and mouse_over == 2:
                    pygame.quit()

    game(character)


# Running the Program

if __name__ == "__main__":
    main_menu()