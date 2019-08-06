'''This is the WSGI entry point for bv_auth
'''

from functools import partial
#import logging.config
import os
import os.path as osp

from flask import Flask
#from flask_login import LoginManager

import bv_rest
import bv_rest.database
import bv_auth

def create_app(test_config=None):
    app_name = osp.basename(osp.dirname(__file__))
    
    #logging.config.dictConfig({
        #'version': 1,
        #'formatters': {'default': {
            #'format': '%s: [%%(asctime)s] %%(levelname)s in %%(module)s: %%(message)s' % app_name,
        #}},
        #'handlers': {'wsgi': {
            #'class': 'logging.handlers.WatchedFileHandler',
            #'formatter': 'default',
            #'filename': osp.join(bv_rest.config.services_dir, 'log', 'services.log'),
        #}},
        #'root': {
            #'level': 'INFO',
            #'handlers': ['wsgi']
        #}
    #})
    
    # create and configure the app
    app = Flask(app_name, instance_path=osp.join(bv_rest.config.services_dir, app_name), instance_relative_config=True)
    #secret_key_file = osp.join(bv_rest.config.services_dir, 'secret.key')
    #app.secret_key = open(secret_key_file, 'rb').read()

    #if test_config is None:
        ## load the instance config, if it exists, when not testing
        #app.config.from_json('config.json')
    #else:
        ## load the test config if passed in
        #app.config.from_mapping(test_config)

    #login_manager = LoginManager(app)
    #login_manager.login_view = 'authentication.login'

    #login_manager.user_loader(partial(User.get, bypass_access_rights=True))

    #app.jinja_env.add_extension('jinja2.ext.do')

    bv_rest.database.init_app(app)
    api = bv_rest.RestAPI(app,
        title='brainvisa_auth',
        description='The BrainVISA authentication and authorization service',
        version='0.0.1',
    )

    bv_rest.init_api(api)
    bv_auth.init_api(api)

    return app

application = create_app()


if __name__ == '__main__':
    application.run()
