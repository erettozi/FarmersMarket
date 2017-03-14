#
# CSV Class
#
# @Author: Erick Rettozi

import csv

class CSV():

    # ---------------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------------
    def __init__(self,file):
        self._file = file
        self.__content = None
        self._parser()

    # ---------------------------------------------------------------
    # Returns an array with the contents of CSV file (already parsed)
    # @Public
    # ---------------------------------------------------------------
    @property
    def content(self):  
        return self.__content

    # ---------------------------------------------------------------
    # Parser CSV file
    # @Private
    # ---------------------------------------------------------------
    def _parser(self):
        self.__content = csv.DictReader(open(self._file))
