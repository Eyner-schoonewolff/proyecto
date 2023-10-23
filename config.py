from decouple import config
from datetime import timedelta

class Config():
    SECRET_KEY = config('SECRET_KEY')
    SESSION_TYPE = config('SESSION_TYPE')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days = 1)
    

class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig
}