import datetime
from fastapi import Request, HTTPException, status
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import HTTPBearer
from passlib.context import CryptContext

from .config import ACCESS_TOKEN_EXP_MIN, SECRET_KEY, ALGORITH

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXP_MIN)})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITH)

def decode_access_token(token: str):
    try:
        encoded_jwt = jwt.encode(token, SECRET_KEY, algorithm=ALGORITH)
    except jwt.JWTError:

        return None

    return encoded_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credantials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        exp = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid auth token')
        if credantials:
            token = decode_access_token(credantials.credentials)
            if token is None:
                raise exp
            return credantials.credentials
        else:
            return exp
