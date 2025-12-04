import sqlite3

# Database file name
DB_NAME = "london_health.db"


class Patient:
    """
    Patient class - handles all patient database operations
    CREATE, READ, UPDATE, DELETE patients
    """

    def __init__(self, patient_id, first_name, last_name, date_of_birth, gender, email):
        """Initialize a patient object with their details"""
        self.patient_id = patient_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.email = email


    @staticmethod
    def create_patient(first_name, last_name, date_of_birth, gender, email):
        """
        Add a new patient to the database
        Raises ValueError if email already exists
        """
        try:
            existing_patient = Patient.get_by_email(email)
            if existing_patient:
                raise ValueError("A patient with this email already exists")

            # Connect to database and insert new patient
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO patients (first_name, last_name, date_of_birth, gender, email) VALUES (?, ?, ?, ?, ?)",
                    (first_name, last_name, date_of_birth, gender, email)
                )
                conn.commit()

        except sqlite3.IntegrityError:
            # Database caught duplicate email
            raise ValueError("A patient with this email already exists")


    @staticmethod
    def get_all_patients():
        """
        Get all patients from database
        Returns list of patient dictionaries
        """
        # Connect to database and get all patients
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients")
            rows = cursor.fetchall()

        # This convert rows to list of dictionaries
        patients = []
        for row in rows:
            patient = {
                'patient_id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'date_of_birth': row[3],
                'gender': row[4],
                'email': row[5]
            }
            patients.append(patient)

        return patients


    @staticmethod
    def get_by_id(patient_id):
        """
        Get a specific patient by their ID
        Returns patient dictionary or None if not found
        """
        # Connect to database and find patient by ID
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
            row = cursor.fetchone()

        # Convert to dictionary if found
        if row:
            patient = {
                'patient_id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'date_of_birth': row[3],
                'gender': row[4],
                'email': row[5]
            }
            return patient
        
        return None


    @staticmethod
    def get_by_email(email):
        """
        Find a patient by their email
        Returns patient dictionary or None if not found
        """
        # Connect to database and find patient by email
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients WHERE email = ?", (email,))
            row = cursor.fetchone()

        # Convert to dictionary if found
        if row:
            patient = {
                'patient_id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'date_of_birth': row[3],
                'gender': row[4],
                'email': row[5]
            }
            return patient
        
        return None


    @staticmethod
    def update(patient_id, first_name, last_name, date_of_birth, gender):
        """
        Update a patient's information
        Returns True if successful, False if patient not found
        """
        try:
            # Connect to database and update patient information
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE patients SET first_name = ?, last_name = ?, date_of_birth = ?, gender = ? WHERE id = ?",
                    (first_name, last_name, date_of_birth, gender, patient_id)
                )
                conn.commit()
                return True
        except Exception as e:
            raise ValueError(f"Failed to update patient: {e}")


    @staticmethod
    def delete_patient(patient_id):
        """
        Delete a patient from database
        """
        # Connect to database and delete patient
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
            conn.commit()
            return True
