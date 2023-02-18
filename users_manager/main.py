from fastapi import FastAPI
from routers import users, jwt_auth_users
# from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(users.router)
app.include_router(jwt_auth_users.router)
# app.include_router(basic_auth_users.router)
# app.mount("/static", StaticFiles(directory="static"), name="static")