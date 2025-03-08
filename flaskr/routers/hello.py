from flask_restx import Resource, Namespace

hello_ns = Namespace("")  # Usa "hello" como nombre

@hello_ns.route("/")  # Ruta raíz dentro del namespace
class Hello(Resource):
    def get(self):
        return {"status": True, "message": "Conectado..."}, 200