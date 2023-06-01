# This is a Snake Game made by Rianne Justin Policarpio
# This uses pygame to create a game from scratch

import pygame
import sys
import random
from pygame.math import Vector2
from button import Button
from os import path


class SNAKE:
    def __init__(self, path):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.power_block = False
        self.skin_path = path

        self.head_up = pygame.image.load(self.skin_path + '/head_up.png').convert_alpha()
        self.head_down = pygame.image.load(self.skin_path + '/head_down.png').convert_alpha()
        self.head_right = pygame.image.load(self.skin_path + '/head_right.png').convert_alpha()
        self.head_left = pygame.image.load(self.skin_path + '/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load(self.skin_path + '/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load(self.skin_path + '/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load(self.skin_path + '/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load(self.skin_path + '/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load(self.skin_path + '/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load(self.skin_path + '/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load(self.skin_path + '/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load(self.skin_path + '/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load(self.skin_path + '/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load(self.skin_path + '/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
        self.bonk_sound = pygame.mixer.Sound('Sound/bonk.wav')
        self.timer_sound = pygame.mixer.Sound('Sound/count3.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos,cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index -1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)


    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down


    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        elif self.power_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.power_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def addpower_block(self):
        self.power_block = True

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def play_bonk_sound(self):
        self.bonk_sound.play()

    def play_timer_sound(self):
        self.timer_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)

class FRUIT:
    def __init__(self):
        self.count = 0
        self.banana_timer = 280
        self.timer = 1
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)
        screen.blit(apple, fruit_rect)

    def draw_powerfruit(self):
        power_fruit_rect = pygame.Rect(int(self.pos2.x * cell_size), int(self.pos2.y * cell_size), cell_size, cell_size)
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)
        if self.banana_timer > 0:
            screen.blit(banana, power_fruit_rect)
            self.banana_timer -= 1


    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
        self.x2 = random.randint(0, cell_number - 1)
        self.y2 = random.randint(0, cell_number - 1)
        self.pos2 = Vector2(self.x2, self.y2)
        self.count = self.count + 1

    def timer_reset(self):
        self.count = 1
        self.banana_timer = 280
        self.timer = 1


class MAIN:
    def __init__(self, path):
        self.snake = SNAKE(path)
        self.fruit = FRUIT()
        self.score_int2 = 0

    def load_data(self):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'r+') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        # self.draw_grass()
        self.fruit.draw_fruit()
        if self.fruit.count % 10 == 0:
            if self.fruit.timer == 1:
                self.snake.play_timer_sound()
                self.fruit.timer = 0
            if self.fruit.banana_timer == 0:
                self.fruit.count += 1
                self.fruit.banana_timer = 280
                self.fruit.timer = 1
                self.fruit.pos2 = Vector2(20, 20)
            self.fruit.draw_powerfruit()
        self.snake.draw_snake()
        self.draw_score()
        self.draw_text("High Score: " + str(self.highscore),22, "white", int(cell_size * cell_number - 100), int(25))
        self.draw_text("ESC to Quit", 20, "white", int(75), int(25))

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.score_int2 += 1
            self.fruit.randomize()
            self.snake.add_block()
            self.fruit.banana_timer = 280
            self.fruit.timer = 1
            self.snake.play_crunch_sound()

        if self.fruit.pos2 == self.snake.body[0]:
            self.score_int2 += 3
            self.fruit.randomize()
            self.snake.addpower_block()
            self.fruit.banana_timer = 280
            self.fruit.timer = 1
            self.snake.play_crunch_sound()


        for block in self.snake.body[1:]:
            if block == self.fruit.pos or block == self.fruit.pos2:
                self.fruit.randomize()


    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.check_score()
            self.snake.play_bonk_sound()
            self.score_int2 = 0
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.check_score()
                self.snake.play_bonk_sound()
                self.score_int2 = 0
                self.game_over()

    def check_score(self):
        if self.score_int2 > self.highscore:
            self.highscore = self.score_int2
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score_int2))

    def check_costume(self):
        if self.skin == "default":
            self.latestPath = 'assets/skin_snake/default'
        elif self.skin == "blue":
            self.latestPath  = 'blue'
        else:
            self.latestPath  = 'assets/skin_snake/blue'


    def game_over(self):
        self.fruit.timer_reset()
        self.snake.reset()

    def draw_grass(self):
        grass_color = (145, 70, 59)
        for row in range(cell_number):
         if row % 2 == 0:
            for col in range(cell_number):
                if col % 2 == 0:
                 grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                 pygame.draw.rect(screen, grass_color, grass_rect)
        else:
            for col in range(cell_number):
                if col % 2 != 0:
                    grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        self.score_int = len(self.snake.body) - 3
        score_text = str(self.score_int2)
        score_surface = game_font.render(score_text, True, (56,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56,74,12), bg_rect,2)
        if self.fruit.pos == score_rect or self.fruit.pos == apple_rect or self.fruit.pos == bg_rect:
            self.fruit.randomize()
        for block in bg_rect[:]:
            if block == self.fruit.pos or block == self.fruit.pos2:
                self.fruit.randomize()

    def draw_text(self, text, size, color, x, y):
        text_surface = game_font.render(text, True, (color))
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        screen.blit(text_surface, text_rect)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 30
cell_number = 20
pygame.display.set_caption("Snake Game by Rianne")
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
banana = pygame.image.load('Graphics/banana.png').convert_alpha()
game_font = pygame.font.Font("Font/PoetsenOne-Regular.ttf", 25)
BG = pygame.image.load("assets/Background.png")
BG2 = pygame.image.load("assets/background2.png")
HS_FILE = "higscore.txt"
SKIN_FILE = "skins.txt"


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

def check_costumes():
    with open(path.join(path.dirname(__file__), SKIN_FILE), 'r+') as f:
        try:
            skin = str(f.read())
        except:
            skin = "default"
    if skin == "default":
        return 'Graphics'
    elif skin == "blue":
       return  'assets/skin_snake/blue'
    else:
        return 'Graphics'

def write_costume(string):
    with open(path.join(path.dirname(__file__), SKIN_FILE), 'w') as f:
        f.write(str(string))
    main_menu()


def play():
    main_game = MAIN(check_costumes())
    main_game.load_data()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_ESCAPE:
                    main_game.check_score()
                    main_menu()

        screen.blit(BG2, (0, 0))
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(90)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(20).render("This is the OPTIONS screen.", True, "#b68f40")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(300, 100))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_CHANGE = Button(image=None, pos=(300, 200),
                              text_input="Change Skin", font=get_font(15), base_color="White", hovering_color="#b68f40")

        OPTIONS_BACK = Button(image=None, pos=(300, 300),
                            text_input="BACK", font=get_font(15), base_color="White", hovering_color="#b68f40")

        OPTIONS_CHANGE.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_CHANGE.update(screen)
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_CHANGE.checkForInput(OPTIONS_MOUSE_POS):
                    costume_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def costume_menu():
    while True:
        COSTUME_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(BG, (0, 0))

        COSTUME_TEXT = get_font(20).render("Pick a Skin", True, "#b68f40")
        COSTUME_RECT = COSTUME_TEXT.get_rect(center=(300, 100))
        screen.blit(COSTUME_TEXT, COSTUME_RECT)

        COSTUME_DEFAULT = Button(image=None, pos=(300, 200),
                                text_input="DEFAULT", font=get_font(15), base_color="White",
                                hovering_color="#b68f40")

        COSTUME_BLUE = Button(image=None, pos=(300, 300),
                              text_input="BLUE", font=get_font(15), base_color="White", hovering_color="#b68f40")

        COSTUME_BACK = Button(image=None, pos=(300, 400),
                              text_input="BACK", font=get_font(15), base_color="White", hovering_color="#b68f40")

        COSTUME_DEFAULT.changeColor(COSTUME_MOUSE_POS)
        COSTUME_DEFAULT.update(screen)
        COSTUME_BLUE.changeColor(COSTUME_MOUSE_POS)
        COSTUME_BLUE.update(screen)
        COSTUME_BACK.changeColor(COSTUME_MOUSE_POS)
        COSTUME_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if COSTUME_DEFAULT.checkForInput(COSTUME_MOUSE_POS):
                    write_costume('default')
            if event.type == pygame.MOUSEBUTTONDOWN:
                if COSTUME_BLUE.checkForInput(COSTUME_MOUSE_POS):
                    write_costume('blue')
            if event.type == pygame.MOUSEBUTTONDOWN:
                if COSTUME_BACK.checkForInput(COSTUME_MOUSE_POS):
                    options()

        pygame.display.update()

def main_menu():
    while True:

        menu_x = int(cell_size * cell_number - 60)
        menu_y = int(cell_size * cell_number - 40)
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(25).render("Snake Game By Rianne", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(300, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(300, 200),
                             text_input="PLAY", font=get_font(15), base_color="#d7fcd4", hovering_color="#b68f40")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(300, 350),
                                text_input="OPTIONS", font=get_font(15), base_color="#d7fcd4", hovering_color="#b68f40")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(300, 500),
                             text_input="QUIT", font=get_font(15), base_color="#d7fcd4", hovering_color="#b68f40")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
