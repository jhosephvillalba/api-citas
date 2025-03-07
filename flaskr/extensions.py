from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
# from flask_restx import Api
from flask_restx import Api
from flask_cors import CORS
from flask_marshmallow import Marshmallow

migration = Migrate()
jwt = JWTManager()
mail = Mail()
api = Api(doc="/swagger-ui/", version="0.1", title="Api Cites")
cors = CORS()
ma = Marshmallow() 
