import asyncio
import time
import curses


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)


def draw(canvas):
    row, column = (5, 20)
    star_blink = blink(canvas, row, column)
    curses.curs_set(False)
    canvas.border()
    while True:
        try:
            star_blink.send(None)
            canvas.refresh()
        except StopIteration:
            break
    time.sleep(5)
    

if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
