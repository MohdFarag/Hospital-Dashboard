# Packages
import os

from flask import Flask

from . import database
from . import auth
from . import dashboard

from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.exceptions import HTTPException

from flaskr.log import almaza_logger

#--------------------------------------------------------------------------#

"""Our app"""
# __ init __
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    
    # configuration
    app.config.from_object('flaskr.config.Config')

    if test_config is None:
        # using a development configuration
        app.config.from_object('flaskr.config.DevConfig')
        
        ## using a production configuration
        # app.config.from_object('config.ProdConfig')
        # app.wsgi_app = ProxyFix(app.wsgi_app)
    else:
        # load the test config if passed in
        app.config.from_object('flaskr.config.Test')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    almaza_logger.info('Settings are setted successfully.')
  
    # Initialize the Database File
    database.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')

    return app



