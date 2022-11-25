import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr


class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    hashed_password: str
    created_at: Optional[datetime.datetime]


class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)
    password2: str

    @validator('password2')
    def password_match(cls, value, values, config, field):
        if 'password' in values and value != values['password']:
            raise ValueError('Passwords dont match')
        return value