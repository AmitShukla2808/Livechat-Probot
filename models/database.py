import psycopg2
from psycopg2 import sql
from utils.helpers import hash_password, log_error, sanitize_input
import bcrypt
from typing import Optional  # Add this line

# # Database connection settings
DB_NAME = 'chatbot'
DB_USER = 'postgres'
DB_PASSWORD = 'amit2808'

def init_db(Db_NAME, Db_USER, Db_PASSWORD):
    DB_NAME = Db_NAME
    DB_USER = Db_USER
    DB_PASSWORD = Db_PASSWORD

    """Initialize the database and create tables if they do not exist."""
    try:
        with psycopg2.connect(host = 'localhost', database=DB_NAME, user=DB_USER, password=DB_PASSWORD) as conn:
            with conn.cursor() as cursor:
                # Create users table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                );
                """)
                # Create chat_logs table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_logs (
                    id SERIAL PRIMARY KEY,
                    user_id INT REFERENCES users(id) ON DELETE CASCADE,
                    user_message TEXT NOT NULL,
                    bot_response TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """)
                conn.commit()
    except Exception as e:
        log_error(f"Database initialization error: {e}")

def get_db_connection():
    """Get a new database connection."""
    return psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)

def save_chat_log(user_id: int, user_message: str, bot_response: str):
    """Save a chat log entry to the database."""
    sanitized_message = sanitize_input(user_message)
    sanitized_response = sanitize_input(bot_response)

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO chat_logs (user_id, user_message, bot_response) VALUES (%s, %s, %s)",
                    (user_id, sanitized_message, sanitized_response)
                )
                conn.commit()
    except Exception as e:
        log_error(f"Error saving chat log: {e}")

def fetch_chat_history(user_id: int, limit: Optional[int] = None):
    """Fetch chat history for a specific user with an optional limit."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    SELECT user_message, bot_response, timestamp 
                    FROM chat_logs 
                    WHERE user_id = %s 
                    ORDER BY timestamp DESC
                """
                if limit:
                    query += f" LIMIT {limit}"
                
                cursor.execute(query, (user_id,))
                return cursor.fetchall()
    except Exception as e:
        log_error(f"Error fetching chat history: {e}")
        return []

    
def clear_chat_history(user_id: int):
    """Clear chat history for a given user."""
    with psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql.SQL("DELETE FROM chat_logs WHERE user_id = %s;"), (user_id,))
            conn.commit()

def create_user(username: str, password: str):
    """Create a new user in the database."""
    hashed_password = hash_password(password)
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id;",
                    (username, hashed_password)
                )
                user_id = cursor.fetchone()[0]
                conn.commit()
                return user_id
    except Exception as e:
        log_error(f"Error creating user: {e}")
        return None
    
def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def get_user(username: str):
    """Fetch a user by username."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, username, password FROM users WHERE username = %s;",
                    (username,)
                )
                return cursor.fetchone()  # Returns a tuple (id, username, hashed_password)
    except Exception as e:
        log_error(f"Error fetching user: {e}")
        return None
    

def delete_user_by_id(user_id: int):
    """Delete a user from the database by user ID."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM users WHERE id = %s;",
                    (user_id,)
                )
                conn.commit()
    except Exception as e:
        log_error(f"Error deleting user: {e}")

