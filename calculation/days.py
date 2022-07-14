from datetime import datetime as dt

from constants.days import DAY1_END, DAY1_START, DAY2_END, DAY2_START, DAY3_END, DAY3_START

#returns 1-3 if within day 1-3, else returns None
def get_day():
    now = dt.now()

    if now >= DAY1_START and now <= DAY1_END:
        return 1
    
    if now >= DAY2_START and now <= DAY2_END:
        return 2
    
    if now >= DAY3_START and now <= DAY3_END:
        return 3
    
    return None