import os
from collections import deque
from exception import CLI_Exception
#TODO Add an error check for when the files are wrong
class Library:
    """
    The Library class holds a list of all the songs to be played 
    by the player. It does this by keeping track of the names of 
    song files inside a list. There are three basic operations
    1) Start a specific individual song or directory list of songs.
    This is accomplished by inputting the name of the song file or the 
    name of a directory contianing song files. In either case the
    songs will be added to the queue list and will be played in the
    order they are added. 
    2) Add a queue of songs to be played later.

    All songs are stored in the queue list which determines which song
    is played next.
    """
    #TODO Check that the file extension is correct
    #TODO Do better comments

    def __init__(self):
        """
        Initializes the Library class making an empty queue.

        param queue: The queue that will hold the playlist 
        """
        self.queue = deque()

    def changeTrack(self, pathname):
        """
        Looks that the path specified by the user and determines if it 
        either a file or a folder. If the path is a file then it is 
        returned to the front end to allow it to be played. If the path
        is a folder then the list of files inside are returned to the 
        FrontEnd to allow the user to select the song from the list.
        If the path isn't valid then a file exception is thrown.

        param pathname: The path specified by the user.
        returns: The pathname if the path is a file or a list if the path
        is a folder.
        throws CLI_Audio_File_Exception if the path is invalid
        """
        if os.path.isfile(pathname):
            return [pathname]
        elif os.path.isdir(pathname):
            return [pathname + '/' + name for name in os.listdir(pathname)]
        else:
           raise CLI_Exception.CLI_Audio_File_Exception
    
    def add_tracks(self, pathname):
        """
        Adds a new list of tracks to the existing queue of tracks. 
        If the path specified wasn't valid an error is thrown.

        param pathname: the pathname of the folder or song file being 
        added
        returns: a string indicating the song or songs have been added
        or not.
        """
        #check to see if it is a relative path from Home directory
        if pathname.startswith('~/'):
            pathname.lstrip('~/')
        if os.path.isfile(pathname):
            self.queue.append(pathname)
            return 'Song added'
        elif os.path.isdir(pathname):
            self.queue.extend(
                [pathname + '/' + name for name in os.listdir(pathname)])
            return 'Songs added'
        else:
            #throw an error
            raise CLI_Exception.CLI_Audio_File_Exception

            
    def get_next_track(self):
        """
        Get the next track in the play queue if the queue isn't empty.
        If the queue is empty than an exception is thrown. 

        returns: the name of the next track
        """
        if len(self.queue ) > 0:
            return self.queue.popleft()
        else:
            raise CLI_Exception.CLI_Audio_File_Exception

    def list_tracks(self):
        """
        Get the list of tracks in the play queue. 

        returns: The list of tracks that are going to be played. 
        """
        return self.queue
