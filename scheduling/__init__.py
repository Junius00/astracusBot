import asyncio
from datetime import datetime as dt
from threading import Timer

def schedule_dt(run_at, action):
    delay = (run_at - dt.now()).total_seconds()
    Timer(delay, action).start()

def schedule_dt_async(run_at, action_async):
    delay = (run_at - dt.now()).total_seconds()
    def run_async():
        asyncio.run(action_async())

    Timer(delay, run_async).start()
