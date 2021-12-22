import asyncio
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import computing, controller

the_event_loop = None

tags_metadata = [
    {
        "name": "computing",
        "title": "Computing",
        "description": "Operation regarding computing resources.",
    },
]


app = FastAPI(
    title='BrainVISA Backend',
    description='Services for remote parallel neuroimaging processing',
    version='0.0.0')


app.include_router(
    computing.router,
    prefix="/computing",
    tags=["computing"])


app.include_router(
    controller.router,
    prefix="/controller",
    tags=["html"])
# The following code should be done in routers.controller module
# but due to a FastAPI bug it must be done using FastAPI instance:
# https://github.com/tiangolo/fastapi/issues/1469
base_dir = os.path.dirname(__file__)
app.mount("/static/controller", StaticFiles(directory=os.path.join(base_dir, 'routers', 'controller', 'static')), name='controller_static')


@app.on_event("startup")
async def startup_event():
    global the_event_loop

    the_event_loop = asyncio.get_running_loop()
