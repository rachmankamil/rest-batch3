# tests/__init__.py

import pytest, json, logging
from flask import Flask, request

from blueprints import app, db
from blueprints.person.model import Persons
from app import cache

def reset_db():
    db.drop_all()
    db.create_all()

    person = Persons("username","password",True)
    db.session.add(person)
    db.session.commit()
    person = Persons("username2","password2",False)
    db.session.commit()

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

def create_token(isinternal=False):
    if isinternal:
        cachename = 'test-internal-token'
        data = {
                'client_key': 'internal',
                'client_secret': 'thisisinternal'
            }
    else:
        cachename = 'test-token'
        data = {
                'client_key': 'altarest',
                'client_secret': '1OopwAPk3Q2D'
            }
    token = cache.get(cachename)
    if token is None:
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
        cache.set(cachename, res_json['token'], timeout=60)

        ## return, because it usefull for other test
        return res_json['token']
    else:
        return token
