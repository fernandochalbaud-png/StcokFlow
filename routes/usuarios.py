from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from database import db
from models import Usuario

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/', methods=['GET'])
@login_required
def listar():
    if current_user.rol == 'god':
        empresa_id = request.args.get('empresa_id', type=int)
        if empresa_id:
            usuarios = Usuario.query.filter_by(empresa_id=empresa_id).all()
        else:
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

    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'JSON inválido o vacío'}), 400
    if not data.get('email') or not data.get('password') or not data.get('nombre'):
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    if len(data['password']) < 6:
        return jsonify({'error': 'Contraseña muy corta, mínimo 6 caracteres'}), 400

    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El email ya existe'}), 400

    rol = data.get('rol', 'operador')
    if current_user.rol == 'admin' and rol == 'god':
        return jsonify({'error': 'Sin permiso para crear usuario god'}), 403

    empresa_id = data.get('empresa_id') or current_user.empresa_id
    if current_user.rol == 'admin' and data.get('empresa_id') and data.get('empresa_id') != current_user.empresa_id:
        return jsonify({'error': 'Un admin no puede crear usuarios para otra empresa'}), 403

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
    # Verificar que el usuario pertenece a la empresa del admin
    if current_user.rol != 'god' and u.empresa_id != current_user.empresa_id:
        return jsonify({'error': 'Sin permiso sobre este usuario'}), 403

    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'JSON inválido o vacío'}), 400

    if current_user.rol == 'admin' and data.get('rol') == 'god':
        return jsonify({'error': 'Sin permiso para asignar rol god'}), 403

    u.nombre = data.get('nombre', u.nombre)
    u.rol    = data.get('rol', u.rol)
    u.activo = data.get('activo', u.activo)

    if current_user.rol != 'god' and data.get('empresa_id') and data.get('empresa_id') != current_user.empresa_id:
        return jsonify({'error': 'No puedes cambiar la empresa de este usuario'}), 403

    if 'empresa_id' in data:
        u.empresa_id = data.get('empresa_id', u.empresa_id)

    if data.get('password'):
        if len(data['password']) < 6:
            return jsonify({'error': 'Contraseña muy corta, mínimo 6 caracteres'}), 400
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
    # Verificar que el usuario pertenece a la empresa del admin
    if current_user.rol != 'god' and u.empresa_id != current_user.empresa_id:
        return jsonify({'error': 'Sin permiso sobre este usuario'}), 403
    db.session.delete(u)
    db.session.commit()
    return jsonify({'ok': True})

@usuarios_bp.route('/<int:id>/reset-password', methods=['PUT'])
@login_required
def reset_password(id):
    if current_user.rol != 'god':
        return jsonify({'error': 'Sin permiso'}), 403
    u = Usuario.query.get_or_404(id)
    data = request.json
    if not data.get('password'):
        return jsonify({'error': 'Contraseña requerida'}), 400
    if len(data['password']) < 6:
        return jsonify({'error': 'Mínimo 6 caracteres'}), 400
    u.set_password(data['password'])
    db.session.commit()
    return jsonify({'ok': True})
