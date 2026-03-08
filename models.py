from database import db
from datetime import datetime

class Producto(db.Model):
    __tablename__ = 'productos'
    id       = db.Column(db.Integer, primary_key=True)
    codigo   = db.Column(db.String(20), unique=True, nullable=False)
    nombre   = db.Column(db.String(100), nullable=False)
    categoria= db.Column(db.String(50), default='General')
    stock    = db.Column(db.Integer, default=0)
    minimo   = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'categoria': self.categoria,
            'stock': self.stock,
            'minimo': self.minimo
        }

class Entrada(db.Model):
    __tablename__ = 'entradas'
    id          = db.Column(db.Integer, primary_key=True)
    fecha       = db.Column(db.String(20), nullable=False)
    factura     = db.Column(db.String(50), nullable=False)
    proveedor   = db.Column(db.String(100), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad    = db.Column(db.Integer, nullable=False)
    obs         = db.Column(db.String(200), default='')
    creado_en   = db.Column(db.DateTime, default=datetime.utcnow)

    producto = db.relationship('Producto', backref='entradas')

    def to_dict(self):
        return {
            'id': self.id,
            'fecha': self.fecha,
            'factura': self.factura,
            'proveedor': self.proveedor,
            'producto': self.producto.nombre,
            'codigo': self.producto.codigo,
            'cantidad': self.cantidad,
            'obs': self.obs
        }

class Salida(db.Model):
    __tablename__ = 'salidas'
    id          = db.Column(db.Integer, primary_key=True)
    fecha       = db.Column(db.String(20), nullable=False)
    tipo        = db.Column(db.String(20), nullable=False)   # factura | ot | cambio
    referencia  = db.Column(db.String(50), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad    = db.Column(db.Integer, nullable=False)
    destino     = db.Column(db.String(100), default='')
    creado_en   = db.Column(db.DateTime, default=datetime.utcnow)

    producto = db.relationship('Producto', backref='salidas')

    def to_dict(self):
        labels = {'factura': 'Factura', 'ot': 'Orden de Trabajo', 'cambio': 'Cambio'}
        return {
            'id': self.id,
            'fecha': self.fecha,
            'tipo': self.tipo,
            'tipoLabel': labels.get(self.tipo, self.tipo),
            'referencia': self.referencia,
            'producto': self.producto.nombre,
            'codigo': self.producto.codigo,
            'cantidad': self.cantidad,
            'destino': self.destino
        }
