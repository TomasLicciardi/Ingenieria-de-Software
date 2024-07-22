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
            if key == 'contrasena':
                usuario.plain_contrasena = value
            else:
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
        try:
            db.session.add(usuario)
            db.session.commit()
        except:
            return "Formato no correcto", 400
        return usuario.to_json(), 201
    

class UsuarioSeguidos(Resource):
    def get(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        seguidores = usuario.seguidores
        seguidores_json = [seguidor.to_json() for seguidor in seguidores]
        return seguidores_json
     
    def post(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        usuario_a_seguir = request.get_json().get('usuario_a_seguir')
        seguidor = db.session.query(UsuarioModel).get_or_404(usuario_a_seguir)
        if (int(id) == usuario_a_seguir):
            return{'mensaje': 'No te podes seguir vos mismo'}, 400
        if not seguidor in usuario.seguidores:
            usuario.seguidores.append(seguidor)
            db.session.commit()
            return usuario.to_json(), 201
        return {'message': 'Ya estas siguiendo este usuario'}, 400

    def delete(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        usuario_a_dejar_de_seguir = request.get_json().get('usuario_a_dejar_de_seguir')
        seguidor = db.session.query(UsuarioModel).get_or_404(usuario_a_dejar_de_seguir)

        if seguidor in usuario.seguidores:
            usuario.seguidores.remove(seguidor)
            db.session.commit()
            return '', 204
        return {'message': 'No estas siguiendo este usuario'}, 400



class UsuarioSeguidores(Resource):
    def get(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        seguidos = usuario.seguidos
        seguidos_json = [seguido.to_json() for seguido in seguidos]
        return seguidos_json
