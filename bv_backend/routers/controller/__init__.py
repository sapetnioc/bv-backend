import os

from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from soma.controller import field_type_str, parse_type_str
from soma.undefined import undefined

router = APIRouter()

base_dir = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(base_dir, 'templates'))

published_controllers = {}

class JinjaController:
    template_per_type = {
        'str': 'str_field.jinja',
        'list': 'list_field.jinja',
    }

    def __init__(self, id, controller):
        self.id = id
        self.controller = controller

    def field_jinja(self, field):
        base_type = parse_type_str(field_type_str(field))[0]
        return self.template_per_type.get(base_type, 'default_field.jinja')

    def value(self, field, default=undefined):
        return getattr(self.controller, field.name, default)

@router.get('/{id}', response_class=HTMLResponse)
async def home(request: Request, id: str):
    controller = published_controllers.get(id)
    if controller is None:
        raise HTTPException(status_code=404, detail=f"Controller not found: {','.join(published_controllers)}")
    else:
        return templates.TemplateResponse("index.html", {'request': request, 
                                                          'cjinja': JinjaController(id, controller)})


@router.websocket("/{id}/ws")
async def websocket(websocket: WebSocket, id: str):
    import bv_backend.main

    controller = published_controllers.get(id)
    if controller is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    else:
        await websocket.accept()
        print('!websocket connected!', id)
        while True:
            async def send_update(name, value):
                await websocket.send_json({
                    'command': 'update',
                    'attribute': name,
                    'value': str(value),
                })

            def value_changed(new_value, old_value, name, controller, index):
                bv_backend.main.the_event_loop.create_task(send_update(name, new_value))
            
            controller.on_attribute_change.add(value_changed)
            try:
                data = await websocket.receive_json()
                print('!websocket!', data, flush=True)
            except WebSocketDisconnect:
                controller.on_attribute_change.remove(value_changed)
