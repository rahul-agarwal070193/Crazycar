import pygame
import random
import time

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# initialising constant variable
display_width = 1200
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)

red = (150, 0, 0)
green = (0, 150, 0)

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

car_width = 72
car_height = 83
pause = False

# read hiscore from txt file 
hiscore = 500

# loading images needed
gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('Crazy Racer')

gameIcon = pygame.image.load('car_type_1.png')
pygame.display.set_icon(gameIcon)

carImg = pygame.image.load('car_type_1.png')
carImg2 = pygame.image.load('car_type_2.jpg')
carImg4 = pygame.image.load('car_type_4.jpg')
carImg3 = pygame.image.load('car_type_3.jpg')
carImg5 = pygame.image.load('car_type_5.jpg')
carImg6 = pygame.image.load('car_type_6.jpg')


stop_sign = pygame.image.load('stop_sign_1.jpg')

baground = pygame.image.load('road2.jpg')
road = pygame.image.load('road1.jpg')


# display hiscore
def things_hiscore(count):
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render("HISCORE: " + str(count), True, black)
    gameDisplay.blit(text, (500, 0))


# display reward
def things_reward(count):
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render("REWARD: " + str(count), True, black)
    gameDisplay.blit(text, (1000, 50))


# display life
def things_life(count):
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render("LIFE: " + str(count), True, black)
    gameDisplay.blit(text, (1000, 0))


# display level
def things_level(count):
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render("LEVEL: " + str(count), True, black)
    gameDisplay.blit(text, (0, 30))


# display dodged
def things_dodged(count):
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render("DODGED: " + str(count), True, black)
    gameDisplay.blit(text, (0, 0))


# create block
def block(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])


# create car
def car(car_type, x, y):
    if car_type == 1:
        gameDisplay.blit(carImg, (x, y))
    if car_type == 2:
        gameDisplay.blit(carImg2, (x, y))
    if car_type == 3:
        gameDisplay.blit(carImg3, (x, y))
    if car_type == 4:
        gameDisplay.blit(carImg4, (x, y))
    if car_type == 5:
        gameDisplay.blit(carImg5, (x, y))
    if car_type == 6:
        gameDisplay.blit(carImg6, (x, y))


# make text surface and rectangle        
def text_objects(text, color, font):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


# deals when car crashs 
def crash(car_type, life, dodged, level, hiscore, reward=None):
    pygame.mixer.music.load("Crash.mp3")
    pygame.mixer.music.play(0)
    # pygame.mixer.music.stop()
    if life == 0:
        with open("hiscore.txt", "w") as f:
            f.write(str(hiscore))
        time.sleep(2)
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = text_objects("GAME OVER", red, largeText)
        TextRect.center = ((display_width / 2), 50)
        gameDisplay.blit(TextSurf, TextRect)

        largeText = pygame.font.SysFont("comicsansms", 70)
        TextSurf, TextRect = text_objects("Your Score :" + str(reward), black, largeText)
        TextRect.center = ((display_width / 2) - 45, (display_height / 2) - 100)
        gameDisplay.blit(TextSurf, TextRect)

        largeText = pygame.font.SysFont("comicsansms", 70)
        TextSurf, TextRect = text_objects("Hiscore :" + str(hiscore), black, largeText)
        TextRect.center = ((display_width / 2) - 100, (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            button("Play Again", 200, 450, 100, 50, green, bright_green, select_car)
            button("Quit", 900, 450, 100, 50, red, bright_red, car_stop)
            pygame.display.update()
            clock.tick(15)

    else:
        time.sleep(1)
        gameDisplay.fill(white)

        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = text_objects("life left " + str(life), black, largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()
        clock.tick(15)
        time.sleep(2)
        game_loop(car_type, life, dodged, level)


# create button
def button(msg, x, y, w, h, ic, ac, action=None, car_type=None, life=None, dodged=None, level=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None and car_type == None:
            action()
        if click[0] == 1 and action != None and car_type != None:
            action(car_type, life, dodged, level)
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, black, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


# exits game
def quitgame():
    pygame.quit()
    quit()


# unpause and pausing the game
def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False


def paused():
    pygame.mixer.music.pause()

    largeText = pygame.font.SysFont("comicsansms", 115)
    TextSurf, TextRect = text_objects("Paused", black, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("Continue", 200, 450, 100, 50, green, bright_green, unpause)
        button("Quit", 900, 450, 100, 50, red, bright_red, car_stop)

        pygame.display.update()
        clock.tick(15)

    # select car window


def select_car():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)

        largeText = pygame.font.SysFont("comicsansms", 50)
        TextSurf, TextRect = text_objects("Choose Vehicle", black, largeText)
        TextRect.center = ((display_width / 2), 50)
        gameDisplay.blit(TextSurf, TextRect)

        gameDisplay.blit(carImg, (50, 150))
        gameDisplay.blit(carImg2, (50, 300))
        gameDisplay.blit(carImg3, (645, 300))
        gameDisplay.blit(carImg4, (635, 150))
        gameDisplay.blit(carImg5, (635, 450))
        gameDisplay.blit(carImg6, (50, 450))

        # def button(msg,x,y,w,h,ic,ac,acti4on=None,car_type=None,life=None,dodged=None,level=None):

        button("Formula 1", 200, 160, 150, 50, green, bright_green, game_loop, 1, 3, 0, 1)
        button("Sedan", 200, 310, 150, 50, green, bright_green, game_loop, 2, 3, 0, 1)
        button("Convertible", 800, 310, 150, 50, green, bright_green, game_loop, 3, 3, 0, 1)
        button("Moterbike", 800, 160, 150, 50, green, bright_green, game_loop, 4, 3, 0, 1)
        button("spaceship", 800, 460, 150, 50, green, bright_green, game_loop, 5, 3, 0, 1)
        button("alien", 200, 460, 150, 50, green, bright_green, game_loop, 6, 3, 0, 1)

        pygame.display.update()
        clock.tick(60)


# opening view of the appplication
def game_intro():
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        gameDisplay.blit(road, (x - 5, 0))
        car(1, x, y)

        largeText = pygame.font.SysFont("comicsansms", 115)
        a = random.randrange(0, 255)
        b = random.randrange(0, 255)
        c = random.randrange(0, 255)
        title_color = [a, b, c]
        TextSurf, TextRect = text_objects("Crazy   Racer", title_color, largeText)
        TextRect.center = ((display_width / 2) - 20, (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)
        # car(x,y)

        button("Lets GO!!!!", 200, 450, 200, 50, green, bright_green, car_start)
        button("Quit", 750, 450, 200, 50, red, bright_red, car_stop)

        pygame.display.update()
        clock.tick(20)


# if player choose start
def car_start():
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    gameDisplay.fill(white)
    while y > 0:
        y = y - 10
        gameDisplay.blit(road, (x - 5, 0))
        car(1, x, y)
        if (y <= 0):
            select_car()
        pygame.display.update()
        clock.tick(60)


# if player choose quit
def car_stop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    gameDisplay.fill(white)
    while y > 0:
        y = y - 10
        gameDisplay.blit(road, (x - 5, 0))
        gameDisplay.blit(stop_sign, (x + 90, 100))
        car(1, x, y)
        pygame.display.update()
        clock.tick(60)

        if (y < 200):
            # time.sleep(1)
            quitgame()

        # the main game


def game_loop(car_type, life1, dodged1, level1):
    global pause

    # adding baground sound
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(0)
    pygame.mixer.music.queue('Race_Car.mp3')

    # que=[pygame.mixer.music.load('music.mp3'),pygame.mixer.music.load('Race_Car.mp3')]
    # pygame.mixer.music.play(-1)
    # volume=pygame.mixer.music.get_volume()
    # print(volume)
    pygame.mixer.music.set_volume(0.5)
    # car position initial
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    x_change = 0
    y_change = 0

    # setting baground sound
    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    car_type = car_type
    life = life1
    level = level1
    dodged = dodged1

    # block variable
    thing_startx = random.randrange(0, display_width)
    thing_starty = -900
    thing_speed = 3 + level - 1
    thing_width = 100

    thing_startx1 = random.randrange(0, display_width)
    thing_starty1 = -800
    thing_speed1 = 3.5 + level - 1
    thing_width1 = 100

    thing_startx2 = random.randrange(0, display_width)
    thing_starty2 = -700
    thing_speed2 = 4 + level - 1
    thing_width2 = 100

    thing_startx3 = random.randrange(0, display_width)
    thing_starty3 = -600
    thing_speed3 = 4.5 + level - 1
    thing_width3 = 100
    reward = 0

    thing_height = 50

    # block color variable
    a = random.randrange(0, 100)
    b = random.randrange(0, 100)
    c = random.randrange(0, 100)
    block_color = [a, b, c]

    gameExit = False

    while not gameExit:
        block_color = [a, b, c]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_UP:
                    y_change = -5
                if event.key == pygame.K_DOWN:
                    y_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        x += x_change
        y += y_change

        # display
        # gameDisplay.blit(baground,(0,0))
        gameDisplay.fill(white)
        car(car_type, x, y)
        things_dodged(dodged)
        things_level(level)
        things_life(life)
        things_reward(reward)
        things_hiscore(float(hiscore))

        # boundry condition
        if x > display_width - car_width or x < 0:
            life -= 1
            things_life(life)
            crash(car_type, life, dodged, level, hiscore, reward)

        if y > display_height - car_height or y < 0:
            life -= 1
            things_life(life)
            crash(car_type, life, dodged, level, hiscore, reward)

        # block 1
        block(thing_startx, thing_starty, thing_width, thing_height, block_color)
        thing_starty += thing_speed

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            dodged += 1
            thing_speed += 0.01
            thing_width = random.randrange(100, 150)

        if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
            if y > thing_starty and y < thing_starty + thing_height or y + car_height > thing_starty and y + car_height < thing_starty + thing_height:
                life -= 1
                things_life(life)
                crash(car_type, life, dodged, level, hiscore, reward)

        # block 2
        block(thing_startx1, thing_starty1, thing_width1, thing_height, block_color)
        thing_starty1 += thing_speed1

        if thing_starty1 > display_height:
            thing_starty1 = 0 - thing_height
            thing_startx1 = random.randrange(0, display_width)
            dodged += 1
            thing_speed1 += 0.01
            thing_width1 = random.randrange(100, 150)

        if x > thing_startx1 and x < thing_startx1 + thing_width1 or x + car_width > thing_startx1 and x + car_width < thing_startx1 + thing_width1:
            if y > thing_starty1 and y < thing_starty1 + thing_height or y + car_height > thing_starty1 and y + car_height < thing_starty1 + thing_height:
                print('uhfuwfh')
                life -= 1
                things_life(life)
                crash(car_type, life, dodged, level, hiscore, reward)

        # block 3
        block(thing_startx2, thing_starty2, thing_width2, thing_height, block_color)
        thing_starty2 += thing_speed2

        if thing_starty2 > display_height:
            thing_starty2 = 0 - thing_height
            thing_startx2 = random.randrange(0, display_width)
            dodged += 1
            thing_speed2 += 0.01
            thing_width2 = random.randrange(100, 150)

        if x > thing_startx2 and x < thing_startx2 + thing_width2 or x + car_width > thing_startx2 and x + car_width < thing_startx2 + thing_width2:
            if y > thing_starty2 and y < thing_starty2 + thing_height or y + car_height > thing_starty2 and y + car_height < thing_starty2 + thing_height:
                print('uhfuwfh')
                life -= 1
                things_life(life)
                crash(car_type, life, dodged, level, hiscore, reward)

        # block 4
        block(thing_startx3, thing_starty3, thing_width3, thing_height, block_color)
        thing_starty3 += thing_speed3

        if thing_starty3 > display_height:
            thing_starty3 = 0 - thing_height
            thing_startx3 = random.randrange(0, display_width)
            dodged += 1
            thing_speed3 += 0.01
            thing_width3 = random.randrange(100, 150)

        if x > thing_startx3 and x < thing_startx3 + thing_width3 or x + car_width > thing_startx3 and x + car_width < thing_startx3 + thing_width3:
            if y > thing_starty3 and y < thing_starty3 + thing_height or y + car_height > thing_starty3 and y + car_height < thing_starty3 + thing_height:
                # print('uhfuwfh')
                life -= 1
                things_life(life)
                crash(car_type, life, dodged, level, hiscore, reward)

        # update hiscore
        if (reward > float(hiscore)):
            hiscore = str(reward)
            things_hiscore(hiscore)

        # level change
        if dodged == 10 + (level * 5):
            # increasing speed of the block
            thing_speed = thing_speed + 1 - 0.5
            thing_speed1 = thing_speed1 + 1 - 0.5
            thing_speed2 = thing_speed2 + 1 - 0.5
            thing_speed3 = thing_speed3 + 1 - 0.5

            # increasing level
            dodged = 0
            level = level + 1

            # changing color of the block for a level
            a = random.randrange(0, 100)
            b = random.randrange(0, 100)
            c = random.randrange(0, 100)

            if level % 3 == 0:
                life = life + 1

        reward = 10 * (level - 1) + level * (level - 1) * 2.5 + dodged
        pygame.display.update()
        clock.tick(60)


game_intro()
