#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apptrivia import db
from models.models import Categoria, Pregunta, Respuesta, Usuario

db.drop_all()
db.create_all()

# categorias
c_geogra = Categoria(descripcion="Geografía")
c_deporte = Categoria(descripcion="Deportes")

# preguntas
q_Laos = Pregunta(text="¿Cuál es la capital de Laos?", categoria = c_geogra)
q_Armenia = Pregunta(text="¿Cuál es la población aproximada de Armenia?", categoria = c_geogra)
q_mundial = Pregunta(text="¿En qué país se jugó la Copa del Mundo de 1962?", categoria = c_deporte)
#Respuestas de Laos
r_Laos1 = Respuesta(text="Vientiane", answer=True, pregunta = q_Laos)
r_Laos2 = Respuesta(text="Oslo", answer=False,  pregunta = q_Laos)
r_Laos3 = Respuesta(text="Barcelona", answer=True, pregunta = q_Laos)
#Respuestas de Armenia
r_Armenia1 = Respuesta(text="3 millones", answer=True,  pregunta = q_Armenia)
r_Armenia2 = Respuesta(text="45 millones", answer=False,  pregunta = q_Armenia)
r_Armenia3 = Respuesta(text="300.000", answer=False,  pregunta = q_Armenia)
#Respuesta de Mundial
r_mundial1 = Respuesta(text="Chile", answer=True, pregunta = q_mundial)
r_mundial2 = Respuesta(text="Francia", answer=False,  pregunta = q_mundial)
r_mundial3 = Respuesta(text="Estados Unidos", answer=False, pregunta = q_mundial)

#Usuario
u_ernesto = Usuario(name="ernesto", email="jeabreugentini@gmial.com", is_admin=True)
u_ernesto.set_password("12345")

db.session.add(c_geogra)
db.session.add(c_deporte)
db.session.add(q_Laos)
db.session.add(q_Armenia)
db.session.add(q_mundial)
db.session.add(r_Laos1)
db.session.add(r_Laos2)
db.session.add(r_Laos3)
db.session.add(r_Armenia1)
db.session.add(r_Armenia2)
db.session.add(r_Armenia3)
db.session.add(r_mundial1)
db.session.add(r_mundial2)
db.session.add(r_mundial3)
db.session.add(u_ernesto)
db.session.commit()

# creamos otros usuarios (…) y los recorremos
categorias = Categoria.query.all()
for c in categorias:
    print(c.id, c.descripcion)
    # para cada categoria, obtenemos sus preguntas y las recorremos
    for p in c.preguntas:
        print(p.id, p.text)


cat = Categoria.query.get(1)
print(cat)

