import jwt
from fastapi import security, HTTPException, Depends
from starlette import status

from routers.user.sevice import service_get_user_by_login, service_create_token, service_oauth2scheme, \
    service_get_user_by_id
from schemas.scemas import User_Pydantic


async def controller_generate_token(form_data: security.OAuth2PasswordRequestForm):
    user = await controller_auth_user(form_data.username, form_data.password)
    return await service_create_token(user)


async def controller_auth_user(login: str, password: str):
    user = await service_get_user_by_login(login)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not founded")
    if not user.verify_password(password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect login or password")
    return user


async def controller_get_current_user(token: str = Depends(service_oauth2scheme())):
    try:
        payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
        user = await service_get_user_by_id(payload["id"])
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect user")
    return User_Pydantic.from_orm(user)
