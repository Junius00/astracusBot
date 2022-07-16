import os, json
from random import randint
from constants.names import KEY_PUP_QUANTITY
from constants.powerups import PUP_INFO
import globals.env as g_env
from objects.Powerup import Powerup
from scheduling.tasks import PUP_FILENAME

def get_random_pup():
    pup_keys = list(g_env.PUP_TRACKER.keys())

    while pup_keys:
        i = randint(0, len(pup_keys) - 1)
        key = pup_keys[i]

        if g_env.PUP_TRACKER[key][KEY_PUP_QUANTITY] > 0:
            return Powerup(key)
        
        del pup_keys[i]
    
    return None

def load_pups():
    if os.path.exists(PUP_FILENAME):
        f = open(PUP_FILENAME, 'r')
        res = json.load(f)
        f.close()
        pups = PUP_INFO()
        for key, powerup in pups.items():
            powerup[KEY_PUP_QUANTITY] = res[key]
        return pups
    return PUP_INFO()
    