class TestWeather():
    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data
        
        if len(args) > 0:
            if args[0] == app.config['WEATHER_URL']+"/ip":
                return MockResponse({
                                        "latitude": 81292980931,
                                        "longitude": 91209381092,
                                        "city":"Malang",
                                        "organization":"Maxindo",
                                        "timezone":"Asia/Jakarta"
                                    }, 200)
            elif args[0] == app.config['WEATHER_URL']+"/current":
                return MockResponse({
                                        "data": [
                                            {
                                                "datetime":"27 Jan 2017",
                                                "temp": 27
                                            }
                                        ]
                                    }, 200)
        else:
            return MockResponse(None, 404)


    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_check_weather(self, client, init_database, mock_get, mock_post):
        ......
        ......
        .....
