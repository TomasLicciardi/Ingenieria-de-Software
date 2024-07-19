from flask_restful import Resource
from main.models import MensajeModel, TablonModel
from .. import db
from flask import request, jsonify


class Mensaje(Resource):
    def get(self, id):
        mensaje = db.session.query(MensajeModel).get_or_404(id)
        return mensaje.to_json()
    
    def put(self, id):
        mensaje = db.session.query(MensajeModel).get_or_404(id)
        data = request.get_json().items()
        print(data)
        for key, value in data:
            setattr(mensaje, key, value)
                
        db.session.add(mensaje)
        db.session.commit()
        return mensaje.to_json(), 201
    
    def delete(self, id):
        mensaje = db.session.query(MensajeModel).get_or_404(id)
        db.session.delete(mensaje)
        db.session.commit()
        return '', 204

class Mensajes(Resource):
    def get(self):
        mensajes = db.session.query(MensajeModel)
        return jsonify({'mensaje': [mensaje.to_json() for mensaje in mensajes] })

    def post(self):
        mensaje = MensajeModel.from_json(request.get_json())
        try:
            db.session.add(mensaje)
            db.session.commit()
        except:
            return "Formato no correcto", 400
        return mensaje.to_json(), 201
    