#
# File Class
#
# @Author: Erick Rettozi

import os

class File():

    # ---------------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------------
    def __init__(self,file):
        self._file = file

    # ---------------------------------------------------------------
    # Checks whether file exists
    # @Private
    # ---------------------------------------------------------------
    def exists(self):
        return os.path.exists(self._file)
