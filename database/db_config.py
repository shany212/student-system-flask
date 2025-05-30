import pymysql
from pymysql.cursors import DictCursor

# Database connection configuration
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'wuxian120',
    'database': 'student_management',
    'charset': 'utf8mb4',
    'cursorclass': DictCursor
}

# Function to get database connection
def get_db_connection():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except pymysql.MySQLError as e:
        print(f"Database connection error: {e}")
        return None

# Function to execute a query with parameters
def execute_query(query, params=None, fetch=True, commit=True):
    conn = get_db_connection()
    result = None
    
    if not conn:
        return None
        
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if fetch:
                result = cursor.fetchall()
            if commit:
                conn.commit()
    except Exception as e:
        print(f"Query execution error: {e}")
        if commit:
            conn.rollback()
    finally:
        conn.close()
        
    return result 