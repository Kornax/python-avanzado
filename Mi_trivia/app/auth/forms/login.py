from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, Email, AnyOf, NoneOf

# Formulario para el login
# class LoginForm(FlaskForm):
#     email = StringField('Email', validators=[InputRequired()])
#     password = PasswordField('Password', validators=[InputRequired()])
#     remember_me = BooleanField('Recuérdame')
#     submit = SubmitField('Login')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message="Debe enviar un email")])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=20), NoneOf({"secret","password"}, message="No es un pass admitido")])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')