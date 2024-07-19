from .. import db

class Muro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mensaje = db.Column(db.String(140), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    usuario = db.relationship("Usuario", uselist=False,back_populates="muro",cascade="all, delete-orphan",single_parent=True)



    def __repr__(self):
        return '<muro: %r %r >' % (self.mensaje,self.id_usuario)
    
    def to_json(self):
        from . import UsuarioModel
        self.usuario = db.session.query(UsuarioModel).get_or_404(self.id_usuario)
        muro_json = {
            'id': self.id,
            'mensaje': str(self.mensaje),
            'usuario': self.usuario.to_json(),
        }
        return muro_json
    

    @staticmethod
    def from_json(muro_json):
        id = muro_json.get('id')
        mensaje = muro_json.get('mensaje')
        id_usuario = muro_json.get('id_usuario')

        return Muro(id=id,
                    mensaje=mensaje,
                    id_usuario=id_usuario
                    )
    