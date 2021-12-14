from fastapi import FastAPI

from .routers import computing, controller

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
