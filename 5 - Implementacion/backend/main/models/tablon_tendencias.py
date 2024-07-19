from .. import db

class Tablon_Tendencias(db.Model):
    id_tablon = db.Column(db.Integer, db.ForeignKey("tablon.id"), primary_key=True)
    n_dias = db.Column(db.Integer, nullable=False)
    tema = db.Column(db.String(140), nullable=False)
    
    tablon = db.relationship("Tablon", uselist=False, back_populates="tablon_tendencias", cascade = 'all, delete-orphan', single_parent=True)


    def __repr__(self):
        return '<tablon_tendencias: %r %r >' % (self.n_dias,self.tema)
    
    def to_json(self):
        from . import TablonModel
        self.tablon = db.session.query(TablonModel).get_or_404(self.id_tablon)
        tablon_tendencias_json = {
            'tablon': self.tablon.to_json(),
            'n_dias': self.n_dias,
            'tema': str(self.tema),
        }
        return tablon_tendencias_json
    

    @staticmethod
    def from_json(tablon_tendencias_json):
        id_tablon = tablon_tendencias_json.get('id_tablon')
        n_dias = tablon_tendencias_json.get('n_dias')
        tema = tablon_tendencias_json.get('tema')
    
        return Tablon_Tendencias(id_tablon=id_tablon,
                    n_dias=n_dias,
                    tema=tema
                    )
    