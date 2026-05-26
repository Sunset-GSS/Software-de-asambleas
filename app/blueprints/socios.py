from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.models import Socio, Estado
from app.extensions import db

bp = Blueprint('socios', __name__, url_prefix='/socios')

@bp.route('/')
@login_required
def index():
    # Búsqueda sencilla por cédula o apellido
    q = request.args.get('q', '')
    if q:
        socios = Socio.query.filter(
            (Socio.cedula.ilike(f'%{q}%')) | 
            (Socio.apellidos.ilike(f'%{q}%')) |
            (Socio.nombres.ilike(f'%{q}%'))
        ).limit(50).all()
    else:
        socios = Socio.query.limit(50).all()
        
    return render_template('socios/index.html', socios=socios, q=q)

@bp.route('/<int:id>/estado')
@login_required
def estado(id):
    socio = Socio.query.get_or_404(id)
    # Obtener el estado de morosidad
    estado_socio = Estado.query.filter_by(socio_id=socio.id).first()
    if not estado_socio:
        # Si no existe registro de estado, asumimos al día por defecto
        estado_socio = Estado(
            socio_id=socio.id,
            mora_cc='al_dia',
            mora_sol='al_dia',
            mora_ape='al_dia',
            mora_credito='al_dia',
            mora_cabal='al_dia',
            mora_visa='al_dia'
        )
        db.session.add(estado_socio)
        db.session.commit()
        
    # Verificar si está habilitado (todas las moras deben estar 'al_dia')
    moras = {
        'Caja de Ahorro / CC': estado_socio.mora_cc,
        'Solidaridad': estado_socio.mora_sol,
        'Aporte': estado_socio.mora_ape,
        'Créditos': estado_socio.mora_credito,
        'Tarjeta Cabal': estado_socio.mora_cabal,
        'Tarjeta Visa': estado_socio.mora_visa
    }
    
    moras_activas = {prod: est for prod, est in moras.items() if est == 'moroso'}
    habilitado = len(moras_activas) == 0
    
    return render_template('socios/estado.html', socio=socio, estado_socio=estado_socio, moras_activas=moras_activas, habilitado=habilitado)

