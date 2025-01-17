from fastapi import FastAPI

from src.routers.auth import router

app = FastAPI()

app.include_router(router, tags=['auth'])

@app.get('/', tags=['Root'])
def read_root():
    return {'message': 'This is Root'}

