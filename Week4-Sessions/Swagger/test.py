import connexion
from flask import render_template

app = connexion.App(__name__, specification_dir='doc/')
app.add_api('api.yml')


@app.route('/')
def home():
    return render_template("hola.html")

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

