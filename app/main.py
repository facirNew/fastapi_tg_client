from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from routers.api_routes import root_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info('Start application')
    yield
    logger.info('Stop application')


app = FastAPI(lifespan=lifespan)
app.include_router(root_router)
