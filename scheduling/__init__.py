from datetime import datetime as dt
from threading import Timer

def schedule_dt(run_at, action):
    delay = (run_at - dt.now()).total_seconds()
    Timer(delay, action).start()