from psycopg2 import Error
from psycopg2.extras import RealDictCursor
import psycopg2

from pydantic import BaseModel
from typing import Optional


DB_URL = "postgresql://root@0.0.0.0:26257/cybero_mis?sslmode=disable"

def get_db_connection():
    conn = psycopg2.connect(DB_URL)
    return conn
    

def create_rule(rule):
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            INSERT INTO immigration_rule (id, colony_id, name, air, lodging, food, water)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''

        cur = conn.cursor()
        cur.execute(query, (rule["id"],
                            rule["colony_id"],
                            rule["name"],
                            rule["air"],
                            rule["lodging"],
                            rule["food"],
                            rule["water"]))
        cur.close()
        conn.close()
    except Error as e:
        return f"Error: {e}"


def get_rule(rule_id):
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            SELECT * FROM immigration_rule WHERE id = %s
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (rule_id,))
        rule = cur.fetchone()
        cur.close()
        conn.close()
        return rule
    except Error as e:
        print(f"Error: {e}")
        return {}


def list_rules():
    conn = get_db_connection()
    try:
        query = '''
            SELECT * FROM immigration_rule
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        rules = cur.fetchall()
        cur.close()
        conn.close()
        return rules
    except Error as e:
        print(f"Error: {e}")
        return []


def update_rule(rule_id, rule):
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            UPDATE immigration_rule
            SET colony_id = %s,
                name = %s,
                air = %s,
                lodging = %s,
                food = %s,
                water = %s
            WHERE id = %s
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (rule.colony_id,
                            rule.name,
                            rule.air,
                            rule.lodging,
                            rule.food,
                            rule.water,
                            rule_id))
        updated_rule = cur.fetchone()
        cur.close()
        conn.close()
        return updated_rule
    except Error as e:
        message = f"updating rule {e}"
        return {"error": message}


def delete_rule(rule_id):
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            DELETE FROM immigration_rule WHERE id = %s
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (rule_id,))
        deleted_rule = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return deleted_rule
    except Error as e:
        print(f"Error: {e}")
        return {}