from fastapi import FastAPI

from .routers import computing

tags_metadata = [
    {
        "name": "computing",
        "title": "Computing",
        "description": "Operation regarding computing resources.",
    },
]


app = FastAPI(
    title='BrainVISA Services',
    description='Services for remote parallel neuroimaging processing',
    version='0.0.0')

app.include_router(
    computing.router,
    prefix="/computing",
    tags=["computing"])
