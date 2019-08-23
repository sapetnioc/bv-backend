import os.path as osp

import datetime
import json
from typing import List


def init_api(api):
    @api.schema
    class Subject:
        id: str
        sex: str
        birth_year: str

    @api.schema
    class Center:
        id: str
        name: str

    @api.schema
    class Data:
        id: str
        a_number: int
        another_number: float
        a_string: str
        another_string: str

    @api.schema
    class Visit:
        id: str
        when: datetime.datetime
        center_id: str
        subject_id: str
        data_id: str

    @api.path('/subjects')
    def get() -> List[Subject]:
        '''List all subjects'''
        return json.load(open(osp.join(osp.dirname(__file__), 'subjects.json')))
    
    
    @api.path('/centers')
    def get() -> List[Center]:
        '''List all centers'''
        return json.load(open(osp.join(osp.dirname(__file__), 'centers.json')))


    @api.path('/data')
    def get() -> List[Data]:
        '''List all data'''
        return json.load(open(osp.join(osp.dirname(__file__), 'data.json')))


    @api.path('/visits')
    def get() -> List[Visit]:
        '''List all visits'''
        return json.load(open(osp.join(osp.dirname(__file__), 'visits.json')))
