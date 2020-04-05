# this is the game using the algorithm

import pygame
import random
import time
from algorithm import shortest_path

pygame.init() 

# initialize the playing  board
BOARD_SIZE = (10,10)
zoom = 40
zoomed_screen = pygame.display.set_mode((BOARD_SIZE[0]*zoom, BOARD_SIZE[1]*zoom))
screen = pygame.Surface((BOARD_SIZE[0], BOARD_SIZE[1]))

# make the board used for path-finding
board = [[0] * BOARD_SIZE[1] for i in range(BOARD_SIZE[0])]

# set the size of the snake and its speed
snake_size = 1
speed = 20

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
body.append(head)

# target appears with random x and y values of the blocks not occupied by the snake's body
available = []
for i in range(BOARD_SIZE[0]):
    for j in range(BOARD_SIZE[1]):
        if board[i][j] == 0:
            available.append([i,j])

target_coordinates = random.choice(available)
target_x = round(target_coordinates[0])
target_y = round(target_coordinates[1])
target = random.choice(['harry', 'muggle'])
score = 0
points = 0
curr_frame = 0
CYCLE_ALLOWANCE = 1.5
TIMEOUT = (4 * BOARD_SIZE[0] - 4) * CYCLE_ALLOWANCE

while (play_on):

    board[x][y] = 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play_on = False

    left = right = up = down = False

    screen.fill((0,0,0))

    if target == 'harry':
        pygame.draw.rect(screen, (255,0,0), [target_x,target_y,snake_size,snake_size])
        points_added = 60
    if target == 'muggle':
        pygame.draw.rect(screen, (0,0,255), [target_x,target_y,snake_size,snake_size])
        points_added = 20

    # use algorithm to find shortest path from snake head to target
    path = shortest_path(board, (x,y), (target_x, target_y))

    # if there is a direct path, take the first step in the path
    if path is not None:
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

    # if the snake is caught in a loop, move to another free block  
    else: 
        if ((x+1) < len(board)-1) and ((x+1) >= 0) and (board[x+1][y] == 0):
            x += snake_size
            y += 0
        elif ((x-1) < len(board)-1) and ((x-1) >= 0) and (board[x-1][y] == 0):
            x -= snake_size
            y += 0
        elif ((y+1) < len(board[0])-1) and ((y+1) >= 0) and (board[x][y+1] == 0):
            x += 0
            y += snake_size
        elif ((y-1) < len(board[0])-1) and ((y-1) >= 0) and (board[x][y-1] == 0):
            x += 0
            y -= snake_size
        else:
            print('TRAPPED')
            return None

    # if snake hits the edge of the board, game over
    if x > BOARD_SIZE[0] or x < 0:
        play_on = False
    if y > BOARD_SIZE[1] or y < 0:
        play_on = False

    # if time runs out, game over
    score += 1
    curr_frame += 1
    if curr_frame > TIMEOUT:
        play_on = False 
        return None

    # initialize head of snake
    head = [x,y]
    body.append(head)      

    if len(body) > length:
        board[body[0][0]][body[0][1]] = 0
        del body[0]

    # if the snake runs into itself, game over
    for block in body[0:length-1]:
        if block == head:
            play_on = False
            print('ran into itself')

    naigini(snake_size, body)
    zoomed_screen.blit(pygame.transform.scale(screen, zoomed_screen.get_rect().size), (0, 0))
    pygame.display.update()

    # if snake eats a target
    if x == target_x and y == target_y:
        length += 1
        points += points_added
        curr_frame = 0

        available = []
        for i in range(BOARD_SIZE[0]):
            for j in range(BOARD_SIZE[1]):
                if board[i][j] == 0:
                    if [i,j] != head:
                        available.append([i,j])

        if len(available) > 0:
            target_coordinates = random.choice(available)
            target_x = round(target_coordinates[0])
            target_y = round(target_coordinates[1])
            target = random.choice(['harry', 'muggle'])
        else:
            print('you won')
            return None

    pygame.time.Clock().tick(speed)

pygame.quit()
quit()

game()
