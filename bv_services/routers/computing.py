from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel, constr

router = APIRouter()

class NewComputingResource(BaseModel):
    name: constr(max_length=40)

class ComputingResource(NewComputingResource):
    id: UUID

@router.get('/', tags=['computing'],
         summary='List computing resources',
         response_model=list[ComputingResource])
async def list_computing():
    '''
    List all computing resources
    '''
    raise HTTPException(status_code=404, detail='Not implemented')


@router.get('/{computing_id}', tags=['computing'],
         summary='Info on computing resource',
         response_model=ComputingResource)
async def computing_resource():
    '''
    Inspect a single computing resource
    '''
    raise HTTPException(status_code=404, detail='Not implemented')


@router.post('/', tags=['computing'],
          summary='Add computing resource',
          response_model=UUID)
async def add_computing(computing_resource: NewComputingResource):
    '''
    Declare a new computing resource
    '''
    raise HTTPException(status_code=404, detail='Not implemented')


@router.delete('/computing/{computing_id}', tags=['computing'],
            summary='Remove a computing resource')
async def remove_computing(computing_id: str):
    raise HTTPException(status_code=404, detail='Not implemented')
