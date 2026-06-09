import os
os.environ["DATABASE_URL"] = "postgresql://postgres:Zelaya1103@localhost:5432/mivoto"

from app import create_app
from app.extensions import db, bcrypt
import random

app = create_app()

with app.app_context():
    # Drop and recreate schema
    from sqlalchemy import text
    db.session.execute(text("DROP SCHEMA public CASCADE;"))
    db.session.execute(text("CREATE SCHEMA public;"))
    db.session.commit()
    
    # Execute schema.sql
    with open("schema.sql", "r", encoding="utf-8") as f:
        sql = f.read()
    
    # Remove BEGIN and END from the postgres dump to execute directly
    sql = sql.replace("BEGIN;", "").replace("END;", "")
    
    raw_conn = db.engine.raw_connection()
    try:
        with raw_conn.cursor() as cursor:
            cursor.execute(sql)
        raw_conn.commit()
    finally:
        raw_conn.close()
    
    print("Schema created successfully.")

    from app.models import Usuario, Rol, Socio

    # Insert Roles
    rol_admin = Rol(nombre='Administrador', descripcion='Acceso total al sistema')
    rol_socio = Rol(nombre='Socio', descripcion='Socio asambleista')
    db.session.add(rol_admin)
    db.session.add(rol_socio)
    db.session.commit()

    # Insert Admin user
    admin = Usuario(
        username='admin',
        email='admin@mivoto.com',
        password_hash=bcrypt.generate_password_hash('admin').decode('utf-8'),
        nombre_completo='Administrador del Sistema',
        activo=True,
        rol_id=rol_admin.id
    )
    db.session.add(admin)
    db.session.commit()

    # Create 20 members
    nombres = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Elena", "Pedro", "Laura", "Jose", "Carmen",
               "Diego", "Sofia", "Miguel", "Lucia", "Javier", "Paula", "Fernando", "Marta", "Ricardo", "Rosa"]
    apellidos = ["Gonzalez", "Rodriguez", "Gomez", "Fernandez", "Lopez", "Diaz", "Martinez", "Perez", "Garcia", "Sanchez"]

    for i in range(1, 21):
        s = Socio(
            cedula=f"{random.randint(1000000, 9999999)}",
            nro_socio=f"S-{i:04d}",
            nombres=nombres[(i-1) % len(nombres)],
            apellidos=f"{random.choice(apellidos)} {random.choice(apellidos)}",
            situacion="activo",
            sexo="M" if i % 2 == 0 else "F"
        )
        db.session.add(s)

    db.session.commit()
    print("Database seeded with admin user and 20 fictional members.")
