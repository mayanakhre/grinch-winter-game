# Rhea Mahuli (rmm9uyv) and Maya Nakhre (mtn4ghj)

# The Grinch Who Stole Clothes

import pygame
import gamebox
import random

game_on = False

def make_title_screen(keys):
    """Designs the title screen for the game. Takes the keys as a parameter"""
    global game_on
    title_screen = gamebox.from_image(400,300,"title_screen.jpg")
    title_screen.scale_by(0.40)
    title = gamebox.from_text(400,200, "The Grinch Who Stole Clothes",75,'darkblue')
    first_line = gamebox.from_text(400, 250, 'You are ice skating at the North Pole, but it’s cold!', 30, 'white')
    second = gamebox.from_text(400, 280, 'Catch the clothes falling from the sky to gain points and stay warm.', 30, 'white')
    third = gamebox.from_text(400, 310, 'Watch out for the grinch; every time you touch him, you’ll lose a life.', 30, 'white')
    fourth = gamebox.from_text(400, 340, 'Lose 3 three lives, and the game ends.', 30,'white')
    five = gamebox.from_text(400, 370, 'Press the spacebar to jump and the right ', 30, 'white')
    six = gamebox.from_text(400, 400,'and left arrows to move from side to side.', 30,'white')
    seven = gamebox.from_text(400, 450, 'PRESS THE "S" KEY TO START', 50, 'darkblue')
    ids = gamebox.from_text(180, 20, 'Rhea Mahuli (rmm9uyv) and Maya Nakhre (mtn4ghj) ', 20, 'darkblue')
    camera.draw(title_screen)
    camera.draw(first_line)
    camera.draw(second)
    camera.draw(third)
    camera.draw(fourth)
    camera.draw(five)
    camera.draw(six)
    camera.draw(seven)
    camera.draw(ids)
    camera.draw(title)
    if pygame.K_s in keys:
        game_on = True


#setup
camera = gamebox.Camera(800, 600)
background = gamebox.from_image(400, 300, 'snow.jpg')
background.scale_by(1.8)
shirt = gamebox.from_image(400, 300, "shirt.jpg")
shirt.scale_by(2)
camera.draw(shirt)
camera.display()
shirt.scale_by(.1)
pant = gamebox.from_image(300,900,"jeans.png")
pant.scale_by(.1)
hat = gamebox.from_image(550,900,"hat.png")
hat.scale_by(.05)


collectibles = [shirt, pant, hat]

scenery = [background]
landed_since_last_jump = False
collectible_speed = 5




def move_collectibles():
    """Moves the collectibles from the top of the screen downwards randomly"""
    global game_on
    for image in collectibles:
        image.y += collectible_speed
        if image.y > 600:
            image.x = random.randrange(0, 800)
            image.y = -25


grinch = "grinch.png"
grinch = gamebox.from_image(1000, 521, grinch)
grinch.scale_by(.13)

def move_and_make_grinch():
    """ Makes a grinch that moves through the screen at random intervals"""
    global grinch, game_on
    grinch_speed = 5
    grinch.x -= grinch_speed
    camera.draw(grinch)
    if grinch.x > 800:
        grinch.x -= random.randrange(int(0.1),2)
    if grinch.x < 0:
        grinch.x = 1000




def draw_scenery():
    """Draws the items in the scenery and the collectibles"""
    for item in scenery:
        camera.draw(item)
    for item in collectibles:
        camera.draw(item)




def make_man():
    """Creates a sprite sheet for the man and returns a list of the positions"""
    spritesheet = "man_sprites.png"
    images = gamebox.load_sprite_sheet(spritesheet, 1, 8)
    man_position = []
    for image in images:
        stage = gamebox.from_image(100, 500, image)
        man_position.append(stage)
    return man_position


def move_man(keys, man_position):
    """ Takes the keys and the list of man positions are parameters. Moves the man when the keys are pressed."""
    global landed_since_last_jump, ground, game_on, stage_counter, score, lives, game_on
    for image in man_position:
        image.move_to_stop_overlapping(ground)
        if image.touches(ground):
            landed_since_last_jump = True
        if pygame.K_RIGHT in keys and landed_since_last_jump:
            image.xspeed += 0.5
        if pygame.K_LEFT in keys and landed_since_last_jump:
            image.xspeed -= 0.5
        if pygame.K_SPACE in keys and landed_since_last_jump:
            game_on = True
            image.yspeed -= 18
            landed_since_last_jump = False
        if image.x > 800:   # boundaries
            image.x = 800
        if image.x < 5:
            image.x = 5
        if image.touches(collectibles[0]):  # collectibles vanish when touches
            collectibles[0].x += 1000
            score += 1
        if image.touches(collectibles[1]):
            collectibles[1].x += 1000
            score += 1
        if image.touches(collectibles[2]):
            collectibles[2].x += 1000
            score += 1
        image.yspeed += gravity
        image.move_speed()

#lives

score = 0
lives = 3

def draw_stats():
    """ Draws the health bar and the score box """
    scorebox = gamebox.from_text(75, 25, "score: " + str(score), 36, 'red')
    camera.draw(scorebox)
    for i in range(lives):
        heart = gamebox.from_image(775, 25, 'heart.png')
        heart.x -= 50 * i
        heart.scale_by(0.5)
        camera.draw(heart)

def touches_grinch(man_position):
    """ Takes the list of man positions as a parameter and checks to see if the grinch was touched. """
    for image in man_position:
        if image.touches(grinch):
            return True

lose = False
def game_over():
    """ Checks to see if all three lives were lost. Sets game_on variable to False"""
    global game_on, lose
    if lives == 0:
        game_on = False
        lose = True

stage_counter = 0
gravity = 1
man = make_man()
ground = gamebox.from_color(400,582,'white',800,50)


#tick
def tick(keys):
    """ This function takes the keys as a parameter and executes the functions made above if game_on variable is set
    to True."""
    global stage_counter, lives, game_on, score
    camera.display()
    if game_on:
        draw_scenery()
        camera.display()
        stage_counter += 0.2
        move_man(keys, man)
        if pygame.K_RIGHT or pygame.K_LEFT or pygame.K_SPACE:
            camera.draw(man[int(stage_counter) % len(man) - 8])
        else:
            camera.draw(man[0])
        if touches_grinch(man):
            grinch.x = 1000
            lives -= 1
        camera.draw(ground)
        draw_stats()
        move_collectibles()
        game_over()
        move_and_make_grinch()
        camera.display()
    else:
        make_title_screen(keys)
        if lose:
            camera.draw(background)
            over = gamebox.from_text(400,200, 'GAME OVER', 90, 'white')
            space = gamebox.from_text(400,350, 'PRESS SPACE TO PLAY AGAIN', 50, 'white')
            camera.draw(over)
            camera.draw(space)
            camera.display()
            if pygame.K_SPACE in keys:
                lives = 3
                score = 0
                game_on = True




gamebox.timer_loop(30, tick)