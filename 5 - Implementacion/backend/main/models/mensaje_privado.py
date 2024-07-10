from .. import db
from . import UsuarioModel

class Mensaje_Privado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(140), nullable=False)
    origen = db.Column(db.String(100), nullable=False)
    destino = db.Column(db.String(100), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    usuario = db.relationship("Usuario", back_populates="mensajes_privados",uselist=False, single_parent=True)

    
    def __repr__(self):
        return '<mensaje_privado: %r %r %r %r >' % (self.texto,self.origen,self.destino,self.id_usuario)
    
    def to_json(self):
        mensaje_privado_json = {
            'id': self.id,
            'texto': str(self.texto),
            'origen': str(self.origen),
            'destino': str(self.destino),
        }
        return mensaje_privado_json
    
    def to_json_complete(self):
        self.usuario = db.session.query(UsuarioModel).get_or_404(self.id_usuario)
        
        mensaje_privado_json = {
            'id': self.id,
            'texto': str(self.texto),
            'origen': str(self.origen),
            'destino': str(self.destino),
            'usuario': self.usuario.to_json(),
        }
        return mensaje_privado_json


    @staticmethod
    def from_json(mensaje_privado_json):
        id = mensaje_privado_json.get('id')
        texto = mensaje_privado_json.get('texto')
        origen = mensaje_privado_json.get('origen')
        destino = mensaje_privado_json.get('destino')
        id_usuario = mensaje_privado_json.get('id_usuario')

        return Mensaje_Privado(id=id,
                    texto=texto,
                    origen=origen,
                    destino=destino,
                    id_usuario = id_usuario
                    )
    