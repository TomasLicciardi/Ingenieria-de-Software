from .. import db
from . import UsuarioModel

tablon_mensaje = db.Table("tablon_mensaje",
    db.Column("id_clase",db.Integer,db.ForeignKey("mensaje.id"),primary_key=True),
    db.Column("id_tablon",db.Integer,db.ForeignKey("tablon.id"),primary_key=True)
    )

class Mensaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(140), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    mensiones = db.Column(db.String(100), nullable=False)
    etiqueta = db.Column(db.String(100), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    usuario = db.relationship("Usuario", back_populates="mensajes",uselist=False, single_parent=True)
    tablones = db.relationship('Tablon', secondary=tablon_mensaje, backref=db.backref('mensaje', lazy='dynamic'))
    


    def __repr__(self):
        return '<mensaje: %r %r %r %r >' % (self.texto,self.autor,self.mensiones,self.etiqueta,self.id_usuario)
    
    def to_json(self):
        mensaje_json = {
            'id': self.id,
            'texto': str(self.texto),
            'autor': str(self.autor),
            'mensiones': str(self.mensiones),
            'etiqueta': str(self.etiqueta)
        }
        return mensaje_json
    
    def to_json_complete(self):
        self.usuario = db.session.query(UsuarioModel).get_or_404(self.id_usuario)

        mensaje_json = {
            'id': self.id,
            'texto': str(self.texto),
            'autor': str(self.autor),
            'mensiones': str(self.mensiones),
            'etiqueta': str(self.etiqueta),
            'usuario': self.usuario.to_json(),
        }
        return mensaje_json
    
    def to_json_complete(self):
        mensaje_json = {
            'id': self.id,
            'texto': str(self.texto),
            'autor': str(self.autor),
            'mensiones': str(self.mensiones),
            'etiqueta': str(self.etiqueta),
            'usuario': self.usuario.to_json(),
            'tablones': [tablon.to_json() for tablon in self.tablones]
        }
        return mensaje_json


    @staticmethod
    def from_json(mensaje_json):
        id = mensaje_json.get('id')
        texto = mensaje_json.get('texto')
        autor = mensaje_json.get('autor')
        mensiones = mensaje_json.get('mensiones')
        etiqueta = mensaje_json.get('etiqueta')
        id_usuario = mensaje_json.get('id_usuario')

        return Mensaje(id=id,
                    texto=texto,
                    autor=autor,
                    mensiones=mensiones,
                    etiqueta=etiqueta,
                    id_usuario = id_usuario
                    )
    