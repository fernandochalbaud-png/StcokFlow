from flask import Blueprint, render_template, request
from flask_login import login_required

vistas_bp = Blueprint('vistas', __name__)

@vistas_bp.route('/')
@login_required
def index():
    return render_template('index.html')

@vistas_bp.route('/login')
def login_page():
    return render_template('login.html')

@vistas_bp.route('/reset/<token>')
def reset_page(token):
    return render_template('reset.html', token=token)
