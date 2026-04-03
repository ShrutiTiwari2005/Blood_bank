from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from app import login_manager
from app.repositories.user_repo import UserRepository

bcrypt = Bcrypt()

class User(UserMixin):
    """SaaS User Object for Flask-Login Registry"""
    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']
        self.email = user_data['email']
        self.role = user_data['role']

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login Callback to retrieve a user from the database."""
    user_data = UserRepository.get_by_id(user_id)
    if user_data:
        return User(user_data)
    return None

class AuthService:
    """SaaS Authentication & Registration Engine v4.0"""

    @staticmethod
    def register_user(username, email, password, role='viewer'):
        """Hashes the password and creates a new user record."""
        # Verification: Check if user exists
        if UserRepository.get_by_username(username):
            return {"status": "error", "message": "Username already exists."}
        
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            UserRepository.create(username, email, hashed_pw, role)
            return {"status": "success", "message": "User registered successfully."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def login_user(username, password):
        """Standardized Login Verification Interface."""
        user_data = UserRepository.get_by_username(username)
        if user_data:
            # Verify bcrypt hash
            if bcrypt.check_password_hash(user_data['password_hash'], password):
                user = User(user_data)
                # Success Logic: Update audit trail timestamp
                UserRepository.update_last_login(user.id)
                return {"status": "success", "user": user}
        
        return {"status": "error", "message": "Invalid username or password."}
