import asyncio
import curses
from random import randint
import time


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
    star1_blink = blink(canvas, row=5, column=20)
    star2_blink = blink(canvas, row=5, column=25)
    star3_blink = blink(canvas, row=5, column=30)
    star4_blink = blink(canvas, row=5, column=35)
    star5_blink = blink(canvas, row=5, column=40)

    coroutines = [
        star1_blink,
        star2_blink,
        star3_blink,
        star4_blink,
        star5_blink,
        ]

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
