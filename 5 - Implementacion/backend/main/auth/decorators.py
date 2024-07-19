from .. import jwt
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from .. import db

#Define el atributo que se utilizará para identificar el usuario
@jwt.user_identity_loader
def user_identity_lookup(usuario):
    #Definir ID como atributo identificatorio
    return usuario.id

#Define que atributos se guardarán dentro del token
@jwt.additional_claims_loader
def add_claims_to_access_token(usuario):
    claims = {
        'id': usuario.id,
        'mail': usuario.mail
    }
    return claims