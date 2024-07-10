from .. import db

seguimientos = db.Table('seguimientos',
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
    seguidores = db.Column(db.Integer(50), nullable=False)
    seguidos = db.Column(db.Integer(50), nullable=False)

    tablon = db.relationship("Tablon", uselist=False, back_populates="usuario", cascade = 'all, delete-orphan', single_parent=True)
    muro = db.relationship("Muro", uselist=False, back_populates="usuario", cascade = 'all, delete-orphan', single_parent=True)
    mensajes_privados = db.relationship("Mensaje_Privado", back_populates='usuario', cascade='all, delete-orphan')
    mensajes = db.relationship("Mensaje", back_populates='usuario', cascade='all, delete-orphan')
    seguidos = db.relationship("Usuario", 
                               secondary=seguimientos,
                               primaryjoin=(seguimientos.c.seguidores_id == id),
                               secondaryjoin=(seguimientos.c.seguido_id == id),
                               backref=db.backref('seguidores', lazy='dynamic'),
                               lazy='dynamic')


    def __repr__(self):
        return '<usuario: %r %r %r %r %r %r %r >' % (self.alias,self.nombre,self.mail,self.foto,self.descripcion,self.seguidores,self.seguidos)
    
    def to_json(self):
        usuario_json = {
            'id': self.id,
            'alias': str(self.alias),
            'nombre': str(self.nombre),
            'mail': str(self.mail),
            'foto': str(self.foto),
            'contrasena':str(self.contrasena),
            'descripcion': str(self.descripcion),
            'seguidores': self.seguidores,
            'seguidos': self.seguidos
        }
        return usuario_json
    
    def to_json_complete(self):
        mensajes_privados = [mensaje_privado.to_json() for mensaje_privado in self.mensajes_privados]
        mensajes = [mensaje.to_json() for mensaje in self.mensajes]

        usuario_json = {
            'id': self.id,
            'alias': str(self.alias),
            'nombre': str(self.nombre),
            'mail': str(self.mail),
            'foto': str(self.foto),
            'contrasena':str(self.contrasena),
            'descripcion': str(self.descripcion),
            'seguidores': self.seguidores,
            'seguidos': self.seguidos,
            'mensajes_privados': mensajes_privados,
            'mensajes': mensajes,
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
        seguidores = usuario_json.get('seguidores')
        seguidos = usuario_json.get('seguidos')

        return Usuario(id=id,
                    alias=alias,
                    nombre=nombre,
                    mail=mail,
                    foto=foto,
                    plain_contraseña=contrasena,
                    descripcion=descripcion,
                    seguidores=seguidores,
                    seguidos=seguidos,
                    )
    