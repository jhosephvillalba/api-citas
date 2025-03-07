from flaskr.models import Usuario
from flaskr.extensions import ma
from marshmallow_enum import EnumField
from flaskr.enums import TiposDeDocumento

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_fk=True

    tipo_de_documento = EnumField(TiposDeDocumento, required=True)
    
