from flask import Blueprint, render_template

vistas_bp = Blueprint('vistas', __name__)

@vistas_bp.route('/')
def index():
    return render_template('index.html')
