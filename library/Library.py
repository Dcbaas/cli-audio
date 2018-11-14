import os
from collections import deque

class Library:
    """
    The Library class holds a list of all the songs to be played 
    by the player. It does this by keeping track of the names of 
    song files inside a list. There are three basic operations
    1) Start a specfic individual song or directory list of songs.
    This is accoplished by inputting the name of the song file or the 
    name of a directory contianing song files. In either case the
    songs will be added to the queue list and will be played in the
    order they are added. 
    2) Add a queue of songs to be played later.

    All songs are stored in the queue list which determines which song
    is played next.
    """

    def __init__(self):
        """
        Initializes the Library class making an empty queue.
        """
        self.queue = deque()
    
    def change_tracks(self, pathname):
        self.queue.clear()

        #TODO Add an error check for when the path doesn't exist
        if os.path.isfile(pathname):
            self.queue.append(pathname)
        elif os.path.isdir(pathname):
            #do stuff
            deque(
            map(lambda name: pathname + '/' + name, os.listdir(pathname))
            )
        else:
            #throw an error
            print("error work on execption")

        

        


