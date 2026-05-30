from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Asamblea, PadronAsamblea, Credencial

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@login_required
def index():
    asamblea_activa = Asamblea.query.filter(Asamblea.estado.in_(['programada', 'en_curso'])).order_by(Asamblea.fecha.asc()).first()
    stats = None
    if asamblea_activa:
        padron = PadronAsamblea.query.filter_by(asamblea_id=asamblea_activa.id).all()
        total_habilitados = sum(1 for p in padron if p.situacion == 'habilitado')
        credenciales = Credencial.query.join(PadronAsamblea).filter(PadronAsamblea.asamblea_id == asamblea_activa.id).count()
        
        no_acreditados = max(0, total_habilitados - credenciales)
        
        stats = {
            'asamblea': asamblea_activa.fecha.strftime('%d/%m/%Y'),
            'total_habilitados': total_habilitados,
            'acreditados': credenciales,
            'no_acreditados': no_acreditados
        }
        
    return render_template('dashboard/index.html', stats=stats)
