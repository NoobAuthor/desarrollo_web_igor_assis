from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
class Region(db.Model):
    __tablename__ = 'region'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    comunas = db.relationship('Comuna', backref='region', lazy=True)

class Comuna(db.Model):
    __tablename__ = 'comuna'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    # Changed relationship definition
    actividades = db.relationship('Actividad', backref='comuna', lazy=True)

class Comentario(db.Model):
    __tablename__ = 'comentario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    texto = db.Column(db.String(300), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    actividad_id = db.Column(db.Integer, db.ForeignKey('actividad.id'), nullable=False)

class Actividad(db.Model):
    __tablename__ = 'actividad'
    id = db.Column(db.Integer, primary_key=True)
    comuna_id = db.Column(db.Integer, db.ForeignKey('comuna.id'), nullable=False)
    sector = db.Column(db.String(100))
    nombre = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.String(15))
    dia_hora_inicio = db.Column(db.DateTime, nullable=False)
    dia_hora_termino = db.Column(db.DateTime)
    descripcion = db.Column(db.String(500))

    # Removed duplicate comuna relationship and kept only the backref from Comuna
    fotos = db.relationship('Foto', backref='actividad', lazy=True)
    contactos = db.relationship('ContactarPor', backref='actividad', lazy=True)
    temas = db.relationship('ActividadTema', backref='actividad', lazy=True)
    comentarios = db.relationship('Comentario', backref='actividad', lazy=True)
    notas = db.relationship('Nota', backref='actividad', lazy=True)

class Foto(db.Model):
    __tablename__ = 'foto'
    id = db.Column(db.Integer, primary_key=True)
    ruta_archivo = db.Column(db.String(300), nullable=False)
    nombre_archivo = db.Column(db.String(300), nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey('actividad.id'), nullable=False)

class ContactarPor(db.Model):
    __tablename__ = 'contactar_por'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    identificador = db.Column(db.String(50), nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey('actividad.id'), nullable=False)

class ActividadTema(db.Model):
    __tablename__ = 'actividad_tema'
    id = db.Column(db.Integer, primary_key=True)
    tema = db.Column(db.String(15), nullable=False)
    glosa_otro = db.Column(db.String(15))
    actividad_id = db.Column(db.Integer, db.ForeignKey('actividad.id'), nullable=False)

class Nota(db.Model):
    __tablename__ = 'nota'
    id = db.Column(db.Integer, primary_key=True)
    actividad_id = db.Column(db.Integer, db.ForeignKey('actividad.id'), nullable=False)
    nota = db.Column(db.Integer, nullable=False)
