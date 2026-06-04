# # from .ascii_converter import frame_to_ascii_color_fast
# import curses

# PLAYING = True
# PAUSED = False

# def _key(stdscr):
#     stdscr.nodelay(True)
#     key = stdscr.getch()
#     if key == -1:
#         return None
#     return key

# def controls():
#     stdscr = curses.initscr()
#     curses.cbreak()
#     stdscr.keypad(True)

#     while True:
#         key = _key(stdscr)
#         if key is not None:
#             if key == ord('q'):
#                 return "QUIT"
#             if key == curses.KEY_LEFT:
#                 return "LEFT"
#             if key == curses.KEY_RIGHT:
#                 return "RIGHT"
#             if key == ord(' '):
#                 return "SPACE"

from select import select
import sys


def get_key():
    dr, _, _ = select([sys.stdin], [], [], 0)
    if dr:
        return sys.stdin.read(1)
    return None