from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.models import Socio

bp = Blueprint('estados', __name__, url_prefix='/estados')

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        busqueda = request.form.get('busqueda', '').strip()
        if busqueda:
            # Buscar por cedula o nro de socio
            socio = Socio.query.filter((Socio.cedula == busqueda) | (Socio.nro_socio == busqueda)).first()
            if socio:
                flash(f'Estado financiero cargado para: {socio.apellidos_nombres}', 'success')
                return redirect(url_for('socios.estado', id=socio.id))
            else:
                flash('No se encontró ningún socio con la cédula o Nro. de socio proporcioando.', 'danger')
        else:
            flash('Por favor ingresa un dato para la búsqueda.', 'warning')
            
    return render_template('estados/index.html')
