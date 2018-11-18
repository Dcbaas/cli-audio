"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time
from exception import CLI_Exception

class Player:
    """
    The Player class is the driver for playing music in the cli. It
    handles the playing pausing and stopping of music. This is done by
    what appears to be steaming a file into an audio stream. It is done 
    in the background in a different thread.
    """
    def __init__(self):
        """
        Initializes the player wth no song playing and the status as 
        paused.
        """
        self.currentSong = "Nothing playing."
        self.paused = True
        self.position = 0

    def getCurrentSong(self):
        """
        Gets the name of the current song playing
        returns: The name of the song playing. 
        """
        return self.currentSong

    def pause(self):
        """
        Toggles weather the player is paused or not. If it is paused, 
        then the stream is stopped and the song is paused at its current
        position.
        """
        if self.paused == False:
            self.paused = True
            self.stream.stop_stream()
        else:
            self.paused = False
            self.stream.start_stream()

    def play(self, track):
        """
        Takes the specified file and plays the audio file at the specified
        location. This is done by created a stream variable that sterams
        the contents of the file though pyaudio. There is also a callback
        function that is called to update where the stream is in the file.

        param track: The audio file that will be played by this player.
        """
        try:
    
            self.paused = False
            self.currentSong = track
            self.wf = wave.open(track, 'rb')

            # instantiate PyAudio (1)
            self.p = pyaudio.PyAudio()

            # open self.stream using callback (3)
            self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                    channels=self.wf.getnchannels(),
                    rate=self.wf.getframerate(),
                    output=True,
                    stream_callback=self.callback)

            # start the self.stream (4)
            self.stream.start_stream()
        except Exception as err:
            raise CLI_Exception.CLI_Audio_File_Exception
            ('Error with file' + err)

    def stop(self):
        """
        Stops the entire stream that is playing an audio file. After this
        member function is called, the audio file cannot be restarted
        """
        self.stream.stop_stream()
        self.stream.close()
        self.wf.close()

        self.p.terminate() 

    def callback(self, in_data, frame_count, time_info, status):
        """
        The callback function is used to read the data at the given part
        of the file stream.
        """
        data = self.wf.readframes(frame_count)
        return (data, pyaudio.paContinue)
