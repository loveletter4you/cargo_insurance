import datetime
from typing import List, Dict

from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from model.models import CargoType, Rate, User
from pydantic import BaseModel

Tortoise.init_models(["model.models"], "models")

CargoType_Pydantic_List = pydantic_queryset_creator(CargoType)
User_Pydantic = pydantic_model_creator(User, name="User")


class CargoTypes_Pydantic(BaseModel):
    cargo_types: CargoType_Pydantic_List
    count: int


class CalculateResponse_Pydantic(BaseModel):
    insurance: float


class CargoRateInput_Pydantic(BaseModel):
    cargo_type: str
    rate: float


class InputRate_Pydantic(BaseModel):
    __root__: Dict[datetime.date, List[CargoRateInput_Pydantic]]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]
