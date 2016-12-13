# icarus.py
# Author: Spencer Ollila

# First work into coming up with a dynamic mapping model
# for the A* frogger project

import sys
import dill
import numpy as np
from ale_python_interface   import ALEInterface
from mapper                 import set_guide

ale = ALEInterface()
ale.setInt('random_seed', 123)

ale.setBool('color_averaging', True)
ale.setInt('frame_skip', 1)
ale.setBool('sound', False)
ale.setBool('display_screen', False)

ale.setInt('max_num_frames', 0)
ale.setInt('max_num_frames_per_episode', 0)
ale.setFloat('repeat_action_probability', 0)

# Finally time to load the ROM file
ale.loadROM("roms/frogger.bin")

# Now it's time to write some code
actions = ale.getMinimalActionSet()
a       = actions[0]
count   = 0
loc     = [12,9]
p_guide = []
time_map = []
for episode in range(1):
    total_reward = 0
    p_guide = set_guide(ale.getScreenRGB(), loc)
    while not ale.game_over():
        screen = ale.getScreenRGB()
        if not(ale.getEpisodeFrameNumber() % 5) and (ale.getEpisodeFrameNumber() > 450):
            #print("icarus: pre-frameNumber: %d" % ale.getEpisodeFrameNumber())
            count += 1
            guide   = set_guide(screen, loc)
            loc     = guide.pop()
            time_entry = [ale.getEpisodeFrameNumber(), guide]
            time_map.append(time_entry)
            # print("icarus: guide: " + str(guide))
            for i in range(len(guide)):
                if not np.all(p_guide[i] == guide[i]):
                    #print('icarus: difference in row %d' % i)
                    p_guide[i] = guide[i]
            #raw_input("Holding...")
            #print("icarus: post-frameNumber: %d" % ale.getEpisodeFrameNumber())
        #if ale.getEpisodeFrameNumber() > 1000:
        #    break
        reward = ale.act(a)
        total_reward += reward
    print('icarus: Episode ended on turn %d' % count)
    #with open('time_map.txt', 'wb') as f:
    #    dill.dump(time_map, f)
    with open('time_map.txt', 'rb') as f:
        new_map = dill.load(f)

    print('icarus: Map at frame 455 is %s' % new_map[0])
    print('icarus: Map at last frame is %s' % new_map.pop())
