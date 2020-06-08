# importamos la instancia de Flask (app)
from apptrivia import app
import random
import datetime

#Para el formulario
from forms.login import LoginForm

# importamos los modelos a usar
from models.models import Categoria, Pregunta, Respuesta, Usuario

from flask import render_template, session, redirect, url_for, flash


@app.route('/trivia')
@app.route('/')
def index():
    session.clear()
    return "<h2>hola Trivia</h2><a href=\"/trivia/categorias\">Entrar<a>"


@app.route('/trivia/categorias', methods=['GET'])
def mostrarcategorias():
    if 'startTime' not in session:
        session['startTime'] = datetime.datetime.now()
    categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=categorias)


@app.route('/trivia/<int:id_categoria>/pregunta', methods=['GET'])
def mostrarpregunta(id_categoria):
    preguntas = Pregunta.query.filter_by(categoria_id=id_categoria).all()
    # elegir pregunta aleatoria pero de la categoria adecuada
    pregunta = random.choice(preguntas)
    categ = Categoria.query.get(id_categoria)
    res = pregunta.respuestas
    return render_template('preguntas.html', categoria=categ, pregunta=pregunta, respuestas=res)

@app.route('/trivia/<int:id_categoria>/<int:id_pregunta>/respuesta/<int:id_respuesta>', methods=['GET'])
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

@app.route('/trivia/winner')
def winner():
    time = datetime.datetime.now() - session['startTime']
    return render_template('winner.html' , time = time)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        user = Usuario.query.filter_by(email=user.username.data)[0]
        if user and user.check_password(user.password.data):        
            flash('Login Successful for user {}'.format(
                form.username.data))
        return redirect('/login')

    # Limpiando los campos antes. Entra aca la 1era vez o si no valida el form.
    form.username.data=""
    form.password.data = ""
    form.remember_me.date = False
    return render_template('login.html', form=form)