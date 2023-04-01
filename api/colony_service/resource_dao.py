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
    

def create_resource(resource):
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            INSERT INTO colony_resource (id, colony_id, name, air, lodging, food, water)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''

        cur = conn.cursor()
        cur.execute(query, (resource["id"],
                            resource["colony_id"],
                            resource["name"],
                            resource["air"],
                            resource["lodging"],
                            resource["food"],
                            resource["water"]))
        cur.close()
        conn.close()
    except Error as e:
        return f"Error: {e}"


def get_resource(resource_id):
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            SELECT * FROM colony_resource WHERE id = %s
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (resource_id,))
        resource = cur.fetchone()
        cur.close()
        conn.close()
        return resource
    except Error as e:
        print(f"Error: {e}")
        return {}


def list_resources():
    conn = get_db_connection()
    try:
        query = '''
            SELECT * FROM colony_resource
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        resources = cur.fetchall()
        cur.close()
        conn.close()
        return resources
    except Error as e:
        print(f"Error: {e}")
        return []


def update_resource(resource_id, resource):
    logging.info(f"Updating resource: {resource} (id: {resource_id}")
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            UPDATE colony_resource
            SET colony_id = %s,
                name = %s,
                air = %s,
                lodging = %s,
                food = %s,
                water = %s
            WHERE id = %s
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        # logging.info(f"Executed query: {cur.mogrify(query, (resource_id,)).decode('utf-8')}") 
        logging.info(f"Cursor description: {cur.description}") 
        logging.info(f"Row count: {cur.rowcount}")
        cur.execute(query, (resource["colony_id"],
                            resource["name"],
                            resource["air"],
                            resource["lodging"],
                            resource["food"],
                            resource["water"],
                            resource_id))
        # Query the updated record
        fetch_query = '''
            SELECT * FROM passenger WHERE id = %s
        '''
        cur.execute(fetch_query, (resource_id,))
        updated_resource = cur.fetchone()
        logging.info(f"resource fetched: {updated_resource}")
        cur.close()
        conn.close()
        return updated_resource
    except Error as e:
        message = f"updating resource {e}"
        return {"error": message}


def delete_resource(resource_id):
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            DELETE FROM colony_resource WHERE id = %s
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (resource_id,))
        deleted_resource = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return deleted_resource
    except Error as e:
        print(f"Error: {e}")
        return {}
    

def delete_resources():
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            TRUNCATE colony_resource
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        cur.close()
        conn.close()
    except Error as e:
        return f"Error: {e}"