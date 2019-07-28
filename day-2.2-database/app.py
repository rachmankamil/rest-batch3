# app.py
from flask import request
from flask_restful import Api
import logging
from blueprints import app
from logging.handlers import RotatingFileHandler

####################################
# Flask-RESTFul define custom error
####################################

api = Api(app, catch_all_404s=True)

if __name__ == '__main__':

    ## define log format and create a rotating log with max size of 10MB and max backup up to 10 files
    formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    log_handler = RotatingFileHandler("%s/%s" % (app.root_path, '../storage/log/app.log'), maxBytes=10000, backupCount=10)
    log_handler.setLevel(logging.INFO)
    log_handler.setFormatter(formatter)
    app.logger.addHandler(log_handler)

    ## if you want to jsonify 500 error, you cannot. But you can set debug=False
    app.run(debug=False, host='0.0.0.0', port=5000)
