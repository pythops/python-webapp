from app.models import User


async def create_new_user(username: str, email: str):
    await User.create(username=username, email=email)


async def get_users() -> list:
    users = await User.get_all()
    return [await user.to_dict() for user in users]
