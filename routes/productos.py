from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from database import db
from models import Producto

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/', methods=['GET'])
@login_required
def listar():
    productos = Producto.query.order_by(Producto.categoria, Producto.nombre).all()
    return jsonify([p.to_dict() for p in productos])

@productos_bp.route('/', methods=['POST'])
@login_required
def crear():
    if current_user.rol != 'admin':
        return jsonify({'error': 'Solo el admin puede agregar productos'}), 403
    data = request.json
    if not data.get('codigo') or not data.get('nombre'):
        return jsonify({'error': 'Código y nombre son requeridos'}), 400
    if Producto.query.filter_by(codigo=data['codigo']).first():
        return jsonify({'error': 'El código ya existe'}), 400
    p = Producto(
        codigo=data['codigo'], nombre=data['nombre'],
        categoria=data.get('categoria', 'General'),
        stock=int(data.get('stock', 0)), minimo=int(data.get('minimo', 0))
    )
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201

@productos_bp.route('/<int:id>', methods=['PUT'])
@login_required
def actualizar(id):
    if current_user.rol != 'admin':
        return jsonify({'error': 'Solo el admin puede editar productos'}), 403
    p = Producto.query.get_or_404(id)
    data = request.json
    p.nombre    = data.get('nombre', p.nombre)
    p.categoria = data.get('categoria', p.categoria)
    p.minimo    = int(data.get('minimo', p.minimo))
    db.session.commit()
    return jsonify(p.to_dict())

@productos_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def eliminar(id):
    if current_user.rol != 'admin':
        return jsonify({'error': 'Solo el admin puede eliminar productos'}), 403
    p = Producto.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({'ok': True})
