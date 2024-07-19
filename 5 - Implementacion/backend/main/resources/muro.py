from flask_restful import Resource
from main.models import MuroModel
from .. import db
from flask import request, jsonify


class Muro(Resource):
    def get(self, id):
        muro = db.session.query(MuroModel).get_or_404(id)
        return muro.to_json()
    
    def put(self, id):
        muro = db.session.query(MuroModel).get_or_404(id)
        data = request.get_json().items()
        print(data)
        for key, value in data:
            setattr(muro, key, value)
                
        db.session.add(muro)
        db.session.commit()
        return muro.to_json(), 201
    
    def delete(self, id):
        muro = db.session.query(MuroModel).get_or_404(id)
        db.session.delete(muro)
        db.session.commit()
        return '', 204
    
class Muros(Resource):
    def get(self):
        muros = db.session.query(MuroModel)
        return jsonify({'muro': [muro.to_json() for muro in muros] })

    def post(self):
        data = request.get_json()
        id = data.get('id_usuario')
        muro_existente = db.session.query(MuroModel).filter_by(id_usuario=id).first()
        if (muro_existente):
            return "Ya existe un muro para este usuario", 400
        muro = MuroModel.from_json(data)
        print(muro)
        try:
            db.session.add(muro)
            db.session.commit()
        except:
            return "Formato no correcto", 400
        return muro.to_json(), 201
