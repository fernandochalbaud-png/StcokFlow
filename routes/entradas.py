from flask import Blueprint, request, jsonify
from database import db
from models import Entrada, Producto

entradas_bp = Blueprint('entradas', __name__)

@entradas_bp.route('/', methods=['GET'])
def listar():
    entradas = Entrada.query.order_by(Entrada.creado_en.desc()).all()
    return jsonify([e.to_dict() for e in entradas])

@entradas_bp.route('/', methods=['POST'])
def crear():
    data = request.json
    if not data.get('factura') or not data.get('proveedor') or not data.get('producto_id') or not data.get('cantidad'):
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    prod = Producto.query.get_or_404(data['producto_id'])
    cantidad = int(data['cantidad'])
    if cantidad <= 0:
        return jsonify({'error': 'La cantidad debe ser mayor a 0'}), 400

    prod.stock += cantidad

    e = Entrada(
        fecha=data.get('fecha', ''),
        factura=data['factura'],
        proveedor=data['proveedor'],
        producto_id=prod.id,
        cantidad=cantidad,
        obs=data.get('obs', '')
    )
    db.session.add(e)
    db.session.commit()
    return jsonify({'entrada': e.to_dict(), 'producto': prod.to_dict()}), 201
