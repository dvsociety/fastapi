from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(prefix="/user",
                   tags=["user"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No Encontrado"}})

users_list = []

def search_user(field: str, key):
    try:
        user = db_client.local.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}

@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.local.users.find())


@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.local.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.local.users.find_one({"_id": id}))
    
    return User(**new_user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):

    found = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})     

    if not found:
        return {"Error": "No se ha eliminado el usuario"}

    return id, "Eliminado"

@router.put("/", response_model=User)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.local.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"Error": "No se ha actualizado el usuario"}

    return search_user("_id", ObjectId(user.id))