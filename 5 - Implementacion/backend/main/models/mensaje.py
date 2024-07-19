from .. import db

class Mensaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(140), nullable=False)
    mensiones = db.Column(db.String(100), nullable=False)
    etiqueta = db.Column(db.String(100), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    usuario = db.relationship("Usuario", back_populates="mensajes",uselist=False, single_parent=True)
    


    def __repr__(self):
        return '<mensaje: %r %r %r %r >' % (self.texto,self.mensiones,self.etiqueta,self.id_usuario)
    
    def to_json(self):
        mensaje_json = {
            'id': self.id,
            'texto': str(self.texto),
            'mensiones': str(self.mensiones),
            'etiqueta': str(self.etiqueta)
        }
        return mensaje_json
    
    def to_json_complete(self):
        from . import UsuarioModel
        self.usuario = db.session.query(UsuarioModel).get_or_404(self.id_usuario)

        mensaje_json = {
            'id': self.id,
            'texto': str(self.texto),
            'mensiones': str(self.mensiones),
            'etiqueta': str(self.etiqueta),
            'usuario': self.usuario.to_json(),
        }
        return mensaje_json


    @staticmethod
    def from_json(mensaje_json):
        id = mensaje_json.get('id')
        texto = mensaje_json.get('texto')
        mensiones = mensaje_json.get('mensiones')
        etiqueta = mensaje_json.get('etiqueta')
        id_usuario = mensaje_json.get('id_usuario')

        return Mensaje(id=id,
                    texto=texto,
                    mensiones=mensiones,
                    etiqueta=etiqueta,
                    id_usuario = id_usuario
                    )
    