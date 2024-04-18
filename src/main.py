from fastapi import FastAPI, Response
from fastapi_users import FastAPIUsers, fastapi_users
import uvicorn
from auth.auth import auth_backend
from auth.database import User

from auth.shemas import UserRead, UserCreate
from manager.manager import get_user_manager

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app = FastAPI()
if __name__ == "__main__":
    uvicorn.run("main:app")


@app.get("/hello")
def hello():
    return {"message": "Hello World"}

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)