import json
from . import client, create_token, reset_db

class TestPersonCrud():

    idPerson = 0
    reset_db()

    def test_person_insert(self, client):
        token = create_token()

        data = {
            "name":"rachmankamil",
            "age":25,
            "sex":"male"
        }

        res = client.post('/person',
                         json=data,
                         headers={'Authorization': 'Bearer ' + token}
                         )
        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id'] > 0
        
        self.idPerson = res_json['id']

    def test_person_list(self, client):
        token = create_token()
        res = client.get('/person',
                        headers={'Authorization': 'Bearer ' + token}
        )
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_person_invalid_token(self, client):
        res=client.get('/person',
                    headers={'Authorization': 'Bearer abc'}
        )
        # res_json=json.loads(res.data)
        assert res.status_code == 401

    def test_person_invalid_input_name(self, client):
        token = create_token()
        data = {
            'age' : 60,
            'sex' : 'Male'
        }
        res=client.post('/person',
                        data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json'
        )

        res_json=json.loads(res.data)
        assert res.status_code == 400

class TestMockWeatherBit():
	def mocked_requests_get(*args, **kwargs):
		class MockResponse:
			def __init__(self, json_data, status_code):
				self.json_data = json_data
				self.status_code = status_code

			def json(self):
				return self.json_data

		if len(args) > 0:
			if args[0] == "api.weatherbit.io/ip/":
				return MockResponse({
							"len": "-12123.123124",
							"long": "123123.123123"
						}, 200)
			elif args[0] == "api.weatherbit.io/weather/":
				return MockResponse({
                    "city":"malang",
                    "weather":23.5
                }, 200)
		else:
			return MockResponse(None, 404)

	@mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
	def test_weather(self, test_reqpost_mock, test_reqget_mock):
        #bla bla bla
		assert ret.status_code == 200
		assert ret.json_data["data"]["weather"] == 23.5