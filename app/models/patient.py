from app.config.mongo_db import get_collection
from bson.objectid import ObjectId


class Patient:
    """
    Patient class - handles all patient database operations
    CREATE, READ, UPDATE, DELETE patients
    """

    def __init__(self, patient_id, id, gender, age, hypertension, heart_disease, 
                 ever_married, work_type, residence_type, avg_glucose_level, 
                 bmi, smoking_status, stroke):
        """Initialize a patient object with their details"""
        self.patient_id = patient_id
        self.id = id
        self.gender = gender
        self.age = age
        self.hypertension = hypertension
        self.heart_disease = heart_disease
        self.ever_married = ever_married
        self.work_type = work_type
        self.residence_type = residence_type
        self.avg_glucose_level = avg_glucose_level
        self.bmi = bmi
        self.smoking_status = smoking_status
        self.stroke = stroke

    @staticmethod
    def create_patient(id, gender, age, hypertension, heart_disease, ever_married, 
                      work_type, residence_type, avg_glucose_level, bmi, 
                      smoking_status, stroke):
        """
        Add a new patient to the database
        Raises ValueError if patient id already exists
        """
        existing_patient = Patient.get_by_patient_id(id)
        if existing_patient:
            raise ValueError("A patient with this ID already exists")

        # Insert new patient into MongoDB
        collection = get_collection()
        patient_data = {
            'id': id,
            'gender': gender,
            'age': age,
            'hypertension': hypertension,
            'heart_disease': heart_disease,
            'ever_married': ever_married,
            'work_type': work_type,
            'Residence_type': residence_type,
            'avg_glucose_level': avg_glucose_level,
            'bmi': bmi,
            'smoking_status': smoking_status,
            'stroke': stroke
        }
        result = collection.insert_one(patient_data)
        return str(result.inserted_id)

    @staticmethod
    def get_all_patients():
        """
        Get all patients from database
        Returns list of patient dictionaries
        """
        collection = get_collection()
        patients = []
        
        for doc in collection.find():
            patient = {
                'patient_id': doc.get('id'), 
                'id': str(doc['_id']) ,            
                'gender': doc.get('gender'),
                'age': doc.get('age'),
                'hypertension': doc.get('hypertension'),
                'heart_disease': doc.get('heart_disease'),
                'ever_married': doc.get('ever_married'),
                'work_type': doc.get('work_type'),
                'Residence_type': doc.get('Residence_type'),
                'avg_glucose_level': doc.get('avg_glucose_level'),
                'bmi': doc.get('bmi'),
                'smoking_status': doc.get('smoking_status'),
                'stroke': doc.get('stroke')
            }
            patients.append(patient)

        return patients

    @staticmethod
    def get_paginated_patients(page=1, per_page=10):
            """
            Get paginated patients from database
            Returns tuple of (patients list, total count)
            """
            collection = get_collection()
            
            # Get total count
            total = collection.count_documents({})
            
            # Calculate skip value
            skip = (page - 1) * per_page
            
            # Get paginated results, sorted by newest first
            patients = []
            cursor = (
                collection.find()
                .sort("_id", -1)      # sort by Mongo's _id
                .skip(skip)
                .limit(per_page)
            )

            for doc in cursor:
                patient = {
                    'patient_id': doc.get('id'),
                    'gender': doc.get('gender'),
                    'age': doc.get('age'),
                    'hypertension': doc.get('hypertension'),
                    'heart_disease': doc.get('heart_disease'),
                    'ever_married': doc.get('ever_married'),
                    'work_type': doc.get('work_type'),
                    'Residence_type': doc.get('Residence_type'),
                    'avg_glucose_level': doc.get('avg_glucose_level'),
                    'bmi': doc.get('bmi'),
                    'smoking_status': doc.get('smoking_status'),
                    'stroke': doc.get('stroke')
                }
                patients.append(patient)

            return patients, total

    @staticmethod
    def get_by_id(patient_id):
        """
        Get a specific patient by their MongoDB _id
        Returns patient dictionary or None if not found
        """
        collection = get_collection()
        
        try:
            doc = collection.find_one({'id': patient_id})
        except:
            return None

        if doc:
            patient = {
                'id': str(doc['_id']) ,
                'patient_id':doc.get('id'),
                'id': doc.get('id'),
                'gender': doc.get('gender'),
                'age': doc.get('age'),
                'hypertension': doc.get('hypertension'),
                'heart_disease': doc.get('heart_disease'),
                'ever_married': doc.get('ever_married'),
                'work_type': doc.get('work_type'),
                'Residence_type': doc.get('Residence_type'),
                'avg_glucose_level': doc.get('avg_glucose_level'),
                'bmi': doc.get('bmi'),
                'smoking_status': doc.get('smoking_status'),
                'stroke': doc.get('stroke')
            }
            return patient
        
        return None

    @staticmethod
    def get_by_patient_id(id):
        """
        Find a patient by their patient id field
        Returns patient dictionary or None if not found
        """
        collection = get_collection()
        doc = collection.find_one({'id': id})

        if doc:
            patient = {
                'id': str(doc['_id']),
                'patient_id': doc.get('id'),
                'gender': doc.get('gender'),
                'age': doc.get('age'),
                'hypertension': doc.get('hypertension'),
                'heart_disease': doc.get('heart_disease'),
                'ever_married': doc.get('ever_married'),
                'work_type': doc.get('work_type'),
                'Residence_type': doc.get('Residence_type'),
                'avg_glucose_level': doc.get('avg_glucose_level'),
                'bmi': doc.get('bmi'),
                'smoking_status': doc.get('smoking_status'),
                'stroke': doc.get('stroke')
            }
            return patient
        
        return None

    @staticmethod
    def update(patient_id, gender, age, hypertension, heart_disease, ever_married,
               work_type, residence_type, avg_glucose_level, bmi, smoking_status, stroke):
        """
        Update a patient's information
        Returns True if successful, False if patient not found
        """
        try:
            collection = get_collection()
            result = collection.update_one(
                {'id': patient_id},
                {'$set': {
                    'gender': gender,
                    'age': age,
                    'hypertension': hypertension,
                    'heart_disease': heart_disease,
                    'ever_married': ever_married,
                    'work_type': work_type,
                    'Residence_type': residence_type,
                    'avg_glucose_level': avg_glucose_level,
                    'bmi': bmi,
                    'smoking_status': smoking_status,
                    'stroke': stroke
                }}
            )
            return result.modified_count > 0
        except Exception as e:
            raise ValueError(f"Failed to update patient: {e}")

    @staticmethod
    def delete_patient(patient_id):
        """
        Delete a patient from database
        """
        collection = get_collection()
        result = collection.delete_one({'id': patient_id})
        return result.deleted_count > 0
