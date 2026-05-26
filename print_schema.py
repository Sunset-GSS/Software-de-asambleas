import sys
from sqlalchemy.schema import CreateTable
from app import create_app
from app.extensions import db

app = create_app()
with app.app_context():
    # Establecer la base de datos temporalmente a postgres en memoria para generar el dialecto correcto
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/dummy'
    
    for name, table in db.metadata.tables.items():
        create_stmt = CreateTable(table).compile(db.engine)
        print(f"--- Table: {name}")
        print(f"{create_stmt};\n")
