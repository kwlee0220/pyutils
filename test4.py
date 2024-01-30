
from typing import Optional

import itertools
import time
# from threading import Thread, Event
from multiprocessing import Process, Event
from multiprocessing import synchronize
import asyncio


async def spin(msg:str) -> None:
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')
    
async def slow() -> int:
    await asyncio.sleep(3)
    return 42

def main() -> None:
    result = asyncio.run(supervisor())
    print(f'Answer: {result}')
    
async def supervisor() -> int:
    spinner = asyncio.create_task(spin('thinking'))
    print(f'spinner object: {spinner}')
    result = await slow()
    spinner.cancel()
    return result

if __name__ == '__main__':
    main()