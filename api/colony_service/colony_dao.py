from psycopg2 import Error
from psycopg2.extras import RealDictCursor
import psycopg2
import logging

from pydantic import BaseModel
from typing import Optional

logging.basicConfig(level=logging.DEBUG)

DB_URL = "postgresql://root@0.0.0.0:26257/cybero_mis?sslmode=disable"

def get_db_connection():
    conn = psycopg2.connect(DB_URL)
    return conn
    

def create_colony(colony):
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            INSERT INTO colony (id, name, inhabitants)
            VALUES (%s, %s, %s)
        '''

        cur = conn.cursor()
        cur.execute(query, (colony["id"],
                            colony["name"],
                            colony["inhabitants"]))
        cur.close()
        conn.close()
    except Error as e:
        return f"Error: {e}"


def get_colony(colony_id):
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            SELECT * FROM colony WHERE id = %s
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (colony_id,))
        colony = cur.fetchone()
        cur.close()
        conn.close()
        return colony
    except Error as e:
        print(f"Error: {e}")
        return {}


def list_colonies():
    conn = get_db_connection()
    try:
        query = '''
            SELECT * FROM colony
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        colonies = cur.fetchall()
        cur.close()
        conn.close()
        return colonies
    except Error as e:
        print(f"Error: {e}")
        return []


def update_colony(colony_id, colony):
    logging.info(f"Updating colony: {colony} (id: {colony_id}")
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            UPDATE colony
            SET name = %s,
                inhabitants = %s
            WHERE id = %s
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (colony["name"],
                            colony["inhabitants"],
                            colony_id))
        # Query the updated record
        fetch_query = '''
            SELECT * FROM colony WHERE id = %s
        '''
        cur.execute(fetch_query, (colony_id,))
        updated_colony = cur.fetchone()
        logging.info(f"colony fetched: {updated_colony}")
        cur.close()
        conn.close()
        return {"updated_colony": updated_colony}
    except Error as e:
        logging.error(f"updating colony {e}")
        # return {"error": message}




def delete_colony(colony_id):
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            DELETE FROM colony WHERE id = %s
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (colony_id,))
        deleted_colony = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return deleted_colony
    except Error as e:
        print(f"Error: {e}")
        return {}


def delete_colonies():
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            TRUNCATE colony
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        cur.close()
        conn.close()
    except Error as e:
        return f"Error: {e}"