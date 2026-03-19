from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from database import db
from models import Empresa, Usuario, EmpresaLog
import re

empresas_bp = Blueprint('empresas', __name__)


def _require_god_role():
    if current_user.rol != 'god':
        return jsonify({'error': 'Sin permiso'}), 403
    return None


def _valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, email))

@empresas_bp.route('/', methods=['GET'])
@login_required
def listar():
    permiso = _require_god_role()
    if permiso:
        return permiso
    return jsonify([e.to_dict() for e in Empresa.query.all()])

@empresas_bp.route('/', methods=['POST'])
@login_required
def crear():
    permiso = _require_god_role()
    if permiso:
        return permiso

    data = request.json or {}
    if not data.get('nombre') or not data.get('email'):
        return jsonify({'error': 'Nombre y email son requeridos'}), 400

    if not _valid_email(data['email']):
        return jsonify({'error': 'Email de empresa inválido'}), 400

    if Empresa.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El email ya existe'}), 400

    empresa = Empresa(nombre=data['nombre'], email=data['email'])
    db.session.add(empresa)

    # Crear usuario admin de la empresa (opcional)
    if data.get('admin_nombre') and data.get('admin_password'):
        admin_email = data.get('admin_email') or f"admin@{data['email'].split('@')[-1]}"
        if not _valid_email(admin_email):
            return jsonify({'error': 'Email de admin inválido'}), 400

        if Usuario.query.filter_by(email=admin_email).first():
            return jsonify({'error': 'El email de admin ya existe'}), 400

        admin = Usuario(
            nombre=data['admin_nombre'],
            email=admin_email,
            rol='admin',
            empresa_id=empresa.id
        )
        admin.set_password(data['admin_password'])
        db.session.add(admin)

    # Registrar log
    log = EmpresaLog(
        empresa_id=empresa.id,
        evento='creada',
        notas=f"Empresa creada por {current_user.nombre}"
    )
    db.session.add(log)

    try:
        db.session.flush()
        db.session.commit()
        return jsonify(empresa.to_dict()), 201
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': 'Error en la creación de la empresa', 'detalle': str(exc)}), 500

@empresas_bp.route('/<int:id>', methods=['PUT'])
@login_required
def actualizar(id):
    permiso = _require_god_role()
    if permiso:
        return permiso

    e = Empresa.query.get_or_404(id)
    data = request.json or {}
    e.nombre = data.get('nombre', e.nombre)

    if 'activo' in data:
        nuevo_estado = data['activo']
        e.activo = nuevo_estado
        evento = 'activada' if nuevo_estado else 'desactivada'
        log = EmpresaLog(
            empresa_id=e.id,
            evento=evento,
            notas=f"Empresa {evento} por {current_user.nombre}"
        )
        db.session.add(log)

    try:
        db.session.commit()
        return jsonify(e.to_dict())
    except Exception as exc:
        db.session.rollback()
        return jsonify({'error': 'Error al actualizar empresa', 'detalle': str(exc)}), 500

@empresas_bp.route('/<int:id>/logs', methods=['GET'])
@login_required
def ver_logs(id):
    permiso = _require_god_role()
    if permiso:
        return permiso
    e = Empresa.query.get_or_404(id)
    logs = EmpresaLog.query.filter_by(empresa_id=id).order_by(EmpresaLog.fecha.desc()).all()
    return jsonify([l.to_dict() for l in logs])