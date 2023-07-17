from datetime import datetime

from fastapi import HTTPException
from starlette import status

from routers.cargo.service import service_get_cargo_types, service_calculate, service_post_cargo_rate
from routers.user.sevice import service_admin_check
from schemas.scemas import User_Pydantic, InputRate_Pydantic


async def controller_post_cargo_rate(data: InputRate_Pydantic, user: User_Pydantic):
    is_admin = await service_admin_check(user)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    await service_post_cargo_rate(data)


async def controller_get_cargo_types(limit: int, page: int):
    offset = limit * page
    return await service_get_cargo_types(limit, offset)


async def controller_calculate(price: int, cargo_type_id: int, date: datetime.date):
    response = await service_calculate(price, cargo_type_id, date)
    if not response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect input")
    return response
