from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.main import api_router
from tortoise.contrib.fastapi import register_tortoise
from app.db_config import TORTOISE_ORM

api = FastAPI()

api.mount("/static", StaticFiles(directory="../frontend/dist"), name="static")

register_tortoise(api, TORTOISE_ORM)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000", "http://127.0.0.1:8080", "http://localhost:8080",
                   "http://127.0.0.1:8848", "http://localhost:8848"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api.include_router(api_router)


@api.get('/')
async def index():
    return {'say': 'hello'}
