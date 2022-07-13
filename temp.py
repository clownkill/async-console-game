import time
import curses


def draw(canvas):
    row, column = (0, 0)
    canvas.addstr(row, column, 'Hello world')
    canvas.refresh()
    time.sleep(1)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
