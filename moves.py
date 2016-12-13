# moves.py
# Author: Spencer Ollila

# This takes the guide's information from mapper.py
# and returns a list of acceptable moves and their
# corresponding locations

import dill

def get_moves(guide = [], loc = [], frame_num = 0, *args):
    if frame_num:
        with open('time_map.txt', 'rb') as f:
            new_map = dill.load(f)
        index = ((frame_num - 455)/5)
        new_guide = new_map[index]
        if frame_num == new_guide[0]:
            guide = new_guide.pop()
    # Check the map in the four directions in which moves are acceptable, 
    # and see if they are clear
    y       = loc[0]
    x       = loc[1]
    #print("moves: checking moves at %d, %d" % (y,x))
    moves   = []
    # If the row above is clear
    if (guide[y-1][x] == 1):
        # Then up is a viable candidate
        new_loc = [y-1, x]
        moves.append([1, new_loc])
    # If they're not already on the far right or a turtle
    if not (x == 17) and not ((y == 2) or (y==5)):
        # If moving to the right is okay
        if (guide[y][x+1] == 1):
            # Then that move is okay to make
            new_loc = [y, x+1]
            moves.append([2, new_loc])
    # If they are not already on the far left or on a turtle
    if not (x == 0) and not ((y == 2) or (y == 5)):
        # If the column to the left is clear
        if (guide[y][x-1] == 1):
            # Then Left is a viable candidate
            new_loc = [y, x-1]
            moves.append([3, new_loc])
    # If they're not already on the bottom
    if not (y == 12):
        # If moving downwards is safe to do
        if (guide[y+1][x] == 1):
            # Then moving downward is alright to do
            new_loc = [y+1, x]
            moves.append([4, new_loc])
    # If no moves were available, it's okay to just sit still for a turn.
    if not len(moves):
        moves.append([0, loc])
    return moves

# Some handy moves & corresponding codes
# noop		    = 0
# up		    = 1
# right		    = 2
# left		    = 3
# down		    = 4
