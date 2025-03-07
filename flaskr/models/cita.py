from flaskr.database import db

class Cita(db.Model):
    __tablename__ = 'citas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo_cita = db.Column(db.Enum('General', 'Especialista', name='tipo_cita_enum'), nullable=False)
    nombre_medico = db.Column(db.String(100), nullable=False)
    direccion_cita = db.Column(db.String(255), nullable=False)
    fecha_cita = db.Column(db.Date, nullable=False)
    hora_cita = db.Column(db.Time, nullable=False)
    asistencia = db.Column(db.Enum('Si', 'No', name='asistencia_enum'), nullable=False)

    usuario = db.relationship("Usuario", back_populates="citas")  # Relación con el modelo Usuario (opcional)
    
    def __repr__(self):
        return f"<Cita(id={self.id}, tipo_cita={self.tipo_cita}, nombre_medico={self.nombre_medico}, fecha={self.fecha_cita}, hora={self.hora_cita}, asistencia={self.asistencia})>"
