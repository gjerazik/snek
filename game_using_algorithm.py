# this is the game using the algorithm

import pygame
import random
import time
from algorithm import shortest_path

pygame.init()

# initialize the playing  board
BOARD_SIZE = (200,200)
screen = pygame.display.set_mode(BOARD_SIZE)

# make the board used for path-finding
board = [[0] * BOARD_SIZE[1] for i in range(BOARD_SIZE[0])]

# set the size of the snake and its speed
snake_size = 10
speed = 20

# record score
def display_text(points, score, curr_frame, timeout, length):
    text_points = pygame.font.SysFont('arial', 20).render("Points: " + str(points), True, (255,255,255))
    text_score = pygame.font.SysFont('arial', 20).render("Score: " + str(score), True, (255,255,255))
    text_curr_frame = pygame.font.SysFont('arial', 20).render("Curr Frame: " + str(curr_frame) + " vs Time out: " + str(timeout), True, (255,255,255))
    text_length = pygame.font.SysFont('arial', 20).render("Length: " + str(length), True, (255,255,255))
    #screen.blit(text_curr_frame, [10,10])
    #screen.blit(text_points, [10,30])
    #screen.blit(text_score, [10,50])
    #screen.blit(text_length, [10,70])

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
    head = [x,y]

    # add snake head and target to the board
    board[0][0] = 1

    # target appears with random x and y values
    target = random.choice(['harry', 'muggle'])
    target_x = round(random.randrange(0, BOARD_SIZE[0] - snake_size)/snake_size)*snake_size
    target_y = round(random.randrange(0, BOARD_SIZE[1] - snake_size)/snake_size)*snake_size
    score = 0
    points = 0
    curr_frame = 0
    timeout = 100

    while (play_on):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play_on = False

        left = right = up = down = False

        # use algorithm to find shortest path from snake head to target
        path = shortest_path(board, (x,y), (target_x, target_y))
        if path[1][0] - path[0][0] == 1:
            x += snake_size
            y += 0
        elif path[1][0] - path[0][0] == -1:
            x -= snake_size
            y += 0
        if path[1][1] - path[0][1] == 1:
            x += 0
            y += snake_size
        elif path[1][1] - path[0][1] == -1:
            x += 0
            y -= snake_size
    

        # if snake hits the edge of the board, game over
        if x > BOARD_SIZE[0] or x < 0:
            play_on = False
        if y > BOARD_SIZE[1] or y < 0:
            play_on = False

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
        
        # add new head to the board
        board[path[1][0]][path[1][1]] = 1
        board[x][y] = 0
        
        # if the snake runs into itself, game over
        for block in body[0:length-1]:
            if block == head:
                play_on = False

        naigini(snake_size, body)
        display_text(points, score, curr_frame, timeout, length)
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