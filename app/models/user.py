
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
