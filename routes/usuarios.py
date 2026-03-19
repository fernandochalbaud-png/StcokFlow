from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from database import db
from models import Usuario

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/', methods=['GET'])
@login_required
def listar():
    if current_user.rol == 'god':
        usuarios = Usuario.query.filter(Usuario.rol != 'god').all()
    elif current_user.rol == 'admin':
        usuarios = Usuario.query.filter_by(empresa_id=current_user.empresa_id).all()
    else:
        return jsonify({'error': 'Sin permiso'}), 403
    return jsonify([u.to_dict() for u in usuarios])

@usuarios_bp.route('/', methods=['POST'])
@login_required
def crear():
    if current_user.rol not in ['admin', 'god']:
        return jsonify({'error': 'Sin permiso'}), 403
    data = request.json
    if not data.get('email') or not data.get('password') or not data.get('nombre'):
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El email ya existe'}), 400

    # Admin solo puede crear operadores y admins de su empresa
    # God puede crear cualquier usuario
    rol = data.get('rol', 'operador')
    if current_user.rol == 'admin' and rol == 'god':
        return jsonify({'error': 'Sin permiso para crear usuario god'}), 403

    empresa_id = data.get('empresa_id') or current_user.empresa_id

    u = Usuario(nombre=data['nombre'], email=data['email'], rol=rol, empresa_id=empresa_id)
    u.set_password(data['password'])
    db.session.add(u)
    db.session.commit()
    return jsonify(u.to_dict()), 201

@usuarios_bp.route('/<int:id>', methods=['PUT'])
@login_required
def actualizar(id):
    if current_user.rol not in ['admin', 'god']:
        return jsonify({'error': 'Sin permiso'}), 403
    u = Usuario.query.get_or_404(id)
    data = request.json
    u.nombre = data.get('nombre', u.nombre)
    u.rol    = data.get('rol', u.rol)
    u.activo = data.get('activo', u.activo)
    if data.get('password'):
        u.set_password(data['password'])
    db.session.commit()
    return jsonify(u.to_dict())

@usuarios_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def eliminar(id):
    if current_user.rol not in ['admin', 'god']:
        return jsonify({'error': 'Sin permiso'}), 403
    if id == current_user.id:
        return jsonify({'error': 'No puedes eliminarte a ti mismo'}), 400
    u = Usuario.query.get_or_404(id)
    db.session.delete(u)
    db.session.commit()
    return jsonify({'ok': True})
