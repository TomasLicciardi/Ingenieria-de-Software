from .. import db
from datetime import datetime

class Mensaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(140), nullable=False)
    menciones = db.Column(db.String(100), nullable=False)
    etiqueta = db.Column(db.String(100), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)

    usuario = db.relationship("Usuario", back_populates="mensajes",uselist=False, single_parent=True)
    


    def __repr__(self):
        return '<mensaje: %r %r %r %r %r>' % (self.texto,self.menciones,self.etiqueta,self.id_usuario,self.fecha)
    
    def to_json(self):
        mensaje_json = {
            'id': self.id,
            'texto': str(self.texto),
            'menciones': str(self.menciones),
            'etiqueta': str(self.etiqueta),
            'id_usuario': self.id_usuario,
            'fecha': str(self.fecha.strftime("%d/%m/%Y, %H:%M:%S"))  
        }
        return mensaje_json
    
    def to_json_complete(self):
        from . import UsuarioModel
        self.usuario = db.session.query(UsuarioModel).get_or_404(self.id_usuario)

        mensaje_json = {
            'id': self.id,
            'texto': str(self.texto),
            'menciones': str(self.menciones),
            'etiqueta': str(self.etiqueta),
            'usuario': self.usuario.to_json(),
            'id_usuario': self.id_usuario,
            'fecha': str(self.fecha.strftime("%d/%m/%Y, %H:%M:%S"))
        }
        return mensaje_json


    @staticmethod
    def from_json(mensaje_json):
        id = mensaje_json.get('id')
        texto = mensaje_json.get('texto')
        menciones = mensaje_json.get('menciones')
        etiqueta = mensaje_json.get('etiqueta')
        id_usuario = mensaje_json.get('id_usuario')
        fecha = datetime.strptime(mensaje_json.get('fecha'),"%d/%m/%Y, %H:%M:%S")
        return Mensaje(id=id,
                    texto=texto,
                    menciones=menciones,
                    etiqueta=etiqueta,
                    id_usuario = id_usuario,
                    fecha = fecha
                    )
    