import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)
db_url = os.getenv('DATABASE_URL')
print("Connecting to:", db_url)

try:
    conn = psycopg2.connect(db_url)
    conn.autocommit = True
    cur = conn.cursor()
    
    # Check if table exists
    cur.execute("SELECT to_regclass('usuarios');")
    table_exists = cur.fetchone()[0]
    print("Table usuarios exists:", table_exists)
    
    if table_exists:
        cur.execute("ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS password_venc TIMESTAMPTZ;")
        print("Column password_venc added successfully.")
        
        # Verify columns
        cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'usuarios';")
        cols = cur.fetchall()
        print("Current columns of usuarios table:")
        for col in cols:
            print(f" - {col[0]}: {col[1]}")
    else:
        print("Table usuarios does not exist!")
        
    cur.close()
    conn.close()
except Exception as e:
    print("Error:", e)
