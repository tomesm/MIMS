from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from db import get_db_connection
from models import PutPassengerRequest
import logging

def create_passenger(passenger: dict):
    logging.basicConfig(level=logging.INFO)
    logging.info("Loging request: " + str(passenger))
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            INSERT INTO passenger (id, flight_id, first_name, last_name, age, criminal_record, health_status, colony, skills, specialization, ticket_number, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cur = conn.cursor()
        cur.execute(query, (passenger["id"],
                            passenger["flight_id"],
                            passenger["first_name"],
                            passenger["last_name"],
                            passenger["age"],
                            passenger["criminal_record"],
                            passenger["health_status"],
                            passenger["colony"],
                            passenger["skills"],
                            passenger["specialization"],
                            passenger["ticket_number"],
                            passenger["status"]))
        cur.close()
        conn.close()
    except Error as e:
        return f"Error: {e}"




def create_passengers(passengers):
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        values = ",".join(["(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" for _ in passengers])
        values = values % tuple(value for record in passengers for value in record.values())

        query = f'''
            INSERT INTO passengers (flight_id, first_name, last_name, age, criminal_record, health_status, colony, skills, specialization, ticket_number, status)
            VALUES {values}
        '''
        # Insert data into the table
        with conn.cursor() as cursor:
            cursor.execute(query)
            cursor.close()

        conn.close()
    except Error as e:
        return f"Error: {e}"


def get_passenger(passenger_id):
    logging.info(f"get_passenger: passenger_id = {passenger_id}, type(passenger_id) = {type(passenger_id)}")
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            SELECT * FROM passenger WHERE id = CAST(%s AS BIGINT)
        '''
        cur = conn.cursor()
        logging.info(f"Executed query: {cur.mogrify(query, (passenger_id,)).decode('utf-8')}") 
        logging.info(f"Cursor description: {cur.description}") 
        logging.info(f"Row count: {cur.rowcount}")
        # cur.execute(query, (passenger_id,))
        cur.execute('SELECT * FROM passenger WHERE id=%s', (passenger_id,))
        passenger = cur.fetchone()
        logging.info(f"Passenger fetched: {passenger}")
        cur.close()
        conn.close()
        return passenger
    except Error as e:
        print(f"Error: {e}")
        return {}

def list_passengers():
    conn = get_db_connection()
    try:
        query = '''
            SELECT * FROM passenger
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        passengers = cur.fetchall()
        cur.close()
        conn.close()
        return passengers
    except Error as e:
        print(f"Error: {e}")
        return []

def list_flagged_passengers():
    conn = get_db_connection()
    try:
        query = '''
            SELECT * FROM passenger WHERE criminal_record IS NOT NULL OR health_status IS NOT NULL
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        passengers = cur.fetchall()
        cur.close()
        conn.close()
        return passengers
    except Error as e:
        print(f"Error: {e}")
        return []

def update_passenger(passenger_id, passenger: dict):
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            UPDATE passenger
            SET flight_id = %s,
                first_name = %s,
                last_name = %s,
                age = %s,
                criminal_record = %s,
                health_status = %s,
                colony = %s,
                skills = %s,
                specialization = %s,
                ticket_number = %s,
                status = %s
            WHERE id = %s
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (passenger["flight_id"],
                            passenger["first_name"],
                            passenger["last_name"],
                            passenger["age"],
                            passenger["criminal_record"],
                            passenger["health_status"],
                            passenger["colony"],
                            passenger["skills"],
                            passenger["specialization"],
                            passenger["ticket_number"],
                            passenger["status"],
                            passenger_id))
        # Query the updated record
        fetch_query = '''
            SELECT * FROM passenger WHERE id = %s
        '''
        cur.execute(fetch_query, (passenger_id,))
        updated_passenger = cur.fetchone()
        cur.close()
        conn.close()
        return updated_passenger
    except Error as e:
        message = f"updating passenger {e}"
        return {"error": message}

def delete_passenger(passenger_id: str):
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            DELETE FROM passenger WHERE id = %s
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (passenger_id,))
        deleted_passenger = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return deleted_passenger
    except Error as e:
        print(f"Error: {e}")
        return {}

def delete_passengers():
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            TRUNCATE passenger
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        cur.close()
        conn.close()
    except Error as e:
        return f"Error: {e}"

