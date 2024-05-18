from backend.server.server import async_start as server_start
from backend.translate_server.server import async_start as translate_server_start
import asyncio

async def manage_task(tasks : list[asyncio.Task]):
    while (True):
        done = True
        for task in tasks:
            if (not task.done()):
                done = False
        if (done == True):
            print('All {} server started'.format(len(tasks)))
            break
        await asyncio.sleep(0.25)

def start():
    loop = asyncio.get_event_loop()
    start_tasks = []
    start_tasks.append(loop.create_task(server_start()))
    start_tasks.append(loop.create_task(translate_server_start()))
    loop.create_task(manage_task(start_tasks))
    loop.run_forever()

