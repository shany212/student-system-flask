from database.db_config import execute_query
import hashlib

def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    """Authenticate a user by username and password."""
    hashed_password = hash_password(password)
    query = "SELECT id, username, is_admin FROM users WHERE username = %s AND password = %s"
    users = execute_query(query, (username, hashed_password))
    
    if users and len(users) > 0:
        # Update last login time
        update_query = "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = %s"
        execute_query(update_query, (users[0]['id'],), fetch=False)
        return users[0]
    return None

def is_username_taken(username):
    """Check if a username is already taken."""
    query = "SELECT id FROM users WHERE username = %s"
    users = execute_query(query, (username,))
    return users and len(users) > 0

def register_user(username, password, is_admin=False):
    """Register a new user."""
    if is_username_taken(username):
        return False, "Username already taken"
    
    hashed_password = hash_password(password)
    query = "INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)"
    execute_query(query, (username, hashed_password, is_admin), fetch=False)
    return True, "User registered successfully"

def is_admin(username):
    """Check if a user is an admin."""
    query = "SELECT is_admin FROM users WHERE username = %s"
    users = execute_query(query, (username,))
    return users and len(users) > 0 and users[0]['is_admin'] 