from flask_restful import Resource
from main.models import Tablon_TendenciasModel, TablonModel, MensajeModel
from .. import db
from flask import request, jsonify

class Tablon(Resource):
    def get(self, id):
        tablon = db.session.query(TablonModel).get_or_404(id)
        return tablon.to_json()
    
    def put(self, id):
        tablon = db.session.query(TablonModel).get_or_404(id)
        data = request.get_json().items()
        print(data)
        for key, value in data:
            setattr(tablon, key, value)
                
        db.session.add(tablon)
        db.session.commit()
        return tablon.to_json(), 201
    
    def delete(self, id):
        tablon = db.session.query(TablonModel).get_or_404(id)
        db.session.delete(tablon)
        db.session.commit()
        return '', 204

class Tablones(Resource):
    def get(self):
        tablones = db.session.query(TablonModel)
        return jsonify({'tablon': [tablon.to_json() for tablon in tablones] })

    def post(self):
        data = request.get_json()
        id = data.get('id_usuario')
        tablon_existente = db.session.query(TablonModel).filter_by(id_usuario=id).first()
        if (tablon_existente):
            return "Ya existe un tablon para este usuario", 400
        tablon = TablonModel.from_json(data)
        try:
            db.session.add(tablon)
            db.session.commit()
        except:
            return "Formato no correcto", 400
        return tablon.to_json(), 201

    
class TablonMensajes(Resource):
    def get(self, id):
        tablon = db.session.query(TablonModel).get_or_404(id)
        mensajes = tablon.mensajes
        mensajes_json = [mensaje.to_json() for mensaje in mensajes]
        return mensajes_json
         
    def post(self, id):
        data = request.get_json()
        id_mensaje = data.get('id_mensaje')
        mensaje = db.session.query(MensajeModel).get_or_404(id_mensaje)
        tablon = db.session.query(TablonModel).get_or_404(id)
        if mensaje and tablon:
            tablon.mensajes.append(mensaje)
            db.session.commit()
            return {'message': 'Mensaje agregado al tablon exitosamente'}, 201
        else:
            return {'message': 'El mensaje o el tablon no existen.'}, 404

    

class Tablon_Tendencias(Resource):
    def get(self, id):
        tablon_tendencias = db.session.query(Tablon_TendenciasModel).get_or_404(id)
        return tablon_tendencias.to_json()
    
    def put(self, id):
        tablon_tendencias = db.session.query(Tablon_TendenciasModel).get_or_404(id)
        data = request.get_json().items()
        print(data)
        for key, value in data:
            setattr(tablon_tendencias, key, value)
                
        db.session.add(tablon_tendencias)
        db.session.commit()
        return tablon_tendencias.to_json(), 201
    
    def delete(self, id):
        tablon_tendencias = db.session.query(Tablon_TendenciasModel).get_or_404(id)
        db.session.delete(tablon_tendencias)
        db.session.commit()
        return '', 204
    
class Tablones_Tendencias(Resource):
    def get(self):
        tablon_tendencias = db.session.query(Tablon_TendenciasModel)
        return jsonify({'tablon_tendencias': [tablon_tendencias.to_json() for tablon_tendencias in tablon_tendencias] })

    def post(self):
        tablon_tendencias = Tablon_TendenciasModel.from_json(request.get_json())
        print(tablon_tendencias)
        try:
            db.session.add(tablon_tendencias)
            db.session.commit()
        except:
            return "Formato no correcto", 400
        return tablon_tendencias.to_json(), 201
