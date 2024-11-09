import bcrypt
from typing import Any, Dict, List, Optional
import re

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def format_chat_history(history: List[Any]) -> str:
    """Format chat history for better readability."""
    formatted_history = "\n"
    for row in history:
        formatted_history += f"Time: {row[2]}\n"
        formatted_history += f"User: {row[0]}\n"
        formatted_history += f"Probot: {row[1]}\n"
        formatted_history += "-" * 40 + "\n\n"
    return formatted_history


def validate_username(username: str) -> bool:
    """Validate username format."""
    return bool(re.match(r'^[a-zA-Z0-9_]{3,30}$', username))

def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength."""
    error_status = ""
    check = True
    if len(password) < 8:
        check = False
        error_status += "* Length too short (Atleast 8 characters required).\n"
    if any(char.isdigit()for char in password) == False:
        check = False
        error_status += "* Atleast 1 digit requiredt\n"
    if any(char.isalpha() for char in password) == False:
        check = False
        error_status += "* Atleast 1 alphabet required\n"
    if any(char in "!@#$%^&*()-_+=" for char in password) == False:
        check = False
        error_status += "* Atleast 1 special character (!@#$%^&*()-_+=) required\n"

    return (check, error_status)


def format_user_response(user: Dict[str, Any]) -> Dict[str, Any]:
    """Format user data for API response."""
    return {
        "id": user["id"],
        "username": user["username"]
    }

def sanitize_input(input_string: str) -> str:
    """Sanitize input to prevent SQL injection or other attacks."""
    return input_string.replace("'", "''")  # Simple SQL injection prevention

def log_error(message: str) -> None:
    """Log error messages for debugging."""
    # In production, you might use logging frameworks instead
    print(f"ERROR: {message}")
