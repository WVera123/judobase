import mysql.connector

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'Hamster2005!',
    'database': 'JudoBase'
}

# Get a new connection
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Execute SELECT queries and return results
def fetch_all(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# Execute INSERT/UPDATE/DELETE queries
def execute_query(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    conn.commit()
    cursor.close()
    conn.close()
