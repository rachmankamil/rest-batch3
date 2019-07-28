import json
from . import app, client, cache, create_token

class TestClientCrud():
    def test_client_list(self, client):
        token = create_token()
        res = client.get('/person',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200
