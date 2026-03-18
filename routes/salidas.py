from flask import Blueprint, request, jsonify
from flask_login import login_required
from database import db
from models import Salida, Producto

salidas_bp = Blueprint('salidas', __name__)

@salidas_bp.route('/', methods=['GET'])
@login_required
def listar():
    salidas = Salida.query.order_by(Salida.creado_en.desc()).all()
    return jsonify([s.to_dict() for s in salidas])

@salidas_bp.route('/', methods=['POST'])
@login_required
def crear():
    data = request.json
    if not data.get('referencia') or not data.get('producto_id') or not data.get('cantidad'):
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    prod = Producto.query.get_or_404(data['producto_id'])
    cantidad = int(data['cantidad'])
    if cantidad <= 0:
        return jsonify({'error': 'La cantidad debe ser mayor a 0'}), 400
    if prod.stock < cantidad:
        return jsonify({'error': f'Stock insuficiente. Disponible: {prod.stock}'}), 400
    prod.stock -= cantidad
    s = Salida(
        fecha=data.get('fecha', ''), tipo=data.get('tipo', 'factura'),
        referencia=data['referencia'], producto_id=prod.id,
        cantidad=cantidad, destino=data.get('destino', '')
    )
    db.session.add(s)
    db.session.commit()
    return jsonify({'salida': s.to_dict(), 'producto': prod.to_dict()}), 201
