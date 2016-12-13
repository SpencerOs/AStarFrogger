# one_re_cur.py
# Author: Spencer Ollila

# An A* Frogger agent where the first time
# the screen becomes visible, the plan of
# attack is formulated and the step carried out
# and then re-evaluated over the same map.

from ale_python_interface   import ALEInterface
from mapper                 import set_guide
from search                 import a_star_sandbar
from search                 import a_sure

#returns the next move to make based off of the screen
def one_step_replan(screen = [], loc = [], *args):
    #return a_star_sandbar(screen, loc, False, 0)
    return a_sure(screen, loc, False, 0)

def second_imp(ale = ALEInterface, episode_number = 1, *args):
    actions = ale.getMinimalActionSet()
    a       = actions[0]
    count   = 0
    loc     = [12,9]
    for episode in range(episode_number):
        total_reward = 0
        while not ale.game_over():
            # The game does not permit you to move until it
            # is done with it's song
            if not(ale.getEpisodeFrameNumber() % 5) and (ale.getEpisodeFrameNumber() > 450):
                count  += 1
                screen  = ale.getScreenRGB()
                num     = one_step_replan(screen, loc)
                loc     = num.pop()
                num     = num[0]
                a       = actions[num]
            elif not((ale.getEpisodeFrameNumber() % 5) -3) and (ale.getEpisodeFrameNumber() > 450):
                a = actions[0]
            reward      = ale.act(a)
            total_reward += reward
        print('second_imp: Episode %d ended with score: %d' % (episode+1, total_reward))
        ale.reset_game()
