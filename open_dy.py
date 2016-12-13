# open_dy.py
# Author: Spencer Ollila

# An A* Frogger solution where the first
# path that it finds over a dynamic map
# creates the path that it follows.

from ale_python_interface   import ALEInterface
from mapper                 import set_guide
from search                 import a_star_sandbar
from search                 import a_sure

# returns the set of moves to make based off of the map through time
def open_loop(screen = [], loc = [], frame = 0, *args):
    #return a_star_sandbar(screen, loc, True, frame)
    return a_sure(screen, loc, True, frame)

def third_imp(ale = ALEInterface, episode_number = 1, *args):
    actions     = ale.getMinimalActionSet()
    a           = actions[0]
    count       = 0
    loc         = [12,9]
    lives       = ale.lives()
    for episode in range(episode_number):
        total_reward    = 0
        move_list       = []
        while not ale.game_over():
            frame   = ale.getEpisodeFrameNumber()
            screen  = ale.getScreenRGB()
            # Check for lives here before it starts trying to reassign stuff with the empty list and mess us up
            if not lives == ale.lives():
                # If the character has died, let them just hang out for the next 100 frames
                lives   = ale.lives()
                #print('third_imp: I died at %s and all I got was this stupid print statement' % loc)
                loc     = [12,9]
                move_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            # Let it wrap up the intro before you start
            if frame == 455:
                move_list = open_loop(screen, loc, frame)
                loc = move_list.pop()
                for move in range(len(move_list)):
                    count += 1
            elif not(frame % 5) and (frame > 455):
                # if there are no more moves to make and the frog isn't dead
                # make a new list!
                if not len(move_list):
                    move_list   = open_loop(screen, loc, frame)
                    loc         = move_list.pop()
                op  = move_list.pop()
                a   = actions[op]
            elif not((frame % 5) - 3) and (frame > 455):
                a   = actions[0]
            reward  = ale.act(a)
            total_reward += reward
        print('third_imp: Episode %d ended with score: %d' % (episode+1, total_reward))
        ale.reset_game()
