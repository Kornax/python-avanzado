from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_principal import identity_loaded,Permission,RoleNeed

# instancia Flask
app = Flask(__name__)
admin = Admin(app)

# lee la config desde el archivo config.py
app.config.from_pyfile('config.py')

# inicializa la base de datos con la config leida
db = SQLAlchemy(app)

# rutas disponibles
from routes import *
from models.models import Categoria, Pregunta, Respuesta, Usuario, BestTime, Role

#Acceso Admin al /admin
from flask import g
admin_permission = Permission(RoleNeed('admin'))
#Para el login de los usuarios
# class MyAdminIndexView(AdminIndexView):
#     def is_accessible(self):
#         has_auth = current_user.is_authenticated
#         has_perm = admin_permission.allows(g.identity)
#         return has_auth and has_perm

#Para el login de los usuarios
class MyModelView(ModelView):
    def is_accessible(self):
        has_auth = current_user.is_authenticated
        has_perm = admin_permission.allows(g.identity)
        return has_auth and has_perm

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

# los modelos que queremos mostrar en el admin
admin.add_view(MyModelView(Categoria, db.session))
admin.add_view(ModelView(Pregunta, db.session))
admin.add_view(ModelView(Respuesta, db.session))
admin.add_view(ModelView(BestTime, db.session))
admin.add_view(MyModelView(Usuario, db.session))

# subimos el server (solo cuando se llama directamente a este archivo)
if __name__ == '__main__':
    app.run()

##MIGRACION de BASE DE DATOS
from flask_migrate import Migrate

migrate = Migrate()
migrate.init_app(app, db)

admin.add_view(MyModelView(Role, db.session)) #para verlo en "/admin"

# Creamos un permiso, para ser satisfecho hay que ser Admin
admin_permission = Permission(RoleNeed('admin'))

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Seteamos la identidad con el usuario actual
    identity.user = current_user
    # La identidad proveerá una Need para current_user.
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))
    # Agregamos a la identidad la lista de roles que posee el usuario
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.rolename))