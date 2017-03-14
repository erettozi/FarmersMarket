#
# Class to export CSV data from farmers markets to database
#
# @Author: Erick Rettozi

import re
import sys
import os
sys.path.append('../class')

from CSV import CSV
from CFG import CFG
from File import File
from DB import DB
from Log import LOG

class CSV2DB():

    # ---------------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------------
    def __init__(self,argv):

        cfg = CFG('../cfg/farmersmarket.yaml')

        # Open connection database
        self._db = DB(cfg.data['db']['type'],
                      cfg.data['db']['host'],
                      cfg.data['db']['user'],
                      cfg.data['db']['pass'],
                      cfg.data['db']['dbname'])

        self._db.connect()

        # Set CSV file path
        self._file = argv[1]

        # Set log file
        self._log = LOG('../log/export-CSV2DB.log')
        self._log.logger.info('Opening connection to the database')

    # ---------------------------------------------------------------
    # Destructor
    # ---------------------------------------------------------------
    def destroy(self):
        # Disconnect database
        self._db.disconnect()

        self._log.logger.info('Connection to finished database')

    # ---------------------------------------------------------------
    # Starts exporting the CSV file to database
    # @Public
    # ---------------------------------------------------------------
    def run(self):
        if( self.runExportRelationalEntities() is True and
            self.runExportFarmerMarket() is True ):

            self._log.logger.info('The CSV file was successfully exported to database')
            return True
        else:
            self._log.logger.info('ERROR when exporting the CSV file to the database')
            return False

    # ---------------------------------------------------------------
    # Export district, subprefecture, neighborhood, region5 and region8
    # @Public
    # ---------------------------------------------------------------
    def runExportRelationalEntities(self):
        # Start the necessary preparation and processing of data-
        # for insertion into database
        return self._insertDataIntoRelationalEntities(self._parserCSVFile().content)

    # ---------------------------------------------------------------
    # Export farmer market list
    # @Public
    # ---------------------------------------------------------------
    def runExportFarmerMarket(self):
        return self._insertDataIntoFarmerMarket(self._parserCSVFile().content)

    # ---------------------------------------------------------------
    # Parser CSV File
    # @Private
    # ---------------------------------------------------------------
    def _parserCSVFile(self):
        # I get first argument passed in command line, in this case,
        # the PATH of CSV file
        csvFile = File(self._file)

        # If file does not exist, then print a message warning the-
        # user and stop running program
        if csvFile.exists() == False:
           print("File not found: %s",csvFile._file)
           sys.exit(os.EX_SOFTWARE)

        # Parser CSV File
        self._log.logger.info('Parser CSV File')
        return CSV(csvFile._file)
 
    # ---------------------------------------------------------------
    # Insert data into relational entities
    # @Private
    # ---------------------------------------------------------------
    def _insertDataIntoRelationalEntities(self,content):

        try:
            for row in content:
                # If the value of the hash key is None, then replaced by ' '
                for k,v in row.items():
                    if(row[k] == ''):
                        row[k] = None

                    if(row[k] is None):
                        break

                self._districtPrepareMaybeInsert(row['CODDIST'],row['DISTRITO'])
                self._subPrefecturePrepareMaybeInsert(row['CODSUBPREF'],row['SUBPREFE'])
                self._neighborhoodPrepareMaybeInsert(row['BAIRRO'])
                self._region5PrepareMaybeInsert(row['REGIAO5'])
                self._region8PrepareMaybeInsert(row['REGIAO8'])

        except Exception as ex:
            self._log.logger.info('ERROR inserting Relational Entities into database. ERRO: ' + str(ex))
            print(ex)
            return False

        finally:
            self._log.logger.info('Relational Entities Successfully inserted into Database')
            return True

    # ---------------------------------------------------------------
    # Insert data into farmer market.
    # Use multi=True property MySQL Connector
    # @Private
    # ---------------------------------------------------------------
    def _insertDataIntoFarmerMarket(self,content):

        multiFarmerMarketInsertQuery = ''
        
        for row in content:
            # If the value of the hash key is None, then replaced by ' '
            for k,v in row.items():
                if(row[k] == ''):
                    row[k] = None

                if(row[k] is None):
                    break

            query = self._farmerMarketPrepareMaybeInsert(
                                        row['ID'],row['LONG'],row['LAT'],
                                        row['SETCENS'],row['AREAP'],row['NOME_FEIRA'],
                                        row['REGISTRO'],row['LOGRADOURO'],row['NUMERO'],
                                        row['REFERENCIA'],row['CODDIST'],row['CODSUBPREF'],
                                        row['REGIAO5'],row['REGIAO8'],row['BAIRRO'])

            if(not (query is None)):
                multiFarmerMarketInsertQuery += str(query) + ';'

        try:
            # I execute the queries. Set multi=True
            self._db.execute(multiFarmerMarketInsertQuery,multiQuery=True)
        except Exception as ex:
            self._log.logger.info('ERROR inserting farmers market into database. ERRO: ' + str(ex))
            print(ex)
            return False
        finally:
            self._log.logger.info('Farmers Market Successfully inserted into Database')
            return True

    # ---------------------------------------------------------------
    # Prepares the query for insertion of the data of the-
    # subprefecture in the Database, if it does not exist
    # @Private
    # ---------------------------------------------------------------
    def _subPrefecturePrepareMaybeInsert(self,id,value):
        self._prepareInsertValueInTable('SubPrefecture',
                                        'subPrefectureID',
                                        'subPrefectureName',
                                        id,
                                        value,
                                        True)

    # ---------------------------------------------------------------
    # Prepares the query for insertion of the data of the-
    # district in the Database, if it does not exist
    # @Private
    # ---------------------------------------------------------------
    def _districtPrepareMaybeInsert(self,id,value):
        self._prepareInsertValueInTable('District',
                                        'districtID',
                                        'districtName',
                                        id,
                                        value,
                                        True)

    # ---------------------------------------------------------------
    # Prepares the query for insertion of the data of the-
    # neighborhood in the Database, if it does not exist
    # @Private
    # ---------------------------------------------------------------
    def _neighborhoodPrepareMaybeInsert(self,value):
        self._prepareInsertValueInTable('Neighborhood',
                                        None,
                                        'neighborhoodName',
                                        None,
                                        value,
                                        True)

    # ---------------------------------------------------------------
    # Prepares the query for insertion of the data of the-
    # region5 in the Database, if it does not exist
    # @Private
    # ---------------------------------------------------------------
    def _region5PrepareMaybeInsert(self,value):
        self._prepareInsertValueInTable('Region5',
                                        None,
                                        'region5Name',
                                        None,
                                        value,
                                        True)

    # ---------------------------------------------------------------
    # Prepares the query for insertion of the data of the-
    # region8 in the Database, if it does not exist
    # @Private
    # ---------------------------------------------------------------
    def _region8PrepareMaybeInsert(self,value):
        self._prepareInsertValueInTable('Region8',
                                        None,
                                        'region8Name',
                                        None,
                                        value,
                                        True)

    # ---------------------------------------------------------------
    # Prepares the query for insertion of the data of the-
    # farmer market in the Database, if it does not exist
    # @Private
    # ---------------------------------------------------------------
    def _farmerMarketPrepareMaybeInsert(self,id,longitude,latitude,setCens,
                                        areaP,name,register,publicPlace,
                                        number,reference,districtID,
                                        subPrefectureID,region5Name,
                                        region8Name,neighborhoodName):
     
        # I get the IDs to build the relationships
        rowRegion5 = self._valueExistsInTable('Region5','region5Name',region5Name)
        if(not (rowRegion5 is None)):
            region5ID = rowRegion5['region5ID']

        rowRegion8 = self._valueExistsInTable('Region8','region8Name',region8Name) 
        if(not (rowRegion8 is None)):
            region8ID = rowRegion8['region8ID']

        rowNeighborhood = self._valueExistsInTable('Neighborhood','neighborhoodName',neighborhoodName)
        if(not (rowNeighborhood is None)):
            neighborhoodID = rowNeighborhood['neighborhoodID']

        # I only enter the farmer market, if it does not exist in database
        if(self._validatesInsertionFarmerMarket(rowRegion5,rowRegion8,rowNeighborhood,id,
                                                longitude,latitude,setCens,areaP,name,
                                                register,publicPlace)):

            values = [id,longitude,latitude,setCens,
                      areaP,name,register,
                      publicPlace,str(number),
                      str(reference),districtID,
                      subPrefectureID,region5ID,
                      region8ID,neighborhoodID]

            newValues = []

            for value in values:
                if type(value) == str:
                    value = '"' + value + '"'
                newValues.append(value)

            return self._prepareInsertValueInTable('FarmerMarket',
                                                   None,
                                                   'farmerMarketName',
                                                   None,
                                                   newValues)

    # ---------------------------------------------------------------
    # Prepares the insert query
    # @Private
    # ---------------------------------------------------------------
    def _prepareInsertValueInTable(self,tbl,fieldID,fieldName,id,value,insertNow=False):
        if(isinstance(value, list) is True):
            valueName = value[5]
        else:
            valueName = value

        # Variable used to receive the query already constructed
        query = ''

        row = self._valueExistsInTable(tbl,fieldName,valueName)

        # If does not exist in the database, then I insert
        if(row is None and valueName != " "):
            if(not (fieldID is None) and not (id is None)):
                query = 'INSERT INTO %s (%s,%s) VALUES(%s,"%s")' % (tbl,
                                                                    fieldID,
                                                                    fieldName,
                                                                    int(id),
                                                                    valueName)
            elif(isinstance(value, list) is True):
                query = 'INSERT INTO ' + tbl + ' VALUES(%s)' % "," . join(map(str,value))

            else:
                query = 'INSERT INTO %s (%s) VALUES("%s")' % (tbl,
                                                              fieldName,
                                                              valueName)

            # If the variable insertNow is True, then I execute the query,
            # otherwise I return the query to method that made the call
            if(insertNow is True and query != ''):
                try:
                    self._db.execute(query)
                except Exception as ex:
                    print(ex)
                    raise
            else:
                return query

    # ---------------------------------------------------------------
    # Checks whether a particular data already exists in the database
    # @Private
    # ---------------------------------------------------------------
    def _valueExistsInTable(self,tbl,fieldName,value):

        if(not (value is None) and value != ''):
            if(not re.search('"',value)):
                value = '"' + value + '"'

            # TODO: Implement variable to check
            #check = self._db.execute('SELECT COUNT(*) AS ifExists FROM %s WHERE %s = %s' % (tbl,
            #                                                                                fieldName,
            #                                                                                value))

            row = self._db.execute('SELECT * FROM %s WHERE %s = %s' % (tbl,
                                                                       fieldName,
                                                                       value))

            if (self._db.rowcount == 1 and not (row is None)):
                return row
            else:
                return None

    # ---------------------------------------------------------------
    # Validates the insertion of farmer market
    # @Private
    # ---------------------------------------------------------------
    def _validatesInsertionFarmerMarket(self,rowRegion5,rowRegion8,
                                        rowNeighborhood,id,longitude,latitude,
                                        setCens,areaP,name,register,publicPlace):

        if(not (rowRegion5 is None) and not (rowRegion8 is None) and
           not (rowNeighborhood is None) and id != "" and longitude != "" and
           latitude != "" and setCens != "" and areaP != "" and name != "" and
           register != "" and publicPlace != ""):
            return True
        else:
            return False
