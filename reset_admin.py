from app import create_app
from app.extensions import db, bcrypt
from app.models import Usuario

app = create_app()
with app.app_context():
    u = Usuario.query.filter_by(username='admin').first()
    if u:
        u.password_hash = bcrypt.generate_password_hash('admin').decode('utf-8')
        db.session.commit()
        print("Admin user password updated to 'admin'.")
    else:
        print("Admin user not found, creating...")
        u = Usuario(username='admin', password_hash=bcrypt.generate_password_hash('admin').decode('utf-8'), rol='Administrador', activo=True)
        db.session.add(u)
        db.session.commit()
        print("Admin user created with password 'admin'.")
