from flask_restful import Resource
from main.models import UsuarioModel, SeguidoresModel
from .. import db
from flask import request, jsonify



class Usuario(Resource):
    def get(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        return usuario.to_json()
    
    def put(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        print(data)
        for key, value in data:
            setattr(usuario, key, value)
                
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201
    
    def delete(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204
    
class Usuarios(Resource):
    def get(self):
        usuarios = db.session.query(UsuarioModel)
        return jsonify({'usuario': [usuario.to_json() for usuario in usuarios] })

    def post(self):
        usuario = UsuarioModel.from_json(request.get_json())
        print(usuario)
        try:
            db.session.add(usuario)
            db.session.commit()
        except:
            return "Formato no correcto", 400
        return usuario.to_json(), 201
    

class UsuarioSeguidores(Resource):
    def post(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        usuario_actual = request.get_json().get('usuario_actual')
        seguidor = db.session.query(UsuarioModel).get_or_404(usuario_actual)
        if (int(id) == usuario_actual):
            
            return{'mensaje': 'No te podes seguir vos mismo'}, 400
        
        if not seguidor in usuario.seguidores:
            usuario.seguidores.append(seguidor)
            db.session.commit()
            return usuario.to_json(), 201
        return {'message': 'El usuario ya está siguiendo'}, 400

    def get(self, id):
        usuario = db.session.query(SeguidoresModel).get_or_404(id)
        return jsonify({'seguidores': [seguidor.to_json() for seguidor in usuario.seguidores]})

    def delete(self, id):
        usuario = db.session.query(SeguidoresModel).get_or_404(id)
        usuario_actual = request.get_json().get('usuario_actual')
        seguidor = db.session.query(SeguidoresModel).get_or_404(usuario_actual)

        if seguidor in usuario.seguidores:
            usuario.seguidores.remove(seguidor)
            db.session.commit()
            return '', 204
        return {'message': 'El usuario no está siguiendo'}, 400