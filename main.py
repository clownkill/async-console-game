import asyncio
import curses
from itertools import cycle
import os
from random import choice, randint
import time

from courses_tools import draw_frame, read_controls, get_frame_size
from fire_animation import fire

STARS = "+*.:"
STAR_QUANTITY = 100
TIC_TIMEOUT = 0.1
SPACESHIP_SPEED = 5


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


async def animate_spaceship(canvas, y, x, frames):
    length, width = get_frame_size(frames[0])

    row = x // 2
    column = y // 2 - width // 2

    for frame in cycle(frames):
        r_direction, c_direction, space_pressed = read_controls(
            canvas, direction_size=SPACESHIP_SPEED
        )
        row += r_direction
        column += c_direction

        if row + length >= x:
            row = x - length - 1

        if column + width >= y:
            column = y - width - 1

        if row - length < -length:
            row = 1

        if column - width < -width + 1:
            column = 1

        for _ in range(2):
            draw_frame(
                canvas,
                row,
                column,
                frame,
                negative=_,
            )
            await asyncio.sleep(0)


def draw(canvas):
    curses.curs_set(False)
    canvas.border()
    canvas.nodelay(True)

    frames = []
    animation_path = "./animation/"
    for file_name in os.listdir(animation_path):
        with open(animation_path + file_name, "r") as f:
            frame = f.read()
            frames.append(frame)

    x, y = canvas.getmaxyx()
    coroutines = []

    spaceship_coroutine = animate_spaceship(canvas, y, x, frames)
    coroutines.append(spaceship_coroutine)

    fire_coroutine = fire(canvas, start_row=x // 2, start_column=y // 2)
    coroutines.append(fire_coroutine)

    for _ in range(STAR_QUANTITY):
        coroutines.append(
            blink(
                canvas,
                row=randint(1, x - 2),
                column=randint(1, y - 2),
                symbol=choice(STARS),
            )
        )

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)

        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)
