from app import db
from ..auth.models import Usuario
import datetime

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(64), index=True, unique=True)
    preguntas = db.relationship('Pregunta', backref='categoria', lazy='dynamic')
    def __repr__(self):
        return '<Categoria: {}>'.format(self.descripcion)


class Pregunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False, unique=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    respuestas = db.relationship('Respuesta', backref='pregunta', lazy='dynamic')
    def __repr__(self):
        return '<Pregunta %s>' % self.text

class Respuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Boolean, nullable=False)
    pregunta_id = db.Column(db.Integer, db.ForeignKey('pregunta.id'))
    def __repr__(self):
        return '<Respuesta %s>' % self.text

class BestTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    time_seconds = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    def __repr__(self):
        return '<Best Time %s>' % self.usuario_id

    def save(self):
        bestTime = BestTime.query.filter_by(usuario_id=self.usuario_id).first()
        if bestTime and bestTime.time_seconds > self.time_seconds:
            bestTime.time_seconds = self.time_seconds
            bestTime.date = self.date
        elif not bestTime:
            db.session.add(self)
        db.session.commit()
    
    def usuario_name(self):
        return Usuario.query.filter_by(id=self.usuario_id).first().name
    
    def time(self):
        return str(datetime.timedelta(seconds=self.time_seconds))

