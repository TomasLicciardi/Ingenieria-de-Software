from .. import db
from werkzeug.security import generate_password_hash, check_password_hash

Seguidores = db.Table('seguidores',
    db.Column('seguidor_id', db.Integer, db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('seguido_id', db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(100), nullable=False)
    foto = db.Column(db.String(200), nullable=False)
    contrasena = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(300), nullable=False)


    tablon = db.relationship("Tablon", uselist=False, back_populates="usuario", cascade='all, delete-orphan', single_parent=True)
    muro = db.relationship("Muro", uselist=False, back_populates="usuario", cascade='all, delete-orphan', single_parent=True)
    mensajes_privados = db.relationship("Mensaje_Privado", back_populates='usuario', cascade='all, delete-orphan')
    mensajes = db.relationship("Mensaje", back_populates='usuario', cascade='all, delete-orphan')
    seguidores = db.relationship("Usuario",
                                 secondary=Seguidores,
                                 primaryjoin=(Seguidores.c.seguidor_id == id),
                                 secondaryjoin=(Seguidores.c.seguido_id == id),
                                 backref=db.backref('siguiendo', lazy='dynamic'),
                                 lazy='dynamic')
    seguidos = db.relationship("Usuario",
                                 secondary=Seguidores,
                                 primaryjoin=(Seguidores.c.seguido_id == id),
                                 secondaryjoin=(Seguidores.c.seguidor_id == id),
                                 backref=db.backref('seguidor', lazy='dynamic'),
                                 lazy='dynamic')


    @property
    def plain_contrasena(self):
        raise AttributeError('contrasena no puede ser leida')
    @plain_contrasena.setter
    def plain_contrasena(self, contrasena):
        self.contrasena = generate_password_hash(contrasena)
    # Método que compara una contrasena en texto plano con el hash guardado en la db
    def validate_pass(self,contrasena):
        return check_password_hash(self.contrasena, contrasena)

    def __repr__(self):
        return '<usuario: %r %r %r %r %r >' % (self.alias, self.nombre, self.mail, self.foto, self.descripcion)
    
    def to_json(self):
        usuario_json = {
            'id': self.id,
            'alias': str(self.alias),
            'nombre': str(self.nombre),
            'mail': str(self.mail),
            'foto': str(self.foto),
            'contrasena': str(self.contrasena),
            'descripcion': str(self.descripcion),
        }
        return usuario_json
    
    def to_json_token(self):
        usuario_json = {
            'id': self.id,
            'mail': str(self.mail),
        }
        return usuario_json
    
    def to_json_complete(self):
        mensajes_privados = [mensaje_privado.to_json() for mensaje_privado in self.mensajes_privados]
        mensajes = [mensaje.to_json() for mensaje in self.mensajes]
        seguidores = [seguidor.to_json() for seguidor in self.seguidores]

        usuario_json = {
            'id': self.id,
            'alias': str(self.alias),
            'nombre': str(self.nombre),
            'mail': str(self.mail),
            'foto': str(self.foto),
            'contrasena': str(self.contrasena),
            'descripcion': str(self.descripcion),
            'mensajes_privados': str(self.mensajes_privados),
            'mensajes': str(self.mensajes),
            'seguidores': self.seguidores
        }
        return usuario_json

    @staticmethod
    def from_json(usuario_json):
        id = usuario_json.get('id')
        alias = usuario_json.get('alias')
        nombre = usuario_json.get('nombre')
        mail = usuario_json.get('mail')
        foto = usuario_json.get('foto')
        contrasena = usuario_json.get('contrasena')
        descripcion = usuario_json.get('descripcion')

        return Usuario(id=id,
                       alias=alias,
                       nombre=nombre,
                       mail=mail,
                       foto=foto,
                       plain_contrasena=contrasena,
                       descripcion=descripcion,)
