import json
from flask import Blueprint
from flask_restful import Api, reqparse, Resource

from . import *

bp_client = Blueprint('client', __name__)
api = Api(bp_client)

# FLASK RESTFUL


class ClientResource(Resource):

    clients = Clients()

    def __init__(self):
        pass

    def get(self, client_id=None):
        if client_id is None:
            return self.clients.get_clients(), 200, {"Content-Type": "application/json"}

        else:
            result = self.clients.get_one(client_id)
            if result is not None:
                return result, 200, {"Content-Type": "application/json"}
            else:
                return {"status": "NOT_FOUND", "message": "Clinbt not found"}, 404, {"Content-Type": "application/json"}

    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('client_id', location='json',
                            type=int, required=True)
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json', required=True)
        parser.add_argument('status', location='json',
                            type='boolean', required=True)
        args = parser.parse_args()

        client = Client()

        client.client_id = self.clients.clients[-1]["client_id"] + 1
        client.client_key = args["client_key"]
        client.client_secret = args["client_secret"]
        client.status = args["status"]

        self.clients.add(client.serialize())

        return client.__dict__, 200, {"Content-Type": "application/json"}

    def put(self, client_id):
        parser = reqparse.RequestParser()
        parser.add_argument('client_id', location='json',
                            type=int, required=True)
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json', required=True)
        parser.add_argument('status', location='json',
                            type='boolean', required=True)
        args = parser.parse_args()

        result = self.clients.edit_one(
            args["client_id"], args["client_key"], args["client_secret"], args["status"])
        if result is None:
            return result.__dict__, 200, {"Content-Type": "application/json"}
        else:
            return {"status": "NOT_FOUND", "message": "Client not found"}, 404, {"Content-Type": "application/json"}

    def delete(self, client_id):
        result = self.clients.delete_one(client_id)
        if result is None:
            return "Deleted", 200, {"Content-Type": "application/json"}
        else:
            return {"status": "NOT_FOUND", "message": "Client not found"}, 404, {"Content-Type": "application/json"}

    def patch(self, client_id):
        return "Not yet implemented", 501


api.add_resource(ClientResource, '', '/<id>')
