from starlette.config import Config

config = Config('.env')

DATABASE_URL = config('APP_DATABASE_URL', cast=str, default='')
ACCESS_TOKEN_EXP_MIN = 6000
ALGORITH = 'HS256'
SECRET_KEY = config('APP_SECRET_KEY', cast=str, default='8eaa96ff1ea1b6f4fb0e92985d4d04790f6fc6c6ba02bb520b42afaa7b9c65c0')