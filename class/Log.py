#
# Log Class
#
# @Author: Erick Rettozi

import logging

class LOG():

    # ---------------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------------
    def __init__(self,file):

        logging.basicConfig(filename=file,
                            level=logging.INFO,
                            format='%(asctime)s %(message)s',
                            datefmt='%Y-%m-%d %I:%M:%S %p -')

        self.__logging = logging

    # ---------------------------------------------------------------
    # Return object pointer
    # @Public
    # ---------------------------------------------------------------
    @property
    def logger(self):  
        return self.__logging
