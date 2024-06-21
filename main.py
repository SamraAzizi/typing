import curses
from curses import wrapper



def main(stdscr):
    stdscr.clear()
    stdscr.addstr("it is a technology time where computers are normal!")
    stdscr.refresh()
    stdscr.getKey()


wrapper(main)
