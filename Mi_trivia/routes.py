# importamos la instancia de Flask (app)
from apptrivia import app
import random
import datetime

#Para el Login
from flask_login import current_user, login_user, login_required, logout_user, LoginManager
# para poder usar Flask-Login
login_manager = LoginManager(app)

#Para la excepciones
from werkzeug.exceptions import HTTPException



#Para el formulario
from forms.login import LoginForm
from forms.register import RegisterForm

# importamos los modelos a usar
from models.models import Categoria, Pregunta, Respuesta, Usuario, BestTime

from flask import render_template, session, redirect, url_for, flash, jsonify


@app.route('/trivia')
@app.route('/')
def index():
    session.clear()
    return "<h2>hola Trivia</h2><a href=\"/trivia/categorias\">Entrar<a>"


@app.route('/trivia/categorias', methods=['GET'])
@login_required
def mostrarcategorias():
    if 'startTime' not in session:
        session['startTime'] = datetime.datetime.now()
    categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=categorias)


@app.route('/trivia/<int:id_categoria>/pregunta', methods=['GET'])
@login_required
def mostrarpregunta(id_categoria):
    preguntas = Pregunta.query.filter_by(categoria_id=id_categoria).all()
    # elegir pregunta aleatoria pero de la categoria adecuada
    pregunta = random.choice(preguntas)
    categ = Categoria.query.get(id_categoria)
    res = pregunta.respuestas
    return render_template('preguntas.html', categoria=categ, pregunta=pregunta, respuestas=res)

@app.route('/trivia/<int:id_categoria>/<int:id_pregunta>/respuesta/<int:id_respuesta>', methods=['GET'])
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

@app.route('/trivia/winner')
@login_required
def winner():
    time = datetime.datetime.now() - session['startTime']
    return render_template('winner.html' , time = time)


#le decimos a Flask-Login como obtener un usuario
@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        #get by email valida
        user = Usuario.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            # funcion provista por Flask-Login, el segundo parametro gestion el "recordar"
            login_user(user, remember=form.remember_me.data)
            # next_page = request.args.get('next', None)
            # if not next_page:
            #     next_page = url_for('index')
            return redirect(url_for('index'))

        else:
            flash('Usuario o contraseña inválido')
            return redirect(url_for('login'))
    # no loggeado, dibujamos el login con el form vacio
    return render_template('login.html', form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = Usuario.get_by_email(email)
        if user is not None:
            flash('El email {} ya está siendo utilizado por otro usuario'.format(email))
        else:
            # Creamos el usuario y lo guardamos
            user = Usuario(name=username, email=email)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            return redirect(url_for('index'))
    return render_template("register.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#Errores

@app.errorhandler(404)
def page_not_found(e):
    #return jsonify(error=str(e)), 404
    return render_template('404.html')


@app.errorhandler(401)
def unathorized(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify(error=str(e)), e.code

#Rankings
@app.route("/rankings")
def rankings():
    bestTime = BestTime.query.all()
    return render_template("ranking.html", bestTime=bestTime)