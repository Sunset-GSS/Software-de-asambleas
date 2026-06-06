import os
from sqlalchemy import inspect
from sqlalchemy.schema import CreateColumn
from app import create_app
from app.extensions import db

# Force environment reload
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass

app = create_app()

with app.app_context():
    engine = db.engine
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    print("Checking database schema against SQLAlchemy models...")
    print(f"Connection URL: {engine.url}")
    print(f"Existing tables in DB: {existing_tables}")
    
    # Track actions
    created_tables = []
    added_columns = []
    
    # Iterate through all models defined in SQLAlchemy metadata
    for table_name, table in db.metadata.tables.items():
        if table_name not in existing_tables:
            print(f"\n[NEW TABLE] Creating table '{table_name}'...")
            table.create(engine)
            created_tables.append(table_name)
            print(f"Table '{table_name}' created successfully.")
        else:
            # Table exists, inspect its columns
            db_cols = {col['name'].lower(): col for col in inspector.get_columns(table_name)}
            
            # Compare with model columns
            for col_name, model_col in table.columns.items():
                if col_name.lower() not in db_cols:
                    print(f"\n[MISSING COLUMN] Column '{col_name}' is missing in table '{table_name}'.")
                    
                    # Compile SQLAlchemy column to PostgreSQL DDL
                    col_ddl = CreateColumn(model_col).compile(dialect=engine.dialect)
                    alter_query = f"ALTER TABLE {table_name} ADD COLUMN {col_ddl}"
                    
                    print(f"Executing: {alter_query}")
                    try:
                        with engine.begin() as conn:
                            conn.execute(db.text(alter_query))
                        added_columns.append(f"{table_name}.{col_name}")
                        print(f"Column '{col_name}' added to table '{table_name}' successfully.")
                    except Exception as err:
                        print(f"Error executing statement: {err}")
                else:
                    # Column exists, we can log it (optional)
                    pass

    print("\n--- SCHEMA VERIFICATION COMPLETE ---")
    print(f"Created tables: {created_tables}")
    print(f"Added columns: {added_columns}")
