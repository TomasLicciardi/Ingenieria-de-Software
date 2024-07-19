# main/auth/routes.py

from flask import request, jsonify, Blueprint
from .. import db
from main.models import UsuarioModel
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from main.mail.functions import sendMail  # Importar sendMail correctamente

auth = Blueprint('auth', __name__, url_prefix='/auth')

# Métodos de login y registro


#Método de login
@auth.route('/login', methods=['POST'])
def login():
    #Busca el usuario en la db por mail
    usuario = db.session.query(UsuarioModel).filter(UsuarioModel.mail == request.get_json().get("mail")).first_or_404()
    #Valida la contraseña
    if usuario.validate_pass(request.get_json().get("contrasena")):
        #Genera un nuevo token
        #Pasa el objeto usuario como identidad
        access_token = create_access_token(identity=usuario)
        #Devolver valores y token
        data = {
            'id': str(usuario.id),
            'mail': usuario.mail,
            'access_token': access_token
        }
        return data, 200
    else:
        return 'Contraseña Incorecta', 401

#Método de registro
@auth.route('/register', methods=['POST'])
def register():
    #Obtener usuario
    usuario = UsuarioModel.from_json(request.get_json())
    #Verificar si el mail ya existe en la db
    exists = db.session.query(UsuarioModel).filter(UsuarioModel.mail == usuario.mail).scalar() is not None
    if exists:
        return 'Mail duplicado', 409
    else:
        try:
            #Agregar usuario a DB
            db.session.add(usuario)
            db.session.commit()
            sent = sendMail([usuario.mail],"Welcome!",'register',usuario = usuario)
        except Exception as error:
            db.session.rollback()
            return str(error), 409
        return usuario.to_json() , 201