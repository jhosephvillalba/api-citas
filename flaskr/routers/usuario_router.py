from flask_restx import Resource, Namespace ,fields 
from flaskr.schemas import UsuarioSchema
from flaskr.models import Usuario
from flask import request
from flaskr.enums import TiposDeDocumento 
from flaskr.database import db
from sqlalchemy.exc import SQLAlchemyError

usuario_ns = Namespace("Usuarios", description="Servicios de usuarios")

# Modelo de serialización para Swagger
usuario_model = usuario_ns.model("Usuario", {
    "id": fields.Integer(readonly=True, description="ID único del usuario"),
    "nombres": fields.String(required=True, description="Nombres del usuario"),
    "apellidos": fields.String(required=True, description="Apellidos del usuario"),
    "tipo_de_documento": fields.String(enum=[t.name for t in TiposDeDocumento], description="Tipo de documento"),
    "numero_documento": fields.String(required=True, description="Número de documento"),
    "fecha_nacimiento": fields.DateTime(description="Fecha de nacimiento"),
    "email": fields.String(description="Correo electrónico"),
    "direccion": fields.String(description="Dirección del usuario"),
    "telefono": fields.String(description="Teléfono de contacto"),
    "empresa": fields.String(description="Nombre de la empresa"),
    "estado": fields.Boolean(description="Estado del usuario"),
    "fecha_ingreso": fields.DateTime(description="Fecha de ingreso"),
})

model_response = usuario_ns.model("ModelResponseUsuario", {
    "status":fields.Boolean(),
    "message":fields.String(),
    "data":fields.Nested(usuario_model)
})


@usuario_ns.route("/usuario-add")
class RegisterUsuario(Resource): 
    @usuario_ns.expect(usuario_model)
    @usuario_ns.marshal_with(model_response)
    def post(self):
        try:
            schema = UsuarioSchema()
            data = schema.load(request.json)

            numero_de_documento = request.json.get("numero_documento")

            if not numero_de_documento: 
                return {
                "status":False,
                "message":"debe colocar su numero de documento",
                "data": {}
                }, 400

            documento_registrado = Usuario.query.filter(
                Usuario.numero_documento == numero_de_documento).first()
            
            if documento_registrado:
                return {
                "status":False,
                "message":"numero de documento registrado",
                "data": {}
                }, 409
            
            email = request.json.get("email")

            if not email: 
                return {
                "status":False,
                "message":"debe colocar una cuenta de correo electronico",
                "data": {}
                }, 400
            
            email_registrado = Usuario.query.filter(
                Usuario.email == email
            ).first()
            
            if email_registrado:
                return {
                "status":False,
                "message":"correo electronico registrado",
                "data": {}
                }, 409
            
            usuario = Usuario( **data )
            db.session.add( usuario )

            db.session.commit()

            return {
                "status":True,
                "message":"solicitud procesada exitosamente",
                "data": {}
            }, 204
        
        except SQLAlchemyError as e: 
            db.session.rollback()
            return {
                "status":False,
                "message":f"algo salio mal: {e}",
                "data": {}
            }, 500
        
        finally:
            db.session.close()


@usuario_ns.route("/usuario-search")
@usuario_ns.doc(params={"document":""})
class SearchUsuario(Resource):
    @usuario_ns.marshal_with(model_response)
    def get(self): 
        try:
            numero_documento = request.args.get("document")

            if not numero_documento:
                return {
                "status":False,
                "message":f"debe ingresar su numero de documento",
                "data": {}
            }, 400

            usuario = Usuario.query.filter(
                Usuario.numero_documento == numero_documento
                ).first()
            
            if not usuario: 
                return {
                "status":False,
                "message":f"Usuario no registrado",
                "data": {}
                }, 404
            
            schema = UsuarioSchema()

            return {
                "status":True,
                "message":"solicitud procesada exitosamente",
                "data": schema.dump(usuario)
            }, 200

        except Exception as e:
            return {
                "status":False,
                "message":f"algo salio mal: {e}",
                "data": {}
            }, 500
        
        except SQLAlchemyError as e:
            return {
                "status":False,
                "message":f"algo salio mal: {e}",
                "data": {}
            }, 500
        finally:
            db.session.close()



@usuario_ns.route("/usuario-update/<string:document>")
class SearchUsuario(Resource):
    @usuario_ns.expect(usuario_model)
    @usuario_ns.marshal_with(model_response)
    def put(self, document): 
        try:

            if not document:
                return {
                "status":False,
                "message":f"debe ingresar su numero de documento",
                "data": {}
            }, 400

            usuario = Usuario.query.filter(
                Usuario.numero_documento == document
                ).first()
            
            if not usuario: 
                return {
                "status":False,
                "message":f"Usuario no registrado",
                "data": {}
                }, 404
            
            schema = UsuarioSchema()
            data = schema.load(request.json)
            
            documento_update = request.json.get("numero_documento")

            if documento_update != document: 
                document_is_register = Usuario.query.filter(
                    Usuario.numero_documento == document).first()
                
                if document_is_register:
                    return {
                        "status":False,
                        "message":f"documento registrado",
                        "data": {}
                    }, 409
                

            for key, value in data.items():
                setattr(usuario, key, value)
                
            db.session.commit()

            return {
                "status":True,
                "message":"solicitud procesada exitosamente",
                "data": schema.dump(usuario)
            }, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "status":False,
                "message":f"algo salio mal: {e}",
                "data": {}
            }, 500
        finally:
            db.session.close()




        
