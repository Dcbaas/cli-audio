"""
The series of CLI Exceptions facilitate error handling within the program.

Author: David Baas
Version 1.0 - 11/18/18
"""


class CLI_Audio_Exception(Exception):
    """
    The base exception class for the cli audio program. Never called 
    but used as a base class for the other two.
    """
    pass



class CLI_Audio_File_Exception(CLI_Audio_Exception):
    """
    This exception is used to trigger errors related to the 
    file being used to change track or start playing music. 
    """
    pass


class CLI_Audio_Screen_Size_Exception(CLI_Audio_Exception):
    """
    This exception is used to trigger error related to invalid screen 
    size at the start of the program. 
    """
    def __init__(self, message):
        self.message = message