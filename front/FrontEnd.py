import curses
import curses.textpad

import sys

from exception import CLI_Exception

from library.Library import Library

class FrontEnd:
    """
    The FrontEnd Class handles the cli gui for the user to interact with.
    It presents an interface that shows the current song being played 
    while also presenting options for the user to take if they wish. 
    The gui runs through a curse wrapper until the user quits the program

    Author: Ira Woodring, David Baas
    Version: 1.0 - 11

    Attributes:
    player: The audio player for the cli
    library: The playlist queue for the cli
    stdscr: The gui object for the cli
    """
    def __init__(self, player):
        """
        Initializes the player and the library and creates the 
        curse gui allowing the menu function to take over.
        If the screen size of the terminal is too small for some reason,
        A exception for screen size will be thrown and the program will
        stop.

        param player: The player for this FrontEnd.
        throws: CLI_Audio_Screen_Size_Exception if the screen size 
        is too small
        """
        if len(sys.argv) != 2:
            print("./cli-audio <song name>")
            exit()
        try: 
            self.player = player
            self.player.play(sys.argv[1])
            self.library = Library()
            curses.wrapper(self.menu)
        except Exception:
            raise CLI_Exception.CLI_Audio_Screen_Size_Exception
            ('Screen Size to Small')

    def menu(self, args):
        """
        The menu function is the driver for the FrontEnd gui. It
        creates a cli interface for the user to interact with and 
        runs the event loop to track user inputs. 
        The commands are:

        p: play/pause
        c: change the song
        q: queue songs: this can take a file or a folder as an input
        n: play the next song
        l: list the songs in the queue
        ESC: quit program.
        """
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
        """
        Updates the title listed as the song playing
        This takes place even if the song is invalid and not playing.
        """
        self.stdscr.addstr(15,10, "                                        ")
        self.stdscr.addstr(15,10, "Now playing: " + self.player.getCurrentSong())

    def changeSong(self):
        """
        Changes the song currently playing to a song of the users choice.
        This is achieved in two ways. First is by typing the path of a 
        song file (relative or absolute) or by typing in the name of a 
        folder containing songs. If the latter method is used then a
        prompt is displayed to ask which song from the list of files
        the user wants played. This method catches an exception related
        to the audio file if something goes wrong. 
        """
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
        #self.player.play(path.decode(encoding = "utf-8"))
        try: 
            changeList = self.library.changeTrack(path.decode(encoding="utf-8"))
            changeListLen = len(changeList)           
            if changeListLen == 1:
                self.player.play(path.decode(encoding = "utf-8"))
            else:
                listWin = curses.newwin(changeListLen + 1, 100, 5, 50)
                #list the song options
                for i in range(changeListLen):
                    listWin.addstr(i, 0, changeList[i])
                
                listWin.addstr(changeListLen, 0, "Select Song, j = DOWN, k = UP ")
                i = 0
                ch = None
                while ch != ord('\n'):
                    listWin.addstr(i, 0, changeList[i], curses.A_REVERSE)
                    self.stdscr.refresh()
                    ch = listWin.getch()
                    if ch == ord('j') and i + 1 < changeListLen:
                        listWin.addstr(i, 0, changeList[i])
                        i = i + 1
                    elif ch == ord('k') and i - 1 >= 0:
                        listWin.addstr(i, 0, changeList[i])
                        i = i - 1
                
                #play the selected song
                self.player.play(changeList[i])
        except CLI_Exception.CLI_Audio_File_Exception:
            self.printError('The file or folder does not exist')
                    
    def nextSong(self):
        """
        Cycles the player to the next song queued in the library.
        This method handles a file exception when the library list
        is empty.
        """
        try:
            next = self.library.get_next_track()
            self.player.stop()
            self.player.play(next)
        except CLI_Exception.CLI_Audio_File_Exception:
            self.printError('The queue is empty')

    def queueSong(self):
        """
        This method allows the user to queue up a series of songs for 
        later play. This is achieved in two ways. First by specify the 
        path of an audio file or specifying the name of a directory
        both means of adding to the queue will add to the queue. If 
        the directory method is used then all the contents of the 
        directory will be added to the queue. This method handles
        file exceptions for when an invalid file or folder name is 
        given by the user.
        """
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
        
        try:
            self.library.add_tracks(path.decode(encoding="utf-8"))
        except CLI_Exception.CLI_Audio_File_Exception:
            self.printError('Error queueing file or folder')

    def listQueue(self):
        """
        Prints a list of queue songs to the user. This is done by 
        asking for the whole queue of songs in the libray and printing 
        them to the screen. If the queue is empty a message indicating 
        such will be displayed. 
        """

        queue = self.library.list_tracks()
        if len(queue) > 0:
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
        else:
            self.printError('Nothing to list')
        
    def printError(self, message):
        """
        If an error occurs weather an exception or otherwise, an error 
        message is printed to the user explaining the error. The only
        error that cant be handled such as a screen exception the 
        program just won't run.

        param: message: The error message being displayed.
        returns: nothing
        """
        errorWindow = curses.newwin(5, 40, 5, 50)
        errorWindow.border()
        errorWindow.addstr(2,2, message)
        self.stdscr.refresh()
        curses.echo()
        errorWindow.getch()
        curses.noecho()
        del errorWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()

    def quit(self):
        """
        Exits the cli program and also stops the player. 
        """
        self.player.stop()
        exit()
