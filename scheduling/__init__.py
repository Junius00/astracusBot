import asyncio
from datetime import datetime as dt
from threading import Timer

def schedule_dt(run_at, action, *args, **kwargs):
    delay = (run_at - dt.now()).total_seconds()
    Timer(delay, action, args=args, kwargs=kwargs).start()

def schedule_dt_async(run_at, action_async, *args, **kwargs):
    delay = (run_at - dt.now()).total_seconds()
    def run_async():
        asyncio.run(action_async(*args, **kwargs))

    Timer(delay, run_async).start()
