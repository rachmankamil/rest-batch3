# app.py

from flask import Flask, request
from flask_restful import Resource, Api
import json, logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
## initiate flask-restful instance
api = Api(app, catch_all_404s=True)

####################################
# Middlewares
######################################

@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    
    app.logger.warning("REQUEST_LOG\t%s",
        json.dumps({
            'method': request.method,
            'code': response.status,
            'uri': request.full_path,
            'request': requestData,
            'response': json.loads(response.data.decode('utf-8'))
        })
    )
    # try:
    #     if request.method == 'GET':
    #         app.logger.warning("REQUEST_LOG\t%s", 
    #             json.dumps({
    #                 'uri': request.full_path,
    #                 'request': request.args.to_dict(), 
    #                 'response': json.loads(response.data.decode('utf-8'))
    #             })
    #         )
    #     else:
    #     app.logger.warning("REQUEST_LOG\t%s", 
    #         json.dumps({
    #             'uri': request.full_path,
    #             'request': request.get_json(), 
    #             'response': json.loads(response.data.decode('utf-8')),
    #         })
    #     )
    # except Exception as e:
    #     app.logger.warning("REQUEST_LOG\t%s",
    #         json.dumps({
    #             'uri': request.full_path,
    #             'request': {},
    #             'response': json.loads(response.data.decode('utf-8')),
    #         })
    #     )
    return response

####################################
# Import blueprints
####################################

from blueprints.person.resources import bp_person

app.register_blueprint(bp_person, url_prefix='/person')

if __name__ == '__main__':

    ## define log format and create a rotating log with max size of 10MB and max backup up to 10 files
    formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    log_handler = RotatingFileHandler("%s/%s" % (app.root_path, 'storage/log/app.log'), maxBytes=10000, backupCount=10)
    log_handler.setLevel(logging.INFO)
    log_handler.setFormatter(formatter)
    app.logger.addHandler(log_handler)

    ## if you want to jsonify 500 error, you cannot. But you can set debug=False
    app.run(debug=False, host='0.0.0.0', port=5000)
