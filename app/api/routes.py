from fastapi import APIRouter, status

from app.api import controllers, schemas


router = APIRouter()


@router.post("/users", status_code=status.HTTP_204_NO_CONTENT)
async def create_new_user(user: schemas.User):
    await controllers.create_new_user(username=user.username, email=user.email)


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_users() -> list[schemas.User]:
    return await controllers.get_users()
