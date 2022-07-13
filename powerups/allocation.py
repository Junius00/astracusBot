from random import randint
from constants.names import KEY_PUP_QUANTITY
import globals.env as g_env
from objects.Powerup import Powerup

def get_random_pup():
    pup_keys = list(g_env.PUP_TRACKER.keys())

    while pup_keys:
        i = randint(0, len(pup_keys) - 1)
        key = pup_keys[i]

        if g_env.PUP_TRACKER[key][KEY_PUP_QUANTITY] > 0:
            return Powerup(key)
        
        del pup_keys[i]
    
    return None
