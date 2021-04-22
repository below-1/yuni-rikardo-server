import os

from flask import Flask
from webapp import db
from pony.flask import Pony
from flask_cors import CORS
from multiprocessing import Process

def create_app(test_config=None):
    # create and configure the app
    app = Flask(
        __name__, 
        static_url_path='', 
        static_folder='static',
        instance_relative_config=True
    )
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_database()
    print('after init database')
    Pony(app)

    if app.config['ENV'] == 'development':
        from pony.orm import set_sql_debug

        def activate_sql_logging():
            set_sql_debug(True)

        app.before_request(activate_sql_logging)

    from webapp.api import api
    app.register_blueprint(api)

    @app.route('/')
    def home():
        return app.send_static_file('index.html')
    # app.cli.add_command(db.init_database)
    # app.teardown_appcontext(queue.remove_queue)

    return app