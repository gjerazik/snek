# this is the game where a user can play

import pygame
import random
import time

pygame.init()

# initialize the playing  board
BOARD_SIZE = (10,10)
zoom = 40
zoomed_screen = pygame.display.set_mode((BOARD_SIZE[0]*zoom, BOARD_SIZE[1]*zoom))
screen = pygame.Surface((BOARD_SIZE[0], BOARD_SIZE[1]))

# set the size of the snake and its speed
snake_size = 1
speed = 15

# make snake
def naigini(snake_size, body):
    for block in body:
        pygame.draw.rect(screen, (255,255,255), [block[0],block[1],snake_size,snake_size])

# make game
def game():

    # body of snake starts as empty array with length 1
    body = []
    length = 1
    play_on = True
    x = y = move_x = move_y = 0

    # target appears with random x and y values
    target = random.choice(['harry', 'muggle'])
    target_x = round(random.randrange(0, BOARD_SIZE[0] - snake_size)/snake_size)*snake_size
    target_y = round(random.randrange(0, BOARD_SIZE[1] - snake_size)/snake_size)*snake_size
    score = 0
    points = 0
    curr_frame = 0
    CYCLE_ALLOWANCE = 1.5
    TIMEOUT = (4 * BOARD_SIZE[0] - 4) * CYCLE_ALLOWANCE

    while (play_on):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                play_on = False

            left = right = up = down = False

            # making the snake move according to which keys are pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left = True
                elif event.key == pygame.K_RIGHT:
                    right = True
                elif event.key == pygame.K_UP:
                    up = True
                elif event.key == pygame.K_DOWN:
                    down = True
    
        if left:
            move_x = -snake_size
            move_y = 0           
        if right:
            move_x = snake_size
            move_y = 0
        if up:
            move_x = 0
            move_y = -snake_size
        if down:
            move_x = 0
            move_y = snake_size

        # if snake hits the edge of the board, game over
        if x > BOARD_SIZE[0] or x < 0:
            play_on = False
        if y > BOARD_SIZE[1] or y < 0:
            play_on = False

        x += move_x
        y += move_y

        score += 1
        curr_frame += 1
        if curr_frame == timeout:
            play_on = False

        screen.fill((0,0,0))
        
        if target == 'harry':
            pygame.draw.rect(screen, (255,0,0), [target_x,target_y,snake_size,snake_size])
            points_added = 60
        if target == 'muggle':
            pygame.draw.rect(screen, (0,0,255), [target_x,target_y,snake_size,snake_size])
            points_added = 20
        
        # initialize head of snake
        head = [x,y]
        body.append(head)
        if len(body) > length:
            del body[0]
        
        # if the snake runs into itself, game over
        for block in body[0:length-1]:
            if block == head:
                play_on = False

        naigini(snake_size, body)
        display_text(points, score, curr_frame, timeout, length)
        zoomed_screen.blit(pygame.transform.scale(screen, zoomed_screen.get_rect().size), (0, 0))
        pygame.display.update()

        # if snake eats a target
        if x == target_x and y == target_y:
            length += 1
            points += points_added
            curr_frame = 0
            target_x = round(random.randrange(0, BOARD_SIZE[0] - snake_size)/snake_size)*snake_size
            target_y = round(random.randrange(0, BOARD_SIZE[1] - snake_size)/snake_size)*snake_size
            target = random.choice(['harry', 'muggle'])

        pygame.time.Clock().tick(speed)

    pygame.quit()
    quit()

game()
