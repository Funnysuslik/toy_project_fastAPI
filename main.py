import uvicorn
from fastapi import FastAPI

from db.base import database
from endpionts import users, auth

app = FastAPI(title='Cash App')
app.include_router(users.router, prefix='/users', tags=['users'])
app.include_router(auth.router, prefix='/auth', tags=['auth'])


@app.get('/')
async def root():
    return {'message': 'Hello world!'}


@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)