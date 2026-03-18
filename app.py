from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from database import db
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Base de datos:
# - En Railway usa DATABASE_URL (PostgreSQL)
# - En local usa SQLite
database_url = os.getenv('DATABASE_URL', 'sqlite:///stockflow.db')

# Railway usa 'postgres://' pero SQLAlchemy necesita 'postgresql://'
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

# Mail config
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

app.register_blueprint(vistas_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(productos_bp, url_prefix='/api/productos')
app.register_blueprint(entradas_bp, url_prefix='/api/entradas')
app.register_blueprint(salidas_bp, url_prefix='/api/salidas')
app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')

with app.app_context():
    db.create_all()
    from models import Usuario, Producto
    if Usuario.query.count() == 0:
        admin = Usuario(nombre='Administrador', email='admin@stockflow.com', rol='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('✅ Usuario admin creado: admin@stockflow.com / admin123')
    if Producto.query.count() == 0:
        from seed import cargar_datos_iniciales
        cargar_datos_iniciales()

if __name__ == '__main__':
    app.run(debug=True)
