import os

from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), 'templates'))

@router.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "value": "a simple value"})


@router.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_json()
            print('!websocket!', data, flush=True)
        except WebSocketDisconnect:
            break
