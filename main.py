import asyncio
import curses
from itertools import cycle
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
    frameset = cycle(frames)
    frame = next(frameset)

    row = x // 2 - 2
    column = y // 2 - 2

    framesize = get_frame_size(frame)
    length, width = framesize

    while True:
        draw_frame(canvas, row, column, frame, negative=True)

        r_direction, c_direction, space_pressed = read_controls(canvas, direction_size=SPACESHIP_SPEED)
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

        draw_frame(
            canvas,
            row,
            column,
            frame,
            negative=True,
        )
        frame = next(frameset)
        draw_frame(canvas, row, column, frame)
        canvas.refresh()

        await asyncio.sleep(0)


def draw(canvas):
    curses.curs_set(False)
    canvas.border()
    canvas.nodelay(True)
    canvas.refresh()

    with open("animation/rocket_frame_1.txt", "r") as f1, open(
        "animation/rocket_frame_2.txt", "r"
    ) as f2:
        frames = (f1.read(), f2.read())

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
        for coroutine in coroutines:
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)

        time.sleep(TIC_TIMEOUT)


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)
