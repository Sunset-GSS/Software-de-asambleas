from app import create_app
from app.extensions import db, bcrypt
from app.models import Usuario

app = create_app()
with app.app_context():
    usuarios = Usuario.query.all()
    for u in usuarios:
        h = u.password_hash
        # Check if the hash is a valid bcrypt hash (typically starts with $2b$ or $2a$)
        if not (h.startswith('$2b$') or h.startswith('$2a$')):
            print(f"Updating password hash for user '{u.username}'...")
            # Set default password: 'admin123' for 'admin', or the username itself for others
            default_pwd = 'admin123' if u.username == 'admin' else u.username
            u.password_hash = bcrypt.generate_password_hash(default_pwd).decode('utf-8')
            print(f"User '{u.username}' password set to '{default_pwd}'")
    db.session.commit()
    print("Passwords updated successfully.")
