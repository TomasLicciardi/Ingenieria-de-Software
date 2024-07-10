from .. import db
from . import UsuarioModel

class Tablon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mensaje = db.Column(db.String(140), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    tablon_tendencias = db.relationship("Tablon_Tendencias", uselist=False,back_populates="tablon",cascade="all, delete-orphan",single_parent=True)
    usuario = db.relationship("Usuario", uselist=False,back_populates="tablon",cascade="all, delete-orphan",single_parent=True)



    def __repr__(self):
        return '<tablon: %r %r >' % (self.mensaje,self.id_usuario)
    
    def to_json(self):
        self.usuario = db.session.query(UsuarioModel).get_or_404(self.id_usuario)
        tablon_json = {
            'id': self.id,
            'mensaje': str(self.mensaje),
            'usuario': self.usuario.to_json(),
        }
        return tablon_json
    

    @staticmethod
    def from_json(tablon_json):
        id = tablon_json.get('id')
        mensaje = tablon_json.get('mensaje')
        id_usuario = tablon_json.get('id_usuario')

        return Tablon(id=id,
                    mensaje=mensaje,
                    id_usuario=id_usuario
                    )
    