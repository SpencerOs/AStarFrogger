# one_re_dy.py
# Author: Spencer Ollila

# An A* Frogger solution where the screen is 
# taken in as input, a turn is decided based on
# an evolving map, and then the cycle continues
# every five frames. If you are on a laptop, buckle up.

from ale_python_interface   import ALEInterface
from mapper                 import set_guide
from search                 import a_star_sandbar
from search                 import a_sure

# returns the next move to make based off of the map through time
def one_step_replan(screen = [], loc = [], frame = 0, *args):
    #return a_star_sandbar(screen, loc, False, frame)
    return a_sure(screen, loc, False, frame)

def fourth_imp(ale = ALEInterface, episode_number = 1, *args):
    actions = ale.getMinimalActionSet()
    a       = actions[0]
    count   = 0
    loc     = [12,9]
    for episode in range(episode_number):
        total_reward    = 0
        while not ale.game_over():
            frame       = ale.getEpisodeFrameNumber()
            # Let the game do it's thing before it lets you move.
            # It's like standing and waiting for Frogger's national anthem
            if  not(frame % 5) and (frame > 450):
                count   += 1
                screen  = ale.getScreenRGB()
                num     = one_step_replan(screen, loc, frame)
                loc     = num.pop()
                num     = num[0]
                a       = actions[num]
            elif not((frame % 5) - 3) and (frame > 450):
                a       = actions[0]
            reward      = ale.act(a)
            total_reward+= reward
        print('fourth_imp: Episode %d ended with score: %d' % (episode+1, total_reward))
        ale.reset_game()
