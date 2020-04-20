import configparser

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

class Config():
    SQLALCHEMY_DATABASE_URI = '%s+%s://%s:%s@%s:%s/%s' % (
        cfg['database']['default_connection'],
        cfg['mysql']['driver'],
        cfg['mysql']['user'],
        cfg['mysql']['password'],
        cfg['mysql']['host'],
        cfg['mysql']['port'],
        cfg['mysql']['db']
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = cfg['jwt']['secret_key']

class DevelopmentConfig(Config):
    APP_DEBUG = True
    DEBUG = True
    MAX_BYTES = 10000
    APP_PORT = 9090

class ProductionConfig(Config):
    APP_DEBUG = False
    DEBUG = False
    MAX_BYTES = 100000
    APP_PORT = 5050

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = '%s+%s://%s:%s@%s:%s/%s_testing' % (
        cfg['database']['default_connection'],
        cfg['mysql']['driver'],
        cfg['mysql']['user'],
        cfg['mysql']['password'],
        cfg['mysql']['host'],
        cfg['mysql']['port'],
        cfg['mysql']['db']
    )
    APP_DEBUG = True
    DEBUG = True
    MAX_BYTES = 10000
    APP_PORT = 9090

