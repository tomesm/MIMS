from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from db import get_db_connection
import logging

def create_passenger(passenger: dict):
    # logging.basicConfig(level=logging.INFO)
    # logging.info("Loging request: " + str(passenger))
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
    # logging.info(f"get_passenger: passenger_id = {passenger_id}, type(passenger_id) = {type(passenger_id)}")
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            SELECT * FROM passenger WHERE id = CAST(%s AS BIGINT)
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        # logging.info(f"Executed query: {cur.mogrify(query, (passenger_id,)).decode('utf-8')}") 
        # logging.info(f"Cursor description: {cur.description}") 
        # logging.info(f"Row count: {cur.rowcount}")
        # cur.execute(query, (passenger_id,))
        cur.execute('SELECT * FROM passenger WHERE id=%s', (passenger_id,))
        passenger = cur.fetchone()
        # logging.info(f"Passenger fetched: {passenger}")
        cur.close()
        conn.close()
        return passenger
    except Error as e:
        print(f"Error: {e}")
        return {}
    

# List all passengers with given "status" attribute. Status is a string param for thios function
def list_by_status(status):
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        query = '''
            SELECT * FROM passenger WHERE status = %s
        '''
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, (status,))
        passengers = cur.fetchall()
        cur.close()
        conn.close()
        return passengers
    except Error as e:
        print(f"Error: {e}")
        return []
    

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

def update_passenger(passenger_id, passenger):
    conn = get_db_connection()
    conn.set_session(autocommit=True)
    try:
        # Prepare the update query with non-None values
        update_fields = []
        update_values = []
        for field, value in passenger.items():
            if value is not None:
                update_fields.append(f"{field} = %s")
                update_values.append(value)

        query = f'''
            UPDATE passenger
            SET {', '.join(update_fields)}
            WHERE id = %s
        '''
        update_values.append(passenger_id)

        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, tuple(update_values))

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

