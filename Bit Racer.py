import pygame
import time
import random
from PIL import Image
from leaderboards import insert, getAll, checkExists

pygame.init()

#############################Initialize sounds#################################
crash_sound = pygame.mixer.Sound("Crash.wav")
pygame.mixer.music.load("Manchester_Dream.wav")
###############################################################################


#############################Initialize display dimensions#####################
display_width = 800
display_height = 600
###############################################################################


#############################Set up colors#####################################

#RGB format(red,green,blue)

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,255)
bright_blue = (0,75,200)
bright_red = (255,0,0)
bright_green = (0,255,0)
###############################################################################


#############################Load Enemy Sprites################################

#List of strings that represent enemy sprites
enemies = ["Enemy_1.png", "Enemy_2.png","Enemy_3.png","Enemy_4.png"]

#List that will hold enemy sprites loaded
car_enemies = []

#Load the enemy sprites into the game
for enemy in enemies:
    car_enemies.append(pygame.image.load(enemy))
###############################################################################


#Set user's car sprite
car_image = 'Bit Racer.png'
carImg = pygame.image.load(car_image)
car_width, car_height = Image.open(car_image).size


gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Bit race')
game_logo = "Bit-Race logo.png"
gameLogo = pygame.image.load(game_logo)
pygame.display.set_icon(gameLogo)

clock = pygame.time.Clock()

pause = False

#Function to display/update the score
def things_doged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: " + str(count), True, black)
    gameDisplay.blit(text, (0,0))


def draw_enemy(enemy, thingx, thingy):
    gameDisplay.blit(enemy, (thingx, thingy))
    #pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

def car(x,y):
    gameDisplay.blit(carImg, (x,y))

def crash(dodged, text=""):

    if not text:
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(crash_sound)

    largeText = pygame.font.Font('freesansbold.ttf', 75)
    TextSurf, TextRect = text_objects("You crashed", largeText)
    TextRect.center = ((display_width / 2), (display_height / 4))
    gameDisplay.blit(TextSurf, TextRect)


    input_box_width = 140
    input_text_size = 32

    font = pygame.font.Font(None, 32)
    smallText = pygame.font.Font('freesansbold.ttf', 32)
    TextSurf, TextRect = text_objects("Name", smallText)
    TextRect.center = ((display_width / 2) - input_box_width, (display_height / 2) + (input_text_size / 2))
    gameDisplay.blit(TextSurf, TextRect)

    input_box = pygame.Rect((display_width / 2), (display_height / 2), input_box_width, input_text_size)
    color_active = pygame.Color('black')
    color = color_active
    active = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            color = color_active
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        active = not active
                        #color = color_active if active else color_inactive
                        insert(dodged, text)
                        gameDisplay.fill(white)
                        play_again()
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        gameDisplay.fill(white)
                        things_doged(dodged)
                        crash(dodged,text)
                    else:
                        text += event.unicode

        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        gameDisplay.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(gameDisplay, color, input_box, 2)

        pygame.display.flip()

        pygame.display.update()
        clock.tick(15)

def play_again():

    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects("Play again?", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("Yes", 150, 450, 150, 50, green, bright_green, game_loop)
        button("No", 550, 450, 100, 50, red, bright_red, quitgame)
        button("Leaderboards", 350, 450, 150, 50, blue, bright_blue, leaderboard_view)

        pygame.display.update()
        clock.tick(15)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)

    game_loop()

def quitgame():
    pygame.quit()
    quit()


def button(msg, x, y, w, h, inactive_color, active_color, action=None):
    # Get current mouse position
    mouse = pygame.mouse.get_pos()

    click = pygame.mouse.get_pressed()

    # If cursor is over a button, change to hover color
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)

def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False

def paused():

    pygame.mixer.music.pause()

    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        #gameDisplay.fill(white)

        button("Continue",150, 450, 100, 50, green, bright_green, unpause)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #Display title
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("Bit race", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!",150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)
        button("Leaderboards", 325, 450, 145, 50, blue, bright_blue, leaderboard_view)

        pygame.display.update()
        clock.tick(15)

def leaderboard_text(name, score, x, y):
    largeText = pygame.font.Font('freesansbold.ttf', 25)
    TextSurf, TextRect = text_objects(name, largeText)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)

    TextSurf, TextRect = text_objects(score, largeText)
    TextRect.center = ((x + 100), y)
    gameDisplay.blit(TextSurf, TextRect)

def leaderboard_view():
    leaderboard = True
    gameDisplay.fill(white)

    if not checkExists():
        largeText = pygame.font.Font('freesansbold.ttf', 30)
        TextSurf, TextRect = text_objects("No records", largeText)
        TextRect.center = (display_width / 2, display_height / 2)
        gameDisplay.blit(TextSurf, TextRect)

    else:
        #From DB
        rows = getAll()

        x = (display_width / 2)
        y = 50

        for row in rows[0:5]:
            name = row[0]
            score = row[1]
            leaderboard_text(name, str(score), x, y)
            y+=50

    while leaderboard:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        button("Main menu", ((display_width / 2) - 63), 500, 125, 50, green, bright_green, game_intro)

        pygame.display.update()
        clock.tick(15)


def game_loop():

    global pause

    pygame.mixer.music.play(-1)

    #rows = getTopFive()
    #i = 0
    #rows = sorted(rows, key=lambda rows:rows[i])

    #print(rows)


    # Cars starting position
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    enemy_start_x = random.randrange(0, display_width)
    enemy_start_y = -600
    enemy_speed = 4
    enemy_width, enemy_height = Image.open(car_image).size
    current_enemy = random.choice(car_enemies)

    dodged = 0

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # If the user presses left or right
            # change the cars position accordingly
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        #Update the car's position (left or right)
        x += x_change

        gameDisplay.fill(white)

        #Draw the enemy
        #things(enemy_start_x, enemy_start_y, enemy_width, enemy_height, black
        draw_enemy(current_enemy, enemy_start_x, enemy_start_y)

        #Update the position of the obstacle
        enemy_start_y += enemy_speed

        #Redraw the car
        car(x,y)

        things_doged(dodged)

        #If the car hits either wall
        if x > display_width - car_width or x < 0:
            crash(dodged)

        #If the enemy left the screen, give it a new random position
        if enemy_start_y > display_height:
            enemy_start_y = 0 - enemy_height
            enemy_start_x = random.randrange(0, display_width)
            dodged += 1
            enemy_speed += 1
            current_enemy = random.choice(car_enemies)

        if enemy_start_y < y < enemy_start_y+enemy_height:
            if x > enemy_start_x and x < enemy_start_x + enemy_width or x + car_width > enemy_start_x and x + car_width <enemy_start_x + enemy_width:
                crash(dodged)

        pygame.display.update()

        clock.tick(60)

game_intro()
game_loop()

pygame.quit()

quit()