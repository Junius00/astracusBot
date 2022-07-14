import asyncio
        
def synchronous_run(func):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # 'RuntimeError: There is no current event loop...'
        loop = None

    if loop and loop.is_running():
        tsk = loop.create_task(func())
    else:
        asyncio.run(func())