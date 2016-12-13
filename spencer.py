# spencer.py
# Author: Spencer Ollila

# This is the placeholder file with which I test bundling
# all of my other works together until I manage to clean
# them all up and package them in a better spot.

# EDIT: Ooooor, maybe I'll just keep them all here.
#       Typing my name every time I want to see something 
#       happen brings out the narcissist in me.

import sys
import numpy as np
from random                 import randrange
from ale_python_interface   import ALEInterface
from open_cur               import first_imp
from one_re_cur             import second_imp
from open_dy                import third_imp
from one_re_dy              import fourth_imp

ale = ALEInterface()
ale.setInt('random_seed', 123)

# color_averaging keeps the system from displaying objects on alternating
# frames. Setting it to true keeps me from having to also implement a memory
# into my detecting method. Enabling this, environment is a blend of the 
# last two frames.
ale.setBool('color_averaging', True)
ale.setInt('frame_skip', 1)
# Turn the sound on because why not!
ale.setBool('sound', False)
# Display the screen each time, because I am a masochist.
ale.setBool('display_screen', True)

ale.setInt('max_num_frames', 0)
ale.setInt('max_num_frames_per_episode', 0)
ale.setFloat('repeat_action_probability', 0)

# Load the ROM file
ale.loadROM("roms/frogger.bin")

#first_imp(ale, 3)
second_imp(ale, 1)
#third_imp(ale, 3)
#fourth_imp(ale)
