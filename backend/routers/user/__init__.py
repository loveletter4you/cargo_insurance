from fastapi import APIRouter, security, Depends

from routers.user.controller import controller_generate_token

router = APIRouter(
    prefix="/api/user",
    tags=["user"],
    responses={404: {"description": "Not found"}}
)


@router.post("/token")
async def login(form_data: security.OAuth2PasswordRequestForm = Depends()):
    token = await controller_generate_token(form_data)
    return token
