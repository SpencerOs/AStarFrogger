# mapper.py
# Author: Spencer Ollila

# This detects the screen input and outputs
# a 13h x 18w graph representing the player's
# current situation, the goal of the agent,
# and the player's current location.
import numpy as np

# Set the screened variables
rows = []
prev = []
# Turtles and Lilly Pads
rows.insert(0, 19)
rows.insert(1, 31)
rows.insert(2, 47)
rows.insert(3, 57)
rows.insert(4, 70)
rows.insert(5, 86)
# The Road
rows.insert(6, 97)

rows.insert(7, 110)
rows.insert(8, 124)
rows.insert(9, 135)
rows.insert(10, 150)
rows.insert(11, 163)

rows.insert(12, 175)

# Left to Right
columns = []
columns.insert(0, 8)
columns.insert(1, 15)
columns.insert(2, 23)
columns.insert(3, 31)
columns.insert(4, 39)
columns.insert(5, 47)
columns.insert(6, 55)
columns.insert(7, 63)
columns.insert(8, 71)
columns.insert(9, 79)
columns.insert(10, 87)
columns.insert(11, 95)
columns.insert(12, 103)
columns.insert(13, 111)
columns.insert(14, 119)
columns.insert(15, 127)
columns.insert(16, 135)
columns.insert(17, 143)
# Right boundry
columns.insert(18, 149)

road        = [0,0,0]
river       = [0,28,136]
frog        = [110,156,66]
road_frog   = [82,126,45]

semi        = [236,236,236]
pink_car    = [198,89,179]
green_car   = [53, 95,24]
purple_car  = [164,89,208]
orange_car  = [195,144,61]

def set_guide(screen = [], old_loc = [],  *args):
    global prev
    coll    = []
    loc     = []
    found   = False
    set_right=False
    # Thirteen rows
    for i in range (13):
        row = []
        y   = rows[i]
        # Eighteen columns
        for j in range (18):
			# states can be one of three states (four is a garbage placeholder value here)
			# 1	    Safe to move to
			# 2	    Unsafe spot
			# 3	    Player
            state = 4
            total = 0
			# Read the row to see if it is safe
            for x in range (columns[j], columns[j+1]):
                # if the frog's (unique!) color has been detected
                if np.all(screen[y,x] == frog):
                    state = 3
                    #if not np.all(old_loc == loc):
                        #print("mapper: new location is %s" % loc)
                    found = True
                # Turns out, the frog changes color when it's on the road, so prepare
                # for some janky-ass hole-patching.
                elif (np.all(screen[y,x] == road_frog) and not i == 0):
                    total += 1
                    if total > 4:
                        state = 3
                        found = True
                elif set_right:
                    state = 2
                    set_right = False
                elif (state == 4) or (state == 1):
                    # for the landing bay section
                    if i == 0:
                        if np.all(screen[y,x] == river):
                            state = 1
                        else:
                            state = 2
					# for the river section
                    elif i < 6:
						# if there are any pixels which aren't the river,
						# mark it as safe
                        if not np.all(screen[y,x] == river):
                            state   = 1
                        else:
							# and keep it that way
                            if not state == 1:
                                state = 2
					# then for the road section
                    else:
                        if not (i % 6):
                            state = 1
                        else:
							# if there are any pixels which is the same color as the road,
                            # then mark it as unsafe
                            if not np.all(screen[y,x] == road):
                                state = 2
                            else:
								# and keep it that way
                                if not state == 2:
                                    state = 1
            if state == 3:
                loc = [i,j]
            if not ((len(row)-1) == j):
                row.append(state)
            # if the state is unsafe
            if state == 2:
                # if it is a row in which the cars move to the left
                # or the floaters move to the right
                if ((i == 1) or (i == 3) or (i == 4) or (i == 7) or (i == 9) or (i == 11)) and (not(j == 0)):
                    # then the spot to it's left is unsafe
                    row[j-1] = 2
        # go reverse through the list to safe-spot the cars heading in the other direction
        # so that we don't flood all entries to the right with false 'unsafe''s.
        for j, entry in reversed(list(enumerate(row))):
            if (not j == 0) and (entry == 1) and (row[j-1] == 2) and ((i == 8) or (i == 10)):
                row[j] = 2
        # frame smoothing does nothing, so I have to do that on my own
        # for the road
        if (2 not in row) and (i < 12) and (i > 6) and (len(prev)):
            row = prev[i]
        # and for the river
        if (1 not in row) and (i > 0) and (i < 6) and (len(prev)):
            row = prev[i]

        coll.append(row)

    # Print it out for reference's sake
    listee = []
    for i in range(len(coll)):
        lister = []
        for j in range(len(coll[0])):
            if (coll[i][j] == 1):
                lister.append(' ')
            elif (coll[i][j] == 2):
                lister.append('X')
            elif (coll[i][j] == 3):
                lister.append('F')
        listee.append(lister)

    if not found:
        loc = old_loc
    # print("mapper: frogger's location: %s" % loc)
    # print("mapper: current screen standing:")
    # for i in range(len(listee)):
    #    print(listee[i])
    # Return it!
    coll.append(loc)
    prev = coll
    return coll
