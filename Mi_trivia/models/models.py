# importamos la instancia de la BD
from apptrivia import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
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

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean)
    tiempos = db.relationship('BestTime', backref='usuario', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<Usuario: {}>'.format(self.email)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Usuario.query.get(id)

    @staticmethod
    def get_by_email(email):
        return Usuario.query.filter_by(email=email).first()

class BestTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    time_seconds = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    def __repr__(self):
        return '<Best Time %s>' % self.usuario_id

    def save(self):
        besTime = BestTime.query.filter_by(usuario_id=self.usuario_id).first()
        if besTime:
            besTime.time_seconds = self.time_seconds
            besTime.date = self.date
        elif not self.id:
            db.session.add(self)
        db.session.commit()
    
    def usuario_name(self):
        return Usuario.query.filter_by(id=self.usuario_id)[0].name
    
    def time(self):
        return str(datetime.timedelta(seconds=self.time_seconds))
