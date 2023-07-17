import jwt
from fastapi import security
from passlib.hash import bcrypt
from model.models import Role, User
from schemas.scemas import User_Pydantic
from settings_env import ADMIN_LOGIN, ADMIN_PASSWORD


async def service_create_admin():
    role = await Role.get_or_none(name="Admin")
    if not role:
        role = await Role.create(name="Admin")
    admin = await User.get_or_none(login=ADMIN_LOGIN, role=role).prefetch_related('role')
    if not admin:
        await User.create(login=ADMIN_LOGIN, password_hash=bcrypt.hash(ADMIN_PASSWORD), role=role)


async def service_get_user_by_login(login: str):
    user = await User.get_or_none(login=login).prefetch_related('role')
    return user


async def service_get_user_by_id(id: int):
    user = await User.get_or_none(id=id).prefetch_related('role')
    return user


async def service_admin_check(user: User):
    if user.role.name == "Admin":
        return True
    return False


async def service_create_token(user: User):
    user_object = User_Pydantic.from_orm(user)
    token = jwt.encode(user_object.dict(), "SECRET_KEY")
    return dict(access_token=token, token_type="bearer")


def service_oauth2scheme():
    return security.OAuth2PasswordBearer(tokenUrl="/api/user/token")
