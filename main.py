import curses
from curses import wrapper

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr( "Welcome To The Speed Typing Test")
    stdscr.addstr("\nPress Any Key To Begin")
    stdscr.refresh()
    stdscr.getkey()
    
    
def wpm_test(stdscr):
    target_text = "hello world this is some test text for this app!"
    current_text = []
    stdscr.clear()
    stdscr.addstr(target_text)
    stdscr.refresh()
    stdscr.getkey()



def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    start_screen(stdscr)


wrapper(main)
