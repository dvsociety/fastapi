from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={404: {"message": "No Encontrado"}})


class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list = [User(id=1, name="a", surname="aaa", url="www.a.com", age=1),
              User(id=2, name="b", surname="bbb", url="www.b.com", age=2)]

def search_user(id: int):
    users = filter(lambda x: x.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"Error": "No se ha esncontrado el usuario"}

@router.get("/")
async def users():
    return users_list


@router.get("/{id}")
async def user(id: int):
    return search_user(id)


@router.post("/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")

    users_list.append(user)
    return user


@router.delete("/{id}")
async def user(id: int):

    found = False
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True         

    if not found:
        return {"Error": "No se ha eliminado el usuario"}

    return id, "Eliminado"

@router.put("/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"Error": "No se ha actualizado el usuario"}

    return user, "Modificado"
