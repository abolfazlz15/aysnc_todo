from fastapi import FastAPI

from src.routers.auth import router as auth_router
from src.routers.user import router as user_router

app = FastAPI()

app.include_router(auth_router, tags=["auth"])
app.include_router(user_router, tags=["user"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "This is Root"}

