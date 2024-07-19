from .. import db

tablon_mensaje = db.Table("tablon_mensaje",
    db.Column("id_mensaje",db.Integer,db.ForeignKey("mensaje.id"),primary_key=True),
    db.Column("id_tablon",db.Integer,db.ForeignKey("tablon.id"),primary_key=True)
    )

class Tablon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    tablon_tendencias = db.relationship("Tablon_Tendencias", uselist=False,back_populates="tablon",cascade="all, delete-orphan",single_parent=True)
    usuario = db.relationship("Usuario", uselist=False,back_populates="tablon",cascade="all, delete-orphan",single_parent=True)
    mensajes = db.relationship('Mensaje', secondary=tablon_mensaje, backref=db.backref('tablon', lazy='dynamic'))


    def __repr__(self):
        return '<tablon: %r >' % (self.id_usuario)
    
    def to_json(self):
        from . import UsuarioModel
        self.usuario = db.session.query(UsuarioModel).get_or_404(self.id_usuario)
        tablon_json = {
            'id': self.id,
            'usuario': self.usuario.to_json(),
            'mensajes': [mensaje.to_json() for mensaje in self.mensajes]
        }
        return tablon_json

    @staticmethod
    def from_json(tablon_json):
        id = tablon_json.get('id')
        id_usuario = tablon_json.get('id_usuario')

        return Tablon(id=id,
                    id_usuario=id_usuario
                    )
    