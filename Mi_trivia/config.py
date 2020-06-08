import os

# configuraciones. True para que el servidor pueda ser levantado en modo debug
DEBUG = True

# configuracion BD
""""
SECRET_KEY =  'A SECRET KEY'
SQLALCHEMY_TRACK_MODIFICATIONS = False
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'models/trivia.db')
"""

POSTGRES = {
    'user': 'postgres',
    'pw': 'cursoflask',
    'db': 'trivia',
    'host': 'localhost',
    'port': '5432',
}
SECRET_KEY =  'A SECRET KEY'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
