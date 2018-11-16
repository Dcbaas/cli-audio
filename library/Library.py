import os
from collections import deque
#TODO Add an error check for when the files are wrong
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
    #TODO Check that the file exetension is correct
    #TODO Do better comments

    def __init__(self):
        """
        Initializes the Library class making an empty queue.

        param queue: The queue that will hold the playlist 
        """
        self.queue = deque()
    
    def change_tracks(self, pathname):
        #TODO make this not remove the old tracks but instead add to the front
        """
        Clears the track queue of all existing songs and adds the new
        track(s) to the play queue and returns the first song to be 
        played. If the path specified wasn't valid an error is thrown.

        param pathname: the pathname of the folder or song file being 
        added
        returns: a string indicating that the song has been added or not.
        """
        self.queue.clear()

        if os.path.isfile(pathname):
            self.queue.append(pathname)
            return 'Song changed'
        elif os.path.isdir(pathname):
            #do stuff
            self.queue = deque(
                [pathname + '/' + name 
                    for name in os.listdir(pathname)]
            )
            return 'Song changed'
        else:
            #throw an error
            return 'File or dierctory doesn\'t exist'

    def add_tracks(self, pathname):
        """
        Adds a new list of tracks to the existing queue of tracks. 
        If the path specified wasn't valid an error is thrown.

        param pathname: the pathname of the folder or song file being 
        added
        returns: a string indicating the song or songs have been added
        or not.
        """
        if os.path.isfile(pathname):
            self.queue.append(pathname)
            return 'Song added'
        elif os.path.isdir(pathname):
            self.queue.extend(
                [pathname + '/' + name for name in os.listdir(pathname)])
            return 'Songs added'
        else:
            #throw an error
            return 'The file or folder doesn\'t exist'
    
    def get_next_track(self):
        """
        Get the next track in the play queue.

        returns: the name of the next track
        """
        return self.queue.popleft()

    def list_tracks(self):
        """
        Get the list of tracks in the play queue. 

        returns: The list of tracks that are going to be played. 
        """
        return self.queue

        

        


