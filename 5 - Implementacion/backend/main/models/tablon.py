from .. import db


class Tablon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mensajes = db.Column(db.String(140), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    tablon_tendencias = db.relationship("Tablon_Tendencias", uselist=False,back_populates="tablon",cascade="all, delete-orphan",single_parent=True)
    usuario = db.relationship("Usuario", uselist=False,back_populates="tablon",cascade="all, delete-orphan",single_parent=True)



    def __repr__(self):
        return '<tablon: %r %r >' % (self.mensajes,self.id_usuario)
    
    def to_json(self):
        from . import UsuarioModel
        self.usuario = db.session.query(UsuarioModel).get_or_404(self.id_usuario)
        tablon_json = {
            'id': self.id,
            'mensajes': str(self.mensajes),
            'usuario': self.usuario.to_json(),
        }
        return tablon_json
    

    @staticmethod
    def from_json(tablon_json):
        id = tablon_json.get('id')
        mensajes = tablon_json.get('mensajes')
        id_usuario = tablon_json.get('id_usuario')

        return Tablon(id=id,
                    mensajes=mensajes,
                    id_usuario=id_usuario
                    )
    