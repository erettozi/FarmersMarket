#
# DB Class
#
# @Author: Erick Rettozi

import sys
import os
import warnings
import re
import mysql.connector
from mysql.connector import errorcode

class DB():

    # ---------------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------------
    def __init__(self,type,host,usr,pwd,db):
        self._type = type
        self._host = host
        self._usr = usr
        self._pwd = pwd
        self._db = db
        self._conn = None
        self.__rowcount = None

    # ---------------------------------------------------------------
    # Rowcount
    # @Public
    # ---------------------------------------------------------------
    @property
    def rowcount(self):
        return self.__rowcount

    # ---------------------------------------------------------------
    # Connect to database
    # @Public
    # ---------------------------------------------------------------
    def connect(self):
        # Prepared to connect to MySQL database only for now
        if self._type == 'mysql':
            self._mysqlConnect()
        else:
            warnings.warn("The database type is not valid")

    # ---------------------------------------------------------------
    # Disconnect to database
    # @Public
    # ---------------------------------------------------------------
    def disconnect(self):
        # Prepared to disconnect to MySQL database only for now
        if self._type == 'mysql':
            self._mysqlDisconnect()
        else:
            warnings.warn("The database type is not valid")

    # ---------------------------------------------------------------
    # Execute the SQL statement
    # @Public
    # ---------------------------------------------------------------
    def execute(self,query,multiQuery=False,fetchAll=False):
        #if not bool(query and query.strip()) or (query is None):
        #    warnings.warn("There is no SQL statement to execute")
        #    sys.exit(os.EX_SOFTWARE)

        if bool(query and query.strip()) and not (query is None):
            # Prepared to execute only statements to the MySQL database for now
            if self._type != 'mysql':
                warnings.warn("The database type is not valid")
                sys.exit(os.EX_SOFTWARE)

            # Query is SELECT?
            match = re.search('select|update', query.lower())

            # Variable used to return the result of the query when it is of type SELECT.
            # The format of the result is of type dict (HASH)
            hash = {}

            cursor = self._conn.cursor(buffered = True)

            # If the query is of type INSERT, then I execute in multi=True
            if match:
                cursor.execute(query)
            elif not match:
                if multiQuery is True:
                    for result in cursor.execute(query,multi=True):
                        pass
                else:
                    cursor.execute(query)

            # If query is not SELECT
            if not match:
                self._conn.commit()

            # If query is SELECT
            if match:
                if not fetchAll:
                    data = cursor.fetchone()
                    if not (data is None):
                        desc = cursor.description
                        for (name, value) in zip(desc, data):
                            hash[name[0]] = value
                elif fetchAll:
                    desc = [d[0] for d in cursor.description]
                    hash = [dict(zip(desc, row)) for row in cursor.fetchall()]

            self.__rowcount = cursor.rowcount
            cursor.close()

            # If query is SELECT
            if match:
                return hash

    # ---------------------------------------------------------------
    # MySQL Connect
    # @Private
    # ---------------------------------------------------------------
    def _mysqlConnect(self):
        try:
            self._conn = mysql.connector.connect(host=self._host,
                                                 user=self._usr,
                                                 password=self._pwd,
                                                 database=self._db,
                                                 raise_on_warnings=True)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
               print("User or password is wrong\n")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
               print("Database does not exist\n")
            else:
               print(err)

    # ---------------------------------------------------------------
    # MySQL Disconnect
    # @Private
    # ---------------------------------------------------------------
    def _mysqlDisconnect(self):
        self._conn.close()
