import datetime

from fastapi import APIRouter, Depends

from routers.cargo.controller import controller_post_cargo_rate, controller_get_cargo_types, controller_calculate
from routers.user.controller import controller_get_current_user
from schemas.scemas import User_Pydantic, CargoTypes_Pydantic, CalculateResponse_Pydantic, InputRate_Pydantic

router = APIRouter(
    prefix="/api/cargo",
    tags=["cargo"],
    responses={404: {"description": "Not found"}}
)


@router.post("")
async def post_cargo_rate(data: InputRate_Pydantic, user: User_Pydantic = Depends(controller_get_current_user)):
    await controller_post_cargo_rate(data, user)


@router.get("/type", response_model=CargoTypes_Pydantic)
async def get_cargo_types(limit: int = 20, page: int = 0):
    return await controller_get_cargo_types(limit, page)


@router.get("/calculate", response_model=CalculateResponse_Pydantic)
async def calculate(price: int, cargo_type_id: int, date: datetime.date = datetime.date.today()):
    return await controller_calculate(price, cargo_type_id, date)
