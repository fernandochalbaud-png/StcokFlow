from flask import Blueprint, request, jsonify, redirect, url_for, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from models import Usuario
from database import db
import secrets

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return redirect(url_for('vistas.login_page'))
    data = request.json
    user = Usuario.query.filter_by(email=data.get('email')).first()
    if not user or not user.check_password(data.get('password', '')):
        return jsonify({'error': 'Email o contraseña incorrectos'}), 401
    if not user.activo:
        return jsonify({'error': 'Usuario desactivado'}), 403
    login_user(user)
    return jsonify({'ok': True, 'usuario': user.to_dict()})

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'ok': True})

@auth_bp.route('/me', methods=['GET'])
@login_required
def me():
    return jsonify(current_user.to_dict())

@auth_bp.route('/recuperar', methods=['POST'])
def recuperar():
    data = request.json
    user = Usuario.query.filter_by(email=data.get('email')).first()
    if not user:
        # Por seguridad respondemos igual aunque no exista
        return jsonify({'ok': True})

    token = secrets.token_urlsafe(32)
    user.reset_token = token
    db.session.commit()

    mail = Mail(current_app)
    link = url_for('auth.reset_password', token=token, _external=True)

    msg = Message(
        subject='Recuperar contraseña — StockFlow',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email]
    )
    msg.body = f'''Hola {user.nombre},

Recibimos una solicitud para restablecer tu contraseña en StockFlow.

Haz clic en el siguiente link para crear una nueva contraseña:
{link}

Si no solicitaste esto, ignora este correo.

— StockFlow
'''
    mail.send(msg)
    return jsonify({'ok': True})

@auth_bp.route('/reset/<token>', methods=['GET'])
def reset_password(token):
    return redirect(url_for('vistas.reset_page', token=token))

@auth_bp.route('/reset', methods=['POST'])
def reset_password_post():
    data = request.json
    user = Usuario.query.filter_by(reset_token=data.get('token')).first()
    if not user:
        return jsonify({'error': 'Token inválido o expirado'}), 400
    user.set_password(data.get('password'))
    user.reset_token = None
    db.session.commit()
    return jsonify({'ok': True})
