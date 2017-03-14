#
# REST Class
#
# @Author: Erick Rettozi

import sys

sys.path.append("../../class")
from DB import DB
from CFG import CFG
from Log import LOG

class REST():

    # ---------------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------------
    def __init__(self):

        cfg = CFG('../../cfg/farmersmarket.yaml')

        self._db = DB(cfg.data['db']['type'],
                      cfg.data['db']['host'],
                      cfg.data['db']['user'],
                      cfg.data['db']['pass'],
                      cfg.data['db']['dbname'])

        self._db.connect()

        # Set log file
        self._log = LOG('../../log/api.log')

        self._log.logger.info('Opening connection to the database')

    # ---------------------------------------------------------------
    # Destructor
    # ---------------------------------------------------------------
    def destroy(self):
        # Disconnect database
        self._db.disconnect()

        self._log.logger.info('Connection to finished database')

    # ---------------------------------------------------------------
    # Search for a farmer market using one of following parameters
    # -districtID
    # -region5ID
    # -farmerMarketName
    # -neighborhoodID
    #
    # @Public
    # ---------------------------------------------------------------
    def getFarmerMarket(self,paramName,value):

        result = {}
        if( (paramName == 'districtID') or (paramName == 'region5ID') or
            (paramName == 'farmerMarketName') or (paramName == 'neighborhoodID') ):

            query = 'SELECT * FROM FarmerMarket WHERE '

            if(value.isdigit()):
                query += paramName + '=' + value
            else:
                query += paramName + ' = "'+str(value)+'"'

            result = self._db.execute(query,fetchAll=True)
        else:
            result['message'] = 'Invalid search parameter!'

        self._log.logger.info('getFarmerMarket(): Query - ' + str(query))
        self._log.logger.info('getFarmerMarket(): RESTful result - ' + str(result))

        return result
    
    # ---------------------------------------------------------------
    # Inserting farmer market data into the database
    # @Public
    # ---------------------------------------------------------------
    def insertFarmerMarket(self,data):
        
        columns = ('farmerMarketID',
                   'farmerMarketLongitude',
                   'farmerMarketLatitude',
                   'farmerMarketSetCens',
                   'farmerMarketAreaP',
                   'farmerMarketName',
                   'farmerMarketRegister',
                   'farmerMarketPublicPlace',
                   'farmerMarketNumber',
                   'farmerMarketReference',
                   'districtID',
                   'subPrefectureID',
                   'region5ID',
                   'region8ID',
                   'neighborhoodID')

        query = 'INSERT INTO FarmerMarket VALUES('

        count = 1
        for column in columns:
            value = data[column]
            if(type(value) != int):
                value = '"' + value + '"'

            query += str(value)
            if count < len(list(data)):
                query += ','
            count += 1

        query += ') '

        result = {}
        try:
            self._db.execute(query)
            result['message'] = 'Success in inserting data into database'
        except Exception as ex:
            result['message'] = 'Error inserting data into the database'
            result['error'] = ex

        self._log.logger.info('insertFarmerMarket(): Query - ' + str(query))
        self._log.logger.info('insertFarmerMarket(): RESTful result - ' + str(result))

        return result

    # ---------------------------------------------------------------
    # Updating the farmer market data in database
    # @Public
    # ---------------------------------------------------------------
    def updateFarmerMarket(self,data,farmerMarketID):
        
        columns = ('farmerMarketLongitude',
                   'farmerMarketLatitude',
                   'farmerMarketSetCens',
                   'farmerMarketAreaP',
                   'farmerMarketName',
                   'farmerMarketPublicPlace',
                   'farmerMarketNumber',
                   'farmerMarketReference',
                   'districtID',
                   'subPrefectureID',
                   'region5ID',
                   'region8ID',
                   'neighborhoodID')

        query = 'UPDATE FarmerMarket SET '

        count = 1
        for column in columns:
            value = data[column]
            if(type(value) != int):
                value = column + ' = "' + value + '"'
            else:
                value = column + ' = ' + str(value)

            query += str(value)
            if count < len(list(data)):
                query += ','
            count += 1

        query += ' WHERE farmerMarketID = ' + farmerMarketID

        result = {}
        try:
            self._db.execute(query)
            result['message'] = 'Sucesso ao atualizar os dados da feira id: ' + str(farmerMarketID)
        except Exception as ex:
            result['message'] = 'Erro'
            result['error'] = ex

        self._log.logger.info('updateFarmerMarket(): Query - ' + str(query))
        self._log.logger.info('updateFarmerMarket(): RESTful result - ' + str(result))

        return result

    # ---------------------------------------------------------------
    # Deleting the farmer market from the database (by registerID)
    # @Public
    # ---------------------------------------------------------------
    def deleteFarmerMarket(self,registerID):
    
        query = 'DELETE FROM FarmerMarket WHERE farmerMarketRegister=' + str(registerID)
        result = {}
        try:
            self._db.execute(query)
            result['message'] = 'Sucesso ao deletar registro: ' + str(registerID)
        except Exception as ex:
            result['message'] = 'Erro'
            result['error'] = ex

        self._log.logger.info('deleteFarmerMarket(): Query - ' + str(query))
        self._log.logger.info('deleteFarmerMarket(): RESTful result - ' + str(result))

        return result
