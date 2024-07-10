from flask_restful import Resource
from main.models import Mensaje_PrivadoModel
from .. import db
from flask import request


class Mensaje_Privado(Resource):
    def get(self, id):
        mensaje_privado = db.session.query(Mensaje_PrivadoModel).get_or_404(id)
        return mensaje_privado.to_json()
    
    def put(self, id):
        mensaje_privado = db.session.query(Mensaje_PrivadoModel).get_or_404(id)
        data = request.get_json().items()
        print(data)
        for key, value in data:
            setattr(mensaje_privado, key, value)
                
        db.session.add(mensaje_privado)
        db.session.commit()
        return mensaje_privado.to_json(), 201
    
    def delete(self, id):
        mensaje_privado = db.session.query(Mensaje_PrivadoModel).get_or_404(id)
        db.session.delete(mensaje_privado)
        db.session.commit()
        return '', 204
    
class Mensajes_Privados(Resource):
    def get(self):
        mensajes_privados = db.session.query(Mensaje_PrivadoModel)
        return mensajes_privados.to_json()

    def post(self):
        mensaje_privado = Mensaje_PrivadoModel.from_json(request.get_json())
        print(mensaje_privado)
        try:
            db.session.add(mensaje_privado)
            db.session.commit()
        except:
            return "Formato no correcto", 400
        return mensaje_privado.to_json(), 201
