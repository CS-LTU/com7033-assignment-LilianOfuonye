import sqlite3

"""Database initialisation to store user authentication details"""

def init_db():
    with sqlite3.connect("london_health.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,      
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role_name TEXT UNIQUE NOT NULL
            )
        ''')
        
        default_roles = ['admin', 'doctor']
        for role in default_roles:
            cursor.execute('''
                INSERT OR IGNORE INTO roles (role_name) VALUES (?)
            ''', (role,))
            
        conn.commit()


# Helper function
def get_user_by_email(email):
    with sqlite3.connect("london_health.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return cursor.fetchone()