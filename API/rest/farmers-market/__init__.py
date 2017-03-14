#
# WebService
#
# @Author: Erick Rettozi

from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
from flask_httpauth import HTTPBasicAuth
import sys
sys.path.append('class')
from REST import REST

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

#Authorized Users
users = {
    'fmmkt': 'hfkYgdtfsli8453hg'
}

# -----------------------------------------------------
# Will allow access only if user is authorized
# -----------------------------------------------------
@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

# -----------------------------------------------------
# Class for methods GET, DELETE AND PUT
# -----------------------------------------------------
class FMRestfulMethods_1(Resource):

    def __init__(self):
        self._rest = REST()

    @auth.login_required
    def get(self, paramName, value):
        if not get_pw(auth.username()):
            abort(404, message='Unauthorized User')

        result = self._rest.getFarmerMarket(paramName,value)
        self._rest.destroy()
        return result

    @auth.login_required
    def delete(self, paramName, value):
        if not get_pw(auth.username()):
            abort(404, message='Unauthorized User')

        result = {}
        if paramName == 'registerID':
            result = self._rest.deleteFarmerMarket(value)
            self._rest.destroy()
        else:
            result['message'] = 'Invalid parameter!'

        return jsonify(result)

    @auth.login_required
    def put(self, paramName, value):
        if not get_pw(auth.username()):
            abort(404, message='Unauthorized User')

        result = {}
        if paramName == 'update':
            data = request.get_json(force=True)
            result = self._rest.updateFarmerMarket(data,value)
            self._rest.destroy()
        else:
            result['message'] = 'Invalid parameter!'

        return jsonify(result)

# -----------------------------------------------------
# Class for method POST
# -----------------------------------------------------
class FMRestfulMethods_2(Resource):
    def __init__(self):
        self._rest = REST()

    @auth.login_required
    def post(self):
        if not get_pw(auth.username()):
            abort(404, message='Unauthorized User')

        data = request.get_json(force=True)
        result = self._rest.insertFarmerMarket(data)
        self._rest.destroy()
        return jsonify(result)

#
# Routes
api.add_resource(FMRestfulMethods_1, '/<paramName>/<value>')
api.add_resource(FMRestfulMethods_2, '/')

#
# @Main
if __name__ == '__main__':
    app.run(debug=True)
