import sys,os
import curses
from time import gmtime, strftime

def formatMoney(v):
        return '{: 16.8f}'.format(round(v, 4))

def window(stdscr, balances, prices, balancesInEur, totalInEur, totalInvested, lastUpdate, refresh):
    k = 0
    cursor_x = 0
    cursor_y = 0

    stdscr.clear()
    stdscr.refresh()

    curses.start_color()
    WHITE = 1
    curses.init_pair(WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK)

    GREEN = 2
    curses.init_pair(GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)

    CYAN = 3
    curses.init_pair(CYAN, curses.COLOR_CYAN, curses.COLOR_BLACK)

    RED = 4
    curses.init_pair(RED, curses.COLOR_RED, curses.COLOR_BLACK)

    YELLOW = 5
    curses.init_pair(YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    RED_ON_WHITE = 6
    curses.init_pair(RED_ON_WHITE, curses.COLOR_RED, curses.COLOR_WHITE)

    BLUE_ON_WHITE = 7
    curses.init_pair(BLUE_ON_WHITE, curses.COLOR_BLUE, curses.COLOR_WHITE)    

    while (k != ord('q')):

        if k == ord('r'):
            updating = '--- UPDATING ---'
            offset = (width - 1 - len(updating)) / 2 
            stdscr.addstr(height-1, 0, ' '*offset, curses.color_pair(RED_ON_WHITE))
            stdscr.addstr(height-1, offset-1, '--- UPDATING ---', curses.color_pair(RED_ON_WHITE))
            stdscr.addstr(height-1, offset+len(updating), ' '*offset, curses.color_pair(RED_ON_WHITE))
            stdscr.refresh()
            refresh()
            return

        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        stdscr.addstr(0, 0, 'BALANCE', curses.color_pair(CYAN))
        stdscr.addstr(0, 30, 'EXCHANGE', curses.color_pair(CYAN))
        stdscr.addstr(0, 60, 'VALUE', curses.color_pair(CYAN))

        stdscr.attron(curses.color_pair(YELLOW))
        i = 0
        for i, c in enumerate(dict.keys(balances)):
            stdscr.addstr(i+1, 0, c + ' ' + formatMoney(balances.get(c, 0)))
            stdscr.addstr(i+1, 30, 'EUR ' + formatMoney(prices.get(c, 0)))
            stdscr.addstr(i+1, 60, 'EUR ' + formatMoney(balancesInEur.get(c, 0)))

        stdscr.addstr(i+2, 60, '--------------------', curses.color_pair(WHITE))

        stdscr.addstr(i+3, 54, 'Total', curses.color_pair(WHITE))
        stdscr.addstr(i+3, 60, 'EUR ' + formatMoney(totalInEur))

        stdscr.addstr(i+4, 51, 'Invested', curses.color_pair(WHITE))
        stdscr.addstr(i+4, 60, 'EUR ' + formatMoney(-totalInvested))

        stdscr.addstr(i+5, 53, 'Profit', curses.color_pair(WHITE))
        profit = balances.get('EUR', 0) + totalInEur - totalInvested
        stdscr.addstr(i+5, 60, 'EUR ' + formatMoney(profit), curses.color_pair(GREEN if profit > 0 else RED))

        stdscr.attron(curses.color_pair(BLUE_ON_WHITE))
        stdscr.addstr(height-1, 0, " " * (width - 1))        
        stdscr.addstr(height-1, 0, 'q: Exit   r: Refresh')
        stdscr.addstr(height-1, width-len(lastUpdate)-1, lastUpdate)

        stdscr.move(cursor_y, cursor_x)
        stdscr.refresh()
        k = stdscr.getch()

class Gui:
    def __init__(self, totalInvested, check):
        self.totalInvested = totalInvested
        self.check = check
        self.lastUpdate = None

    def render(self):
        balances, prices, balancesInEur, totalInEur = self.check()
        self.lastUpdate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        curses.wrapper(window, balances, prices, balancesInEur, totalInEur, self.totalInvested, self.lastUpdate, lambda: self.render())
