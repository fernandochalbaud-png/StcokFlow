from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from database import db
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

database_url = os.getenv('DATABASE_URL', 'sqlite:///stockflow.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'stockflow-secret-2024')
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 5,
    'pool_recycle': 300,
    'pool_pre_ping': True
}
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'vistas.login_page'

@login_manager.user_loader
def load_user(user_id):
    from models import Usuario
    return Usuario.query.get(int(user_id))

from routes.vistas import vistas_bp
from routes.auth import auth_bp
from routes.productos import productos_bp
from routes.entradas import entradas_bp
from routes.salidas import salidas_bp
from routes.usuarios import usuarios_bp
from routes.empresas import empresas_bp

app.register_blueprint(vistas_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(productos_bp, url_prefix='/api/productos')
app.register_blueprint(entradas_bp, url_prefix='/api/entradas')
app.register_blueprint(salidas_bp, url_prefix='/api/salidas')
app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')
app.register_blueprint(empresas_bp, url_prefix='/api/empresas')

with app.app_context():
    db.create_all()
    from models import Usuario
    if Usuario.query.filter_by(rol='god').count() == 0:
        god = Usuario(nombre='God', email=os.getenv('GOD_EMAIL', 'god@stockflow.com'), rol='god')
        god.set_password(os.getenv('GOD_PASSWORD', 'god123'))
        db.session.add(god)
        db.session.commit()
        print('✅ Usuario God creado')

if __name__ == '__main__':
    app.run(debug=True)
