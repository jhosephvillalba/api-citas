from flask_restx import Resource, Namespace ,fields 
from flaskr.schemas import CitaSchema
from flaskr.models import Cita, Usuario
from flask import request
from flaskr.database import db
from sqlalchemy.exc import SQLAlchemyError

citas_ns = Namespace("Citas", description="Servicios para crear citas")

cita_model = citas_ns.model('CitaResponse', {
    'id': fields.Integer(readOnly=True, description='ID único de la cita'),
    # 'id_usuario': fields.Integer(required=True, description='ID del usuario asociado a la cita'),
    'tipo_cita': fields.String(required=True, description='Tipo de cita (General o Especialista)'),
    'nombre_medico': fields.String(required=True, description='Nombre del médico'),
    'direccion_cita': fields.String(required=True, description='Dirección de la cita'),
    'fecha_cita': fields.String(required=True, description='Fecha de la cita en formato YYYY-MM-DD'),
    'hora_cita': fields.String(required=True, description='Hora de la cita en formato HH:MM:SS'),
    'asistencia': fields.String(required=True, description='Asistencia a la cita (Si o No)')
})

cita_register_model = citas_ns.model('CitaRegister', {
    # 'id_usuario': fields.Integer(required=True, description='ID del usuario asociado a la cita'),
    'tipo_cita': fields.String(required=True, description='Tipo de cita (General o Especialista)'),
    'nombre_medico': fields.String(required=True, description='Nombre del médico'),
    'direccion_cita': fields.String(required=True, description='Dirección de la cita'),
    'fecha_cita': fields.String(required=True, description='Fecha de la cita en formato YYYY-MM-DD'),
    'hora_cita': fields.String(required=True, description='Hora de la cita en formato HH:MM:SS'),
    'asistencia': fields.String(required=True, description='Asistencia a la cita (Si o No)')
})

model_response = citas_ns.model("CitaResponseWrapperNotData", {
    "status":fields.Boolean(),
    "message":fields.String()
})

model_response_data = citas_ns.model("CitaResponseWrapperSingel", {
     "status":fields.Boolean(),
     "message":fields.String(), 
     "data":fields.Nested(cita_model)
})

model_response_List_data = citas_ns.model("CitaResponseWrapperList", {
     "status":fields.Boolean(),
     "message":fields.String(), 
     "data":fields.List(fields.Nested(cita_model))
})


@citas_ns.route("/add/<int:user_id>")
class RegisterCitas(Resource): 
    @citas_ns.expect(cita_register_model)
    @citas_ns.marshal_with(model_response)
    def post(self, user_id):
        try:

            if not user_id: 
                return {
                "status":False,
                "message":f"debe seleccionar un usuario para asignar una cita",
                "data": {}
                }, 400
            
            usuario = Usuario.query.get(user_id)

            if not usuario:
                 return {
                "status":False,
                "message":f"no se encontro el usuario",
                "data": {}
                }, 404
            
            schema = CitaSchema()
            data = schema.load(request.json)
            cita = Cita( **data )

            usuario.citas = [ cita, *usuario.citas ]
            db.session.commit()

            return {
                "status":True,
                "message":f"solicitud procesada exitosamente",
                "data": {}
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


@citas_ns.route("/list/<int:user_id>")
class ListCitas(Resource): 
    @citas_ns.marshal_with(model_response_List_data)
    def get(self, user_id):
        try:

            if not user_id: 
                return {
                "status":False,
                "message":f"debe seleccionar un usuario para asignar una cita",
                "data": {}
                }, 400
            
            citas = Cita.query.where(Cita.id_usuario == user_id).all()

            if citas.__len__() == 0:
                return {
                "status":True,
                "message":f"solicitud procesada exitosamente",
                "data": []
                }, 200
            
            schema = CitaSchema()

            return {
                "status":True,
                "message":f"solicitud procesada exitosamente",
                "data": schema.dump(citas, many=True)
            }, 200

        except SQLAlchemyError as e:
            
            return {
                "status":False,
                "message":f"algo salio mal: {e}",
                "data": {}
            }, 500
        
        finally:
            db.session.close()


@citas_ns.route("/cita-update/<int:cita_id>")
class UpdateCitas(Resource): 
    @citas_ns.expect(cita_model)
    @citas_ns.marshal_with(model_response)
    def put(self, cita_id):
        """Actualizar una cita"""
        try:
            if not cita_id: 
                return {
                "status":False,
                "message":f"no se ha selecionado una cita",
                "data": {}
                }, 400
            
            cita = Cita.query.get(cita_id)

            if not cita:
                return {
                "status":False,
                "message":f"no se encontro la cita.",
                "data": {}
                }, 404
            
            schema = CitaSchema()
            data = schema.load(request.json)

            for key, value in data.items():
                setattr(cita, key, value)

            db.session.commit()

            return {
                "status":True,
                "message":f"solicitud procesada exitosamente",
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


@citas_ns.route("/cita-delete/<int:cita_id>")
class DeleteCitas(Resource): 
    @citas_ns.marshal_with(model_response)
    def delete(self, cita_id):
        """cancelar una cita"""
        try:
            if not cita_id: 
                return {
                "status":False,
                "message":f"no se ha selecionado una cita",
                "data": {}
                }, 400
            
            cita = Cita.query.get(cita_id)

            if not cita:
                return {
                "status":False,
                "message":f"no se encontro la cita.",
                "data": {}
                }, 404
            
            db.session.delete(cita)
            db.session.commit()

            return {
                "status":True,
                "message":f"solicitud procesada exitosamente",
                "data": {}
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



@citas_ns.route("/cita-details/<int:cita_id>")
class DetalleCitas(Resource): 
    @citas_ns.marshal_with(model_response_data)
    def get(self, cita_id):
        """Detalle una cita"""
        try:
            if not cita_id: 
                return {
                "status":False,
                "message":f"no se ha selecionado una cita",
                "data": {}
                }, 400
            
            cita = Cita.query.get(cita_id)

            if not cita:
                return {
                "status":False,
                "message":f"no se encontro la cita.",
                "data": {}
                }, 404
            
            schema = CitaSchema()
            
            return {
                "status":True,
                "message":f"solicitud procesada exitosamente",
                "data": schema.dump(cita)
            }, 200

        except SQLAlchemyError as e:
            
            return {
                "status":False,
                "message":f"algo salio mal: {e}",
                "data": {}
            }, 500
        
        finally:
            db.session.close()





