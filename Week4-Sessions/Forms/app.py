from forms.login import LoginForm
from flask import flash, redirect, Flask, render_template
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def home():
    return "hola"

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/login')

    # Limpiando los campos antes. Entra aca la 1era vez o si no valida el form.
    form.username.data=""
    form.password.data = ""
    form.remember_me.date = False
    return render_template('login.html', form=form)



if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
