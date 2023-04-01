import psycopg2

DB_URL = "postgresql://root@0.0.0.0:26257/cybero_mis?sslmode=disable"

def get_db_connection():
    conn = psycopg2.connect(DB_URL)
    return conn

