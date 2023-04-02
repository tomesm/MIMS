from psycopg2 import Error
from psycopg2.extras import RealDictCursor
import psycopg2

import logging

logging.basicConfig(level=logging.INFO)

DB_URL = "postgresql://root@0.0.0.0:26257/cybero_mis?sslmode=disable"

def get_db_connection():
    conn = psycopg2.connect(DB_URL)
    return conn
    

def create_rule(rule):
    logging.info("Creating rule: %s", rule)

    conn = get_db_connection()
    conn.set_session(autocommit=True)

    try:
        query = '''
            INSERT INTO immigration_rule (id, colony_id, rule_type, description)
            VALUES (%s, %s, %s, %s)
        '''

        cur = conn.cursor()
        cur.execute(query, (rule["id"],
                            rule["colony_id"],
                            rule["rule_type"],
                            rule["description"]))
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


def list_rules(colony_id):
    conn = get_db_connection()
    try:
        query = '''
            SELECT * FROM immigration_rule WHERE colony_id = %s
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (colony_id,))
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
                rule_type = %s,
                description = %s,
            WHERE id = %s
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (rule["colony_id"],
                            rule["rule_type"],
                            rule["description"],
                            rule_id))
        updated_rule = cur.fetchone()
        cur.close()
        conn.close()
        return updated_rule
    except Error as e:
        message = f"updating rule {e}"
        return {"error": message}


def delete_rule(colony_id):
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            DELETE FROM immigration_rule WHERE colony_id = %s
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (colony_id,))
        deleted_rule = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return deleted_rule
    except Error as e:
        print(f"Error: {e}")
        return {}
    

def delete_rules(colony_id):
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            DELETE FROM immigration_rule WHERE colony_id = %s
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (colony_id,))
        cur.close()
        conn.close()
    except Error as e:
        return f"Error: {e}"