# app/public/routes.py

from app import login_required, current_user
from flask import render_template, session
from . import public_bp
from .models import Categoria, Pregunta, Respuesta, BestTime
import random
import datetime

@public_bp.route('/trivia')
@public_bp.route('/')
def index_trivia():
    return render_template('trivia.html')

@public_bp.route('/trivia/categorias', methods=['GET'])
@login_required
def mostrarcategorias():
    if 'startTime' not in session:
        session['startTime'] = datetime.datetime.now()
    categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=categorias)


@public_bp.route('/trivia/<id_categoria>/pregunta', methods=['GET'])
@login_required
def mostrarpregunta(id_categoria):
    preguntas = Pregunta.query.filter_by(categoria_id=id_categoria).all()
    # elegir pregunta aleatoria pero de la categoria adecuada
    pregunta = random.choice(preguntas)
    categ = Categoria.query.get(id_categoria)
    res = pregunta.respuestas
    return render_template('preguntas.html', categoria=categ, pregunta=pregunta, respuestas=res)

@public_bp.route('/trivia/<int:id_categoria>/<int:id_pregunta>/respuesta/<int:id_respuesta>', methods=['GET'])
@login_required
def mostrarRespuesta(id_categoria, id_pregunta, id_respuesta):
    respuesta = Respuesta.query.filter_by(id=id_respuesta)[0]
    if str(id_categoria) not in session:
        session[str(id_categoria)] = respuesta.answer
    categorias = [str(c.id) for c in Categoria.query.all()]
    categoriasAnswers = [session[i] for i in categorias if i in session]
    if all(categoriasAnswers) and len(categorias) == len(categoriasAnswers) :
        return redirect(url_for('winner'))
    else:
        return render_template('respuesta.html' , respuesta=respuesta)

@public_bp.route('/trivia/winner', methods=['GET'])
@login_required
def winner():
    time = datetime.datetime.now() - session.pop('startTime', None)
    bestTime = BestTime(usuario_id=current_user.id,time_seconds=time.total_seconds(), date=datetime.datetime.now())
    bestTime.save()
    return render_template('winner.html' , time = time)

#Rankings
@public_bp.route("/trivia/rankings", methods=['GET'])
def rankings():
    bestTime = BestTime.query.all()
    bestTime = sorted(bestTime, key = lambda i:i.time_seconds)
    return render_template("ranking.html", bestTime=bestTime)





