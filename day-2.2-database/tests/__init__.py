# tests/__init__.py

import pytest, json, logging
from flask import Flask, request

from blueprints import app
from blueprints.person.model import Persons
from app import cache

def call_client(request):
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()
    # return client

@pytest.fixture
def client(request):
    return call_client(request)

@pytest.fixture
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 =  Persons(person_name="Kamil", age=20, sex='Male',salt=salt, pass=hash)
    user2 = User(email='kennedyfamilyrecipes@gmail.com',
                 plaintext_password='PaSsWoRd')
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()

def create_token():
    token = cache.get('test-token')
    if token is None:
        ## prepare request input
        data = {
            'client_key': 'altarest',
            'client_secret': '1OopwAPk3Q2D'
        }

        ## do request
        req = call_client(request)
        res = req.get('/token', 
                        query_string=data
        )
        
        ## store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        ## assert / compare with expected result
        assert res.status_code == 200

        ## save token into cache
        cache.set('test-token', res_json['token'], timeout=60)

        ## return, because it usefull for other test
        return res_json['token']
    else:
        return token
