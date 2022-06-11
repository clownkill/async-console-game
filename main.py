import asyncio
import curses
from random import choice, randint
import time


STARS = '+*.:'


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(randint(1, 20)):
            await asyncio.sleep(0)
        
        canvas.addstr(row, column, symbol)
        for _ in range(randint(1, 20)):
            await asyncio.sleep(0)
       
        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(randint(1, 20)):
            await asyncio.sleep(0)
       
        canvas.addstr(row, column, symbol)
        for _ in range(randint(1, 20)):
            await asyncio.sleep(0)
        


def draw(canvas):
    x, y = canvas.getmaxyx()
    coroutines = []

    for _ in range(100):
        coroutines.append(blink(canvas, row=randint(1, x - 2), column=randint(1, y - 2), symbol=choice(STARS)))

    curses.curs_set(False)
    canvas.border()
    
    while True:
        for coroutine in coroutines:
            coroutine.send(None)
        canvas.refresh()
        time.sleep(0.1)
    

if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
