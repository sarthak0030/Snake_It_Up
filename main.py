from pygame.locals import *
import time
import random
import sys
import pygame
from pygame.math import Vector2

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
light_green = (0, 200, 0)
blue = (0, 0, 255)
bg = pygame.image.load("Graphics/background_4.jpg")
controls_screen_bg = pygame.image.load("Graphics/control_menu_window_1.jpg")
starting_window = pygame.image.load("Graphics/start_window.jpg")
cell_size = 40
cell_number = 17
clock = pygame.time.Clock()

# define global variable
clicked = False


def message(msg, color, x_pos, y_pos, size):
    font = pygame.font.SysFont(None, size)
    screen_text = font.render(msg, True, color)
    screen.blit(screen_text, [x_pos, y_pos])


screen = pygame.display.set_mode(
    (cell_size * cell_number, cell_size * cell_number))


class button:
    # colours for button and text
    button_col = (236, 129, 0)
    hover_col = (242, 193, 2)
    click_col = (252, 246, 50)
    text_col = white
    width = 170
    height = 50

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def draw_button(self):

        global clicked
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.width, self.height)

        # check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(screen, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(screen, self.hover_col, button_rect)
        else:
            pygame.draw.rect(screen, self.button_col, button_rect)

        # add border to button
        pygame.draw.line(screen, white, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(screen, white, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(screen, white, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(screen, white, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        # add text to button
        text_img = game_font_1.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 8))
        return action

    screen.blit(starting_window, (0, 0))
    pygame.display.update()
    time.sleep(2)


def controls_menu():
    control = True
    while control:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    control = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.blit(controls_screen_bg, (0, 0))
        pygame.display.update()
        clock.tick(90)


play = button(250, 360, 'START')
controls = button(250, 435, 'CONTROLS')
Quit = button(250, 515, 'QUIT')


# Graphics, body and logic of snake
class SNAKE:
    # Snake Graphics
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/Sound_crunch.wav')

    # Assemble snake
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
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

    # Implimenting head graphics
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    # Implimenting tail graphics
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    # Snake movement
    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    # Increase length of the snake after eating apple
    def add_block(self):
        self.new_block = True

    # Sound while eating apple
    def play_crunch_sound(self):
        self.crunch_sound.play()

    # Reset snake after game over
    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


# Drawing apple and position of it
class FRUIT:
    def __init__(self):
        self.randomize()

    # Draw apple
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    # Randomizing the position of apple
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


# Main game code
class MAIN:
    def __init__(self):
        self.play_background_music()
        self.snake = SNAKE()
        self.fruit = FRUIT()

    # Update all
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    # Draw elements
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    # Check if snake collide the fruit
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    # Pause function
    def pause(self):
        self.paused_bg = pygame.image.load("Graphics/paused_background_1.png")
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pygame.mixer.music.unpause()
                        paused = False
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            screen.blit(self.paused_bg, (0, 0))
            pygame.display.update()
            clock.tick(20)

    # Game over text
    def Game_Over(self):
        self.game_over_bg = pygame.image.load("Graphics/game_over_background.png")
        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_over = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            pygame.mixer.music.pause()
            screen.blit(self.game_over_bg, (0, 0))
            pygame.display.update()
            clock.tick(2)

    # Check if snake collide wall and then game over
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.play_wall_crash_sound()
            self.game_over()
            self.Game_Over()
            pygame.mixer.music.unpause()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    # Reseting the snake after game over
    def game_over(self):
        self.snake.reset()

    # dark shade of grass
    def draw_grass(self):
        grass_color = (162, 209, 73)
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

    # background music
    def play_background_music(self):
        pygame.mixer.music.load("Sound/snake_game_background_music_1.wav")
        pygame.mixer.music.play(-1)

    def play_wall_crash_sound(self):
        sound = pygame.mixer.Sound("Sound/wall_hit_sound.wav")
        pygame.mixer.Sound.play(sound)

    # draw score
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left - 2, apple_rect.top, apple_rect.width + score_rect.width + 6,
                              apple_rect.height)

        pygame.draw.rect(screen, (162, 209, 73), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 17
apple = pygame.image.load('Graphics/apple_2.png').convert_alpha()
game_font = pygame.font.Font('Font/poetsenoneregular.ttf', 25)
game_font_1 = pygame.font.Font('Font/poetsenoneregular.ttf', 30)
pygame.display.set_caption('Snake It Up')
icon = pygame.image.load('Graphics/snake_logo.png')
pygame.display.set_icon(icon)
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()


def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                elif event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                elif event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                elif event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                elif event.key == pygame.K_SPACE:
                    pygame.mixer.music.pause()
                    main_game.pause()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill((170, 215, 81))
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)


run = True
while run:

    screen.blit(bg, (0, 0))
    pygame.mixer.music.unpause()

    if play.draw_button():
        game_loop()
    if Quit.draw_button():
        pygame.quit()
        sys.exit()
    if controls.draw_button():
        controls_menu()

    message("Contact Us:", white, 13, 632, 21)
    message("patilsarthak00030@gmail.com", white, 13, 653, 21)
    clock.tick(0)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_s:
                game_loop()
            if event.key == pygame.K_c:
                controls_menu()
            if event.type == pygame.QUIT:
                run = False
    pygame.display.update()