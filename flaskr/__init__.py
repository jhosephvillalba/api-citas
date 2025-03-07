import os
from flask import Flask
from flaskr.database import db
from flaskr.extensions import migration, jwt, mail, api, cors, ma

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_object(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #configuration flask restful 
    import flaskr.models

    db.init_app(app)
    migration.init_app(app, db)

    cors.init_app(app, resources={
        r"/*": {
            "origins": "*", 
            "methods": ["GET", "POST", "PUT", "DELETE"], 
            "allow_headers": "*"
            }})
    
    from flaskr.routers import namespaces

    ma.init_app(app)
    mail.init_app(app)
    
    for ns in namespaces:
         api.add_namespace(ns, path=f"/{ns.name}")

    jwt.init_app(app)
    api.init_app(app)
    
    return app
