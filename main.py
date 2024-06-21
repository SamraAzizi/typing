import curses
from curses import wrapper



def main(stdscr):
    stdscr.clear()
    stdscr.addstr("hey hasey")
    stdscr.refresh()
    stdscr.getKey()


wrapper(main)
