import curses
import curses.textpad

import sys

from library.Library import Library

class FrontEnd:

    def __init__(self, player):
        self.player = player
        self.player.play(sys.argv[1])
        self.library = Library()
        curses.wrapper(self.menu)

    def menu(self, args):
        self.stdscr = curses.initscr()
        self.stdscr.border()
        self.stdscr.addstr(0,0, "cli-audio",curses.A_REVERSE)
        self.stdscr.addstr(5,10, "c - Change current song")
        self.stdscr.addstr(6,10, "p - Play/Pause")
        self.stdscr.addstr(7,10, "q - Queue Songs")
        self.stdscr.addstr(8,10, "n - Next Song")
        self.stdscr.addstr(9,10, "l - List Queue")
        self.stdscr.addstr(10,10, "ESC - Quit")
        self.updateSong()
        self.stdscr.refresh()
        while True:
            c = self.stdscr.getch()
            if c == 27:
                self.quit()
            elif c == ord('p'):
                self.player.pause()
            elif c == ord('c'):
                self.changeSong()
                self.updateSong()
                self.stdscr.touchwin()
                self.stdscr.refresh()
            elif c == ord('q'):
                self.queueSong()
            elif c == ord('n'):
                self.nextSong()
                self.updateSong()
                self.stdscr.touchwin()
                self.stdscr.refresh()
            elif c == ord('l'):
                self.listQueue()  
    
    def updateSong(self):
        self.stdscr.addstr(15,10, "                                        ")
        self.stdscr.addstr(15,10, "Now playing: " + self.player.getCurrentSong())

    def changeSong(self):
        changeWindow = curses.newwin(5, 40, 5, 50)
        changeWindow.border()
        changeWindow.addstr(0,0, "What is the file path?", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        path = changeWindow.getstr(1,1, 30)
        curses.noecho()
        del changeWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()
        self.player.stop()
        self.player.play(path.decode(encoding="utf-8"))

    def nextSong(self):
        next = self.library.get_next_track()
        if next != False:
            self.player.stop()
            self.player.play(next)

    def queueSong(self):
        queueWindow = curses.newwin(5, 40, 5, 50)
        queueWindow.border()
        queueWindow.addstr(0,0, "What is the file path?", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        path = queueWindow.getstr(1,1, 30)
        curses.noecho()
        del queueWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()
        
        self.library.add_tracks(path.decode(encoding="utf-8"))

    def listQueue(self):
        queue = self.library.list_tracks()
        listWin = curses.newwin(len(queue), 40, 5, 50)
        for i in range(len(queue)):
            listWin.addstr(i, 0, queue[i])
        self.stdscr.refresh()
        curses.echo()
        listWin.getch()
        curses.noecho()
        del listWin
        self.stdscr.touchwin()
        self.stdscr.refresh()
        
    def quit(self):
        self.player.stop()
        exit()
