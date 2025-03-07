from flaskr.database import db 
from flaskr.enums import TiposDeDocumento

class Usuario(db.Model):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombres = db.Column(db.String(40))
    apellidos = db.Column(db.String(40))
    tipo_de_documento = db.Column(db.Enum(TiposDeDocumento), nullable=True) 
    numero_documento = db.Column(db.String(11), nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=True)
    email = db.Column(db.String(150), nullable=True)
    direccion = db.Column(db.String(150), nullable=True)
    telefono = db.Column(db.String(10), nullable=True)
    empresa = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.Boolean(), default=True)
    fecha_ingreso = db.Column(db.DateTime, nullable=True)
    citas = db.relationship("Cita", back_populates="usuario")




