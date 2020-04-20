import requests
from flask import Blueprint
from flask_restful import Api, reqparse, Resource
from flask_jwt_extended import jwt_required

bp_weather = Blueprint('weather', __name__)
api = Api(bp_weather)

class PublicGetCurrentWeather(Resource):
    wio_host = 'https://api.weatherbit.io/v2.0'
    wio_apikey = '001de4440e814c16bc45197fd601ef9d'

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip', location='args', default=None)
        args = parser.parse_args()

        rq_post = requests.post('endpoint', json={'ip':'192.168.0.1'})

        ## step - 1 - check lon lat from ip
        rq = requests.get(self.wio_host + '/ip', params={'ip': args['ip'], 'key': self.wio_apikey})
        geo = rq.json()
        lat = geo['latitude']
        lon = geo['longitude']

        ## step - 2 - get current weather from lat lon
        rq = requests.get(self.wio_host + '/current', params={'lat': lat, 'lon': lon, 'key': self.wio_apikey})
        current = rq.json()

        return {
            'city': geo['city'],
            'organization': geo['organization'],
            'timezone': geo['timezone'],
            'current_weather': {
                'date': current['data'][0]['datetime'],
                'temp': current['data'][0]['temp']
            }
        }

api.add_resource(PublicGetCurrentWeather, '/ip')
