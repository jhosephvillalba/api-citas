from flaskr.extensions import ma
from flaskr.models import Cita

class CitaSchema(ma.SQLAlchemyAutoSchema): 
    class Meta:
        model = Cita

    