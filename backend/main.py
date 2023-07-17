from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from routers import cargo, user
from routers.user.sevice import service_create_admin
from settings_env import DB_ROOT, DB_PASSWORD, DB_HOST, DB_NAME


def app_factory():
    myapp = FastAPI()
    myapp.include_router(cargo.router)
    myapp.include_router(user.router)
    return myapp


async def app_startup():
    await service_create_admin()


app = app_factory()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    db_url=f"asyncpg://{DB_ROOT}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}",
    modules={'models': ['model.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.on_event("startup")
async def startup():
    await app_startup()
