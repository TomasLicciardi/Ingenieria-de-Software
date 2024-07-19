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
        print(mensaje)
        try:
            db.session.add(mensaje)
            db.session.commit()
        except:
            return "Formato no correcto", 400
        return mensaje.to_json(), 201
    
class TablonMensaje(Resource):
    def get(self, id):
        mensaje = db.session.query(MensajeModel).get_or_404(id)
        tablon = mensaje.tablones
        tablon_json = [tablon.to_json() for tablon in tablon]
        return tablon_json
    
class TablonMensajes(Resource):
    def get(self):
        data = request.get_json()
        id_tablon = data.get('id_tablon')
        tablon = db.session.query(TablonModel).get_or_404(id_tablon)
        mensajes = tablon.mensajes
        mensajes_json = [mensaje.to_json() for mensaje in mensajes]
        return mensajes_json
         
    def post(self):
        data = request.get_json()
        id_mensaje = data.get('id_mensaje')
        id_tablon = data.get('id_tablon')
        mensaje = db.session.query(MensajeModel).get_or_404(id_mensaje)
        tablon = db.session.query(TablonModel).get_or_404(id_tablon)
        if mensaje and tablon:
            tablon.mensajes.append(mensaje)
            db.session.commit()
            return {'message': 'Mensaje agregado al tablon exitosamente'}, 201
        else:
            return {'message': 'El mensaje o el tablon no existen.'}, 404
    