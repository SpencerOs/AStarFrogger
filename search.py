# search.py
# Author: Spencer Ollila

# implements A* and A-sure search algorithms

from mapper     import set_guide
from moves      import get_moves
from toolbox    import priority_queue
from toolbox    import sandbar_distance
from toolbox    import goal_distance

def a_star_sandbar(screen = [], old_loc = [], loop = False, frame_num = 0, *args):
    # Performs A* on the frog in order to get the player to the half-way point
    # (the sandbar). Takes the screen and previous player's location, and
    # returns the move or set of moves to make as well as the player's new position.
    loc         = old_loc
    guide       = set_guide(screen, loc)
    loc         = guide.pop()

    dist        = sandbar_distance(loc)
    node        = []
    if frame_num:
        # Dynamic nodes are made up of location, move that got there,
        # the cost of the node (traveled + heuristic), the frame it
        # came from, and the parent of the current node (implicit list).
        node    = [loc, None, dist, frame_num, None]
    else:
        # Nodes are made up of location, move that got there,
        # the cost of the node (traveled + heuristic) and the
        # parent node of the current one(they're implicitly linked).
        node        = [loc, None, dist, None]

    frontier    = priority_queue()
    frontier.push(node, dist)

    explored    = []
    move        = 0
    move_list   = []
    if frame_num:
        while True:
            if frontier.is_empty():
                return None
            parent_node = frontier.pop()
            loc, move, this_cost, frame, grand_parent_node = parent_node
            if loc in explored:
                continue
            if not sandbar_distance(loc):
                while parent_node:
                    _, action, _, _, parent_node = parent_node
                    if not action == None:
                        if not loop:
                            move = action
                        else:
                            move_list.append(action)
                if loop:
                    move_list.append(loc)
                    return move_list
                else:
                    move = [move, loc]
                    return move
            explored.append(loc)

            for move in get_moves(guide, loc, frame):
                action, new_loc = move
                h_cost          = sandbar_distance(new_loc)
                new_cost        = 1 + h_cost
                next_frame      = 5 + frame
                child_node      = [new_loc, action, new_cost, next_frame, parent_node]
                if not((new_loc in explored) or (new_loc in frontier)):
                    frontier.push(child_node, new_cost)
                elif (new_loc in frontier):
                    frontier.push(child_node, new_cost)
    else:
        while True:
            if frontier.is_empty():
                return None
            parent_node = frontier.pop()
            loc, move, this_cost, grand_parent_node = parent_node
            if loc in explored:
                continue
            if not sandbar_distance(loc):
                while parent_node:
                    _, action, _, parent_node = parent_node
                    if not action == None:
                        if not loop:
                            move = action
                        else:
                            move_list.append(action)
                if loop:
                    move_list.append(loc)
                    return move_list
                else:
                    move = [move, loc]
                    return move
            explored.append(loc)
            

            for move in get_moves(guide, loc):
                action, new_loc = move
                h_cost          = sandbar_distance(new_loc)
                new_cost        = 1 + h_cost
                child_node      = [new_loc, action, new_cost, parent_node]
                if not((new_loc in explored) or (new_loc in frontier)):
                    frontier.push(child_node, new_cost)
                elif (new_loc in frontier):
                    frontier.push(child_node, new_cost)
                

def a_sure(screen = [], old_loc = [], loop = False, frame_num = 0, *args):
    # Takes the screen and the previous player's position as input
    # and returns either the next move to make or the set of moves
    # to make as well as the new position of the player.
    loc         = old_loc
    guide       = set_guide(screen, loc)
    loc         = guide.pop()
    closest     = [] # a list, with first element being h_cost, then the node

    dist        = goal_distance(loc, guide)
    # Nodes are made up of location, move that got there,
    # the cost of the node (traveled + heuristic), and the
    # parent node of the current one (they're implicitly linked).
    node        = [loc, None, dist, None]
    closest     = [dist, node]

    frontier    = priority_queue()
    frontier.push(node, dist)

    explored    = []
    move        = 0
    move_list   = []
    while True:
        if frontier.is_empty():
            parent_node = closest[1]
            while parent_node:
                loc, action, _, parent_node = parent_node
                if not action == None:
                    if not loop:
                        move = action
                    else:
                        move_list.append(action)
            #print("a_sure: incomplete move: " + str(move) + " from distance " + str(goal_distance(loc, guide)))
            if loop:
                move_list.append(loc)
                return move_list
            else:
                move = [move,loc]
                return move
        parent_node = frontier.pop()
        loc, move, this_cost, grand_parent_node = parent_node
        if loc in explored:
            continue
        if not goal_distance(loc, guide):
            while parent_node:
                loc, action, _, parent_node = parent_node
                if not action == None:
                    if not loop:
                        move = action
                    else:
                        move_list.append(action)
            #print("a_sure: complete move: " + str(move) + " from location: " + str(loc))
            if loop:
                move_list.append(loc)
                return move_list
            else:
                move = [move, loc]
                return move
        explored.append(loc)

        for new_move in get_moves(guide, loc, frame_num):
            new_action, new_loc = new_move
            # print("a_sure: new_action = " + str(new_action) + " new_loc = " + str(new_loc))
            new_h_cost          = goal_distance(new_loc, guide)
            new_cost            = 1 + new_h_cost
            this_child_node = [new_loc, new_action, new_cost, parent_node]
            if not((new_loc in explored) or (new_loc in frontier)) or (new_action == 0):
                #print("a_sure: checked location: " + str(new_loc))
                frontier.push(this_child_node, new_cost)
            elif(new_loc in frontier):
                #print("a_sure: re-entered location: " + str(new_loc))
                frontier.push(this_child_node, new_cost)
            if (new_h_cost < closest[0]):
                closest = [new_h_cost, this_child_node]
            elif (new_h_cost == closest[0]):
                if (new_cost < closest[1][2]):
                    closest = [new_h_cost, this_child_node]
