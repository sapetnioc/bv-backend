'''This is the WSGI entry point for bv_admin
'''

from functools import partial
#import logging.config
import os
import os.path as osp

from flask import Flask
#from flask_login import LoginManager

import bv_rest
import bv_rest.database
import bv_admin

def create_app():
    app_name = osp.basename(osp.dirname(__file__))
        
    # create and configure the app
    app = Flask(app_name, instance_path=osp.join(bv_rest.config.services_dir, app_name), instance_relative_config=True)

    bv_rest.database.init_app(app)
    api = bv_rest.RestAPI(app,
        title='bv_admin',
        description='Project and users administration for BrainVISA services',
        version='0.0.1',
    )

    bv_rest.init_api(api)
    bv_admin.init_api(api)

    return app

application = create_app()
