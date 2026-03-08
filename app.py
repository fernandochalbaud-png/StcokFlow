from flask import Flask
from database import db

app = Flask(__name__)

# Configuracion de la base de datos (archivo local SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stockflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'stockflow-secret-2024'

# Inicializar base de datos
db.init_app(app)

# Importar rutas
from routes.productos import productos_bp
from routes.entradas import entradas_bp
from routes.salidas import salidas_bp
from routes.vistas import vistas_bp

app.register_blueprint(vistas_bp)
app.register_blueprint(productos_bp, url_prefix='/api/productos')
app.register_blueprint(entradas_bp, url_prefix='/api/entradas')
app.register_blueprint(salidas_bp, url_prefix='/api/salidas')

# Crear tablas si no existen
with app.app_context():
    db.create_all()
    from models import Producto
    # Cargar productos iniciales si la base esta vacia
    if Producto.query.count() == 0:
        from seed import cargar_datos_iniciales
        cargar_datos_iniciales()

if __name__ == '__main__':
    app.run(debug=True)
