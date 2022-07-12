import asyncio
import curses
from itertools import cycle
from random import choice, randint
import time

from courses_tools import draw_frame
from fire_animation import fire


STARS = "+*.:"
STAR_COUNT = 100
TIC_TIMEOUT = 0.1


async def blink(canvas, row, column, symbol="*"):
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


async def animate_spaceship(canvas, row, column, frames):
    frames = cycle(frames)
    frame = next(frames)
    
    while True:
        draw_frame(canvas, row, column, frame, negative=True)
        frame = next(frames)
        draw_frame(canvas, row, column, frame)
        canvas.refresh()
        await asyncio.sleep(0)


def draw(canvas):
    with open("animation/rocket_frame_1.txt", "r") as f1, open(
        "animation/rocket_frame_2.txt", "r"
    ) as f2:
        frames = (f1.read(), f2.read())

    x, y = canvas.getmaxyx()
    coroutines = []

    x_ship = x // 2 - 2
    y_ship = y // 2 - 2
    spaceship_coroutine = animate_spaceship(canvas, x_ship, y_ship, frames)
    coroutines.append(spaceship_coroutine)

    fire_coroutine = fire(canvas, start_row=x // 2, start_column=y // 2)
    coroutines.append(fire_coroutine)

    for _ in range(STAR_COUNT):
        coroutines.append(
            blink(
                canvas,
                row=randint(1, x - 2),
                column=randint(1, y - 2),
                symbol=choice(STARS),
            )
        )

    curses.curs_set(False)
    canvas.border()

    while True:

        for coroutine in coroutines:
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)

        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)
