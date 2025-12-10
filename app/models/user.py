import sqlite3
from datetime import datetime

DB_NAME = "london_health.db"


class User:
    """
    User class 
    """

    def __init__(self, id, first_name, last_name, email, password_hash, role, created_at):
        """Initialize a user object with their details"""
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at

    @staticmethod
    def create_user(first_name, last_name, email, password_hash, role):
        """
        Add a new user to the database
        Raises ValueError if email already exists
        """
        try:
            existing_user = User.get_by_email(email)
            if existing_user:
                raise ValueError("A user with this email already exists")

            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (first_name, last_name, email, password_hash, role) VALUES (?, ?, ?, ?, ?)",
                    (first_name, last_name, email, password_hash, role)
                )
                conn.commit()
                return cursor.lastrowid

        except sqlite3.IntegrityError:
            raise ValueError("A user with this email already exists")

    @staticmethod
    def get_all_users():
        """
        Get all users from database
        Returns list of user dictionaries
        """
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()

        users = []
        for row in rows:
            user = {
                'id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'email': row[3],
                'password_hash': row[4],
                'role': row[5],
                'created_at': row[6]
            }
            users.append(user)

        return users

    @staticmethod
    def get_paginated_users(page=1, per_page=10):
        """
        Get paginated users from database
        Returns tuple of (users list, total count)
        """
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            
            # Get total count
            cursor.execute("SELECT COUNT(*) FROM users")
            total = cursor.fetchone()[0]
            
            # Calculate offset
            offset = (page - 1) * per_page
            
            # Get paginated results
            cursor.execute(
                "SELECT * FROM users LIMIT ? OFFSET ?",
                (per_page, offset)
            )
            rows = cursor.fetchall()

        users = []
        for row in rows:
            user = {
                'id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'email': row[3],
                'password_hash': row[4],
                'role': row[5],
                'created_at': row[6]
            }
            users.append(user)

        return users, total

    @staticmethod
    def get_by_id(user_id):
        """
        Get a specific user by their id
        Returns user dictionary or None if not found
        """
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()

        if row:
            user = {
                'id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'email': row[3],
                'password_hash': row[4],
                'role': row[5],
                'created_at': row[6]
            }
            return user
        
        return None

    @staticmethod
    def get_by_email(email):
        """
        Find a user by their email
        Returns user dictionary or None if not found
        """
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()

        if row:
            user = {
                'id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'email': row[3],
                'password_hash': row[4],
                'role': row[5],
                'created_at': row[6]
            }
            return user
        
        return None

    @staticmethod
    def update(user_id, first_name, last_name, role):
        """
        Update a user's information
        Returns True if successful, False if user not found
        """
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET first_name = ?, last_name = ?, role = ? WHERE id = ?",
                    (first_name, last_name, role, user_id)
                )
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            raise ValueError(f"Failed to update user: {e}")

    @staticmethod
    def update_password(user_id, password_hash):
        """
        Update a user's password
        Returns True if successful, False if user not found
        """
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET password_hash = ? WHERE id = ?",
                    (password_hash, user_id)
                )
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            raise ValueError(f"Failed to update password: {e}")

    @staticmethod
    def delete_user(user_id):
        """
        Delete a user from database
        """
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0
