import datetime

from model.models import CargoType, Rate
from schemas.scemas import CargoType_Pydantic_List, InputRate_Pydantic


async def service_post_cargo_rate(data: InputRate_Pydantic):
    for date in data:
        for cargo_rate in data[date]:
            cargo_type = await CargoType.get_or_none(name=cargo_rate.cargo_type)
            if not cargo_type:
                cargo_type = await CargoType.create(name=cargo_rate.cargo_type)
            rate = await Rate.get_or_none(date=date, cargo_type=cargo_type)
            if not rate:
                await Rate.create(date=date, rate=cargo_rate.rate, cargo_type=cargo_type)
            else:
                rate.rate = cargo_rate.rate
                await rate.save()


async def service_get_cargo_types(limit: int, offset: int):
    cargo_types = await CargoType_Pydantic_List.from_queryset(CargoType.all().offset(offset).limit(limit))
    return dict(cargo_types=cargo_types, count=await CargoType.all().count())


async def service_calculate(price: int, cargo_type_id: int, date: datetime.date):
    # date more than Rate.date and ordering by desc for getting max value
    rate = await Rate.filter(cargo_type_id=cargo_type_id).filter(date__lte=date).order_by("-date").first()
    if not rate:
        return None
    return dict(insurance=round(rate.rate * price, 2))
