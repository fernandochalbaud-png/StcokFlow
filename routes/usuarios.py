from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from database import db
from models import Usuario

usuarios_bp = Blueprint('usuarios', __name__)

def solo_admin():
    if current_user.rol != 'admin':
        return jsonify({'error': 'Acceso denegado'}), 403

@usuarios_bp.route('/', methods=['GET'])
@login_required
def listar():
    if current_user.rol != 'admin':
        return jsonify({'error': 'Acceso denegado'}), 403
    return jsonify([u.to_dict() for u in Usuario.query.all()])

@usuarios_bp.route('/', methods=['POST'])
@login_required
def crear():
    if current_user.rol != 'admin':
        return jsonify({'error': 'Acceso denegado'}), 403
    data = request.json
    if not data.get('email') or not data.get('password') or not data.get('nombre'):
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El email ya existe'}), 400
    u = Usuario(nombre=data['nombre'], email=data['email'], rol=data.get('rol', 'operador'))
    u.set_password(data['password'])
    db.session.add(u)
    db.session.commit()
    return jsonify(u.to_dict()), 201

@usuarios_bp.route('/<int:id>', methods=['PUT'])
@login_required
def actualizar(id):
    if current_user.rol != 'admin':
        return jsonify({'error': 'Acceso denegado'}), 403
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
    if current_user.rol != 'admin':
        return jsonify({'error': 'Acceso denegado'}), 403
    if id == current_user.id:
        return jsonify({'error': 'No puedes eliminarte a ti mismo'}), 400
    u = Usuario.query.get_or_404(id)
    db.session.delete(u)
    db.session.commit()
    return jsonify({'ok': True})
