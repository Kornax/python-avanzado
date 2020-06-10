from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, Email, AnyOf

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Email(message="Debe enviar un email")])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=20), AnyOf({"secret","password"}, message="No es un pass admitido")])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
