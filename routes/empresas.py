from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from database import db
from models import Empresa, Usuario

empresas_bp = Blueprint('empresas', __name__)

@empresas_bp.route('/', methods=['GET'])
@login_required
def listar():
    if current_user.rol != 'god':
        return jsonify({'error': 'Sin permiso'}), 403
    return jsonify([e.to_dict() for e in Empresa.query.all()])

@empresas_bp.route('/', methods=['POST'])
@login_required
def crear():
    if current_user.rol != 'god':
        return jsonify({'error': 'Sin permiso'}), 403
    data = request.json
    if not data.get('nombre') or not data.get('email'):
        return jsonify({'error': 'Nombre y email son requeridos'}), 400
    if Empresa.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El email ya existe'}), 400

    empresa = Empresa(nombre=data['nombre'], email=data['email'])
    db.session.add(empresa)
    db.session.flush()  # get empresa.id before commit

    # Create admin user for this company
    if data.get('admin_email') and data.get('admin_password'):
        admin = Usuario(
            nombre=data.get('admin_nombre', 'Administrador'),
            email=data['admin_email'],
            rol='admin',
            empresa_id=empresa.id
        )
        admin.set_password(data['admin_password'])
        db.session.add(admin)

    db.session.commit()
    return jsonify(empresa.to_dict()), 201

@empresas_bp.route('/<int:id>', methods=['PUT'])
@login_required
def actualizar(id):
    if current_user.rol != 'god':
        return jsonify({'error': 'Sin permiso'}), 403
    e = Empresa.query.get_or_404(id)
    data = request.json
    e.nombre = data.get('nombre', e.nombre)
    e.activo = data.get('activo', e.activo)
    db.session.commit()
    return jsonify(e.to_dict())
