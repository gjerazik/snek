# this is the path-finding algorithm (A* search) used in the game

class Block:

    def __init__(self, previous, position):
        self.f = 0
        self.g = 0
        self.h = 0
        self.previous = previous
        self.position = position
    
    def __str__(self):
        return(str(self.position))
    
    # define equality between blocks
    def __eq__(self, other):
        if self.position == other.position:
            return True

def shortest_path(board, snake, target):

    opened = [] # unexplored blocks adjacent to the ones in closed list
    closed = [] # explored blocks
    snake = Block(None, snake)
    target = Block(None, target)
    snake.f = 0
    opened.append(snake)

    # loop until target is found
    while len(opened) > 0:

        # the current block is the one with the smallest f value
        current_block = opened[0]
        for next_block in opened:
            if current_block.f > next_block.f:
                current_block = next_block

        opened.pop(opened.index(current_block))
        closed.append(current_block)

        # target is found -> make path by traversing thru previous blocks
        if current_block == target:
            path = []
            last_block = current_block
            while last_block is not None:
                path.append(last_block.position)
                last_block = last_block.previous
            path.reverse()
            return path
        
        # target is not found -> get adjacent blocks and keep searching
        adjacent = []

        up = (current_block.position[0], current_block.position[1] - 1)
        if (up[0] < (len(board)-1)) and (up[1] < (len(board[0])-1)):
            if (up[0] >= 0) and (up[1] >= 0):
                if board[up[0]][up[1]] == 0:
                    adjacent.append(Block(current_block, up))
        
        down = (current_block.position[0], current_block.position[1] + 1)
        if (down[0] < (len(board)-1)) and (down[1] < (len(board[0])-1)):
            if (down[0] >= 0) and (down[1] >= 0):
                if board[down[0]][down[1]] == 0:
                    adjacent.append(Block(current_block, down))

        right = (current_block.position[0] - 1, current_block.position[1])
        if (right[0] < (len(board)-1)) and (right[1] < (len(board[0])-1)):
            if (right[0] >= 0) and (right[1] >= 0):
                if board[right[0]][right[1]] == 0:
                    adjacent.append(Block(current_block, right))

        left = (current_block.position[0] + 1, current_block.position[1])
        if (left[0] < (len(board)-1)) and (left[1] < (len(board[0])-1)):
            if (left[0] >= 0) and (left[1] >= 0):
                if board[left[0]][left[1]] == 0:
                    adjacent.append(Block(current_block, left))
        
        # loop thru the adjacent blocks
        for block in adjacent:

            if block == target:
                path = []
                last_block = block
                while last_block is not None:
                    path.append(last_block.position)
                    last_block = last_block.previous
                path.reverse()
                return path

            for k in opened:
                if block == k:
                    if block.f > k.f:
                        break
                    elif block.g > k.g:
                        k.previous = current_block
                        k.g = current_block.g + (abs(k.position[0] - current_block.position[0]) + abs(k.position[1] - current_block.position[1]))
                        k.h = abs(k.position[0] - target.position[0]) + abs(k.position[1] - target.position[1])
                        k.f = k.g + k.h
            
            # check if the block is already in closed
            for y in closed:
                if block == y:
                    break

            if block not in closed:
                opened.append(block)

            # g(n) is the distance from the current block to the snake's head
            block.g = current_block.g + (abs(block.position[0] - current_block.position[0]) + abs(block.position[1] - current_block.position[1]))
            # h(n) is the distance from the current block to the target (manhattan distance)
            block.h = abs(block.position[0] - target.position[0]) + abs(block.position[1] - target.position[1])
            # f(n) is the total cost
            block.f = block.g + block.h
