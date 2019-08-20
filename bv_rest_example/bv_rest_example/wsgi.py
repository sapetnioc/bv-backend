'''This is the WSGI entry point for bv_auth
'''

from functools import partial
import os
import os.path as osp

from flask import Flask

import bv_rest
import bv_rest_example

def create_app(test_config=None):
    app_name = osp.basename(osp.dirname(__file__))
    
    
    # create and configure the app
    app = Flask(app_name, instance_path=osp.join(bv_rest.config.services_dir, app_name), instance_relative_config=True)

    api = bv_rest.RestAPI(app,
        title='bv_rest_exmple',
        description='Example of REST services',
        version='0.0.1',
    )

    bv_rest.init_api(api)
    bv_rest_example.init_api(api)

    return app

application = create_app()


if __name__ == '__main__':
    application.run()
