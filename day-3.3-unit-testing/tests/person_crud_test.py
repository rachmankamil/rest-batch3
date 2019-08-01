import json
from . import app, client, cache, create_token

class TestPersonCrud():

    idPerson = 0

    def test_person_insert(self, client):
        token = create_token()

        data = {

        }

        res = client.post('/person',
                         data=json.dumps(data),
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
        res_json=json.loads(res.data)
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
