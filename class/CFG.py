#
# CFG Class
#
# @Author: Erick Rettozi

import yaml

class CFG():

    # ---------------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------------
    def __init__(self,file):
        self._file = file
        self.__data = None
        self._parser()

    # ---------------------------------------------------------------
    # Returns an array with the contents of CFV file
    # @Public
    # ---------------------------------------------------------------
    @property
    def data(self):  
        return self.__data

    # ---------------------------------------------------------------
    # Parser CFV file
    # @Private
    # ---------------------------------------------------------------
    def _parser(self):
        fh = open(self._file)
        self.__data = yaml.safe_load(fh)
        fh.close()
