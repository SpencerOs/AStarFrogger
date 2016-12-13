# open_cur.py
# Author: Spencer Ollila

# An A* Frogger solution where the
# first path that it finds is what it follows

from ale_python_interface   import ALEInterface
from mapper                 import set_guide
from search                 import a_star_sandbar
from search                 import a_sure

#returns the list of moves to make based off of the first screen
def open_loop(screen = [], loc = [], *args):
    #return a_star_sandbar(screen, loc, True, 0)
    return a_sure(screen, loc, True, 0)


def first_imp(ale = ALEInterface, episode_number = 1, *args):
    actions     = ale.getMinimalActionSet()
    a           = actions[0]
    count       = 0
    loc         = [12,9]
    lives       = ale.lives()
    for episode in range(episode_number):
        total_reward    = 0
        move_list       = []
        while not ale.game_over():
            screen = ale.getScreenRGB()
            # Check for the change in lives here before it tries and detects the empty list.
            if not lives == ale.lives():
                lives = ale.lives()
                # Tell it where it is and keep it busy while it goes through the death animation.
                loc = [12,9]
                move_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                #print('first_imp: I died!')
            # The game doesn't let you make a move until it is
            # done making you listen to it's little song
            # which goes on for about 450 frames
            if ale.getEpisodeFrameNumber() == 455:
                # Then grab the list of moves to make based off of the first 'play' frame.
                move_list = open_loop(screen, loc)
                loc = move_list.pop()
                for move in range(len(move_list)):
                    count += 1
            elif not(ale.getEpisodeFrameNumber() % 5) and (ale.getEpisodeFrameNumber() > 455):
                # if there are no more moves to make and somehow
                # the frog isn't dead, get a new list!
                if not len(move_list):
                    move_list = open_loop(screen, loc)
                    loc = move_list.pop()
                op = move_list.pop()
                a = actions[op]
            elif not((ale.getEpisodeFrameNumber() % 5) - 3) and (ale.getEpisodeFrameNumber() > 455):
                a = actions[0]
            reward = ale.act(a)
            total_reward += reward
        print('first_imp: Episode %d ended with score: %d' % (episode+1, total_reward))
        ale.reset_game()
