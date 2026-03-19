from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from database import db
from models import Entrada, Producto

entradas_bp = Blueprint('entradas', __name__)

@entradas_bp.route('/', methods=['GET'])
@login_required
def listar():
    empresa_id = current_user.empresa_id if current_user.rol != 'god' else request.args.get('empresa_id', type=int)
    q = Entrada.query
    if empresa_id:
        q = q.filter_by(empresa_id=empresa_id)
    return jsonify([e.to_dict() for e in q.order_by(Entrada.creado_en.desc()).all()])

@entradas_bp.route('/', methods=['POST'])
@login_required
def crear():
    data = request.json
    if not data.get('factura') or not data.get('proveedor') or not data.get('producto_id') or not data.get('cantidad'):
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    prod = Producto.query.get_or_404(data['producto_id'])

    # Verificar que el producto pertenece a la empresa del usuario
    if current_user.rol != 'god' and prod.empresa_id != current_user.empresa_id:
        return jsonify({'error': 'Sin permiso sobre este producto'}), 403

    cantidad = int(data['cantidad'])
    if cantidad <= 0:
        return jsonify({'error': 'La cantidad debe ser mayor a 0'}), 400

    prod.stock += cantidad
    e = Entrada(
        fecha=data.get('fecha', ''), factura=data['factura'],
        proveedor=data['proveedor'], producto_id=prod.id,
        cantidad=cantidad, obs=data.get('obs', ''),
        empresa_id=current_user.empresa_id
    )
    db.session.add(e)
    db.session.commit()
    return jsonify({'entrada': e.to_dict(), 'producto': prod.to_dict()}), 201
