from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str 
    email: str
    disabled: bool 

class UserDB(User):
    password: str

users_db = {
    "vsociety": {
        "username": "vsociety",
        "full_name": "Pablo Martin Moreno",
        "email": "pablou@gmail.com",
        "disabled": False,
        "password": "123456"
    },
    "vsociety2": {
        "username": "vsociety2",
        "full_name": "Pablo Martin Moreno2",
        "email": "pablou2@gmail.com",
        "disabled": False,
        "password": "123456"
    },
    "vsociety3": {
        "username": "vsociety3",
        "full_name": "Pablo Martin Moreno3",
        "email": "pablou3@gmail.com",
        "disabled": True,
        "password": "123456"
    }
}

def search_user(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autentificación invalidas",
            headers={"WWW-Authenticate": "bearer"})

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")
            
    return user 
    
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400, detail="El usuario no es correcto")

    user = search_user(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=400, detail="La contraseña no es correcta")

    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user 