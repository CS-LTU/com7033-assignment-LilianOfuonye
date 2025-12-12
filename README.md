# London Hospital Data Portal

A secure Flask-based web application that allows healthcare staff record, manage, and review patient data used in patient's assessment. Designed to prioritise protection of data, smooth user experience, and strict privacy controls, the system provides separate access levels for doctors and administrators within a hospital setting. 
## Features

- Secure User Authentication
- Patient Data Management 
- Admin Dashboard for CRUD functionalities
- Dashboard for Doctors to view and manage patient's records
- Secure Session Handling & Input Validation
- Role-Based Access Control with two roles (Administrator, Doctor)
- Zero Trust Architecture and OWASP-aligned security practices

## System Architecture

#### The application follows a three-layered architecture aligned with SSDLC principles:

| Layer                  | Description                                            | Security Controls                                                                                                                        |
| ---------------------- | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **Presentation Layer** | Flask HTML templates (Jinja2), forms, and Tailwind UI | Input validation, CSRF protection                                                                                                        |
| **Application Layer**  | Flask backend (business logic, RBAC, authentication)   | RBAC, session management, exception handling                                                                                             |
| **Data Layer**         | SQLite (Auth), MongoDB (Patients Record)               | Encryption-at-rest (password hashes), least privilege DB access, integrity checks, injection (SQL/NoSQL injection, XSS) prevention      |

## Tech Stack

| Category           | Technology Used                                                                     |
| ------------------ | ----------------------------------------------------------------------------------- |
| **Framework**      | Flask                                                                               |
| **Frontend**       | HTML5, Tailwind (CDN), Jinja2 Templates                                             |
| **Databases**      | SQLite (auth), MongoDB (patients record)                                            |
| **Authentication** | Flask session, CSRF (Flask-WTF), password hashing (Werkzeug)                        |
| **Security**       | CSRF, XSS prevention (Jinja2 autoescape), input validation, RBAC, env-based secrets |
| **Environment**    | Python Virtual env (`venv`)                                                         |
| **Dev Tools**      | Unittest (built-in)                                              |

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/CS-LTU/com7033-assignment-LilianOfuonye.git

# Go to project directory
cd com7033-assignment-LilianOfuonye
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv

# on bash
source venv/Scripts/activate

# Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create an `.env` file in the project root and set:

```bash
SECRET_KEY = "yoursecretkey"
MONGO_URL = yourmongoURL
DB_NAME=HealthcareDB
PATIENT_COLLECTION=StrokeData
```

## Run the Application
```bash
python run.py
```

The url can be accessed here http://localhost:5000/

## Run all Tests

Using unittest:

```bash
python -m unittest discover -s app/tests -p "*.py" -v
```

## API & Routes Reference

### Authentication Routes (`/`)

| Method | Route | Access | Description | Required Fields |
|--------|-------|--------|-------------|-----------------|
| GET | `/` | Public | Landing page | - |
| GET/POST | `/login` | Public | User login | email, password |
| GET/POST | `/register` | Public | User registration | first_name, last_name, email, password, confirm_password, role |
| GET | `/logout` | Authenticated | Terminate user session | - |

### Dashboard Routes (`/dashboard`)

| Method | Route | Access | Description | Required Fields |
|--------|-------|--------|-------------|-----------------|
| GET | `/dashboard` | Doctor/Admin | View paginated patient list | page (optional), per_page (optional) |
| GET/POST | `/register_patient` | Admin | Create new patient record | id, gender, age, hypertension, heart_disease, ever_married, work_type, residence_type, avg_glucose_level, bmi, smoking_status, stroke |
| GET | `/dashboard/patients/<patient_id>` | Doctor/Admin | View patient details | - |
| POST | `/dashboard/patients/<patient_id>/update` | Doctor/Admin | Update patient record | gender, age, hypertension, heart_disease, ever_married, work_type, residence_type, avg_glucose_level, bmi, smoking_status, stroke |
| POST | `/dashboard/patients/<patient_id>/delete` | Admin | Delete patient record | - |
| GET | `/user_dashboard` | Admin | View user management dashboard | page (optional), per_page (optional) |
| POST | `/register_user` | Admin | Create new user account | first_name, last_name, email, password, role |
| POST | `/dashboard/users/<user_id>/update` | Admin | Update user information | first_name, last_name, role |
| POST | `/dashboard/users/<user_id>/delete` | Admin | Delete user account | - |

### Error Handlers

| Code | Route | Access | Description |
|------|-------|--------|-------------|
| 404 | Any invalid route | All | Custom 404 error page with role-based navigation |

### Input Validation Rules

| Field | Validation Rule |
|-------|-----------------|
| Email | Regex: `^[\w\.-]+@[\w\.-]+\.\w+$` |
| Password | Min 8 chars, uppercase, lowercase, digit, special char: `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,}$` |
| Age | Integer: 0-120 |
| BMI | Float: 10-100 |
| Glucose Level | Float: 0-500 |

## Design Rationale

### Architecture Decisions

#### 1. Three-Layered Architecture
**Decision:** Implement Presentation, Application, and Data layers as separate concerns.

**Rationale:**
- **Separation of Concerns:** Clear boundaries between UI, business logic, and data storage improve maintainability
- **Security:** Each layer can implement its own security controls without cross-contamination
- **Testability:** Layers can be tested independently (unit tests for application layer, integration tests across layers)

#### 2. Dual Database Strategy (SQLite + MongoDB)
**Decision:** Use SQLite for user authentication and MongoDB for patient records.

**Rationale:**
- **SQLite for Auth:**
  - Relational structure suits user-role relationships
  - ACID compliance critical for authentication data
  - Local file-based storage reduces external dependencies for auth
  - Simpler backup and recovery for critical user data

- **MongoDB for Patients:**
  - Flexible schema to accommodate evolving medical data fields
  - Document model maps naturally to patient records (the embedded health indicators)
  - Better performance for large-scale patient data retrieval
  - Future-proof for unstructured data (medical images, PDFs)

#### 3. Flask Framework Selection

**Rationale:**
- **Lightweight:** Minimal overhead for focused healthcare application
- **Flexibility:** Freedom to choose security libraries (Flask-WTF for CSRF) 
- **Learning Curve:** Simpler for understanding security implementation at lower level
- **Jinja2 Integration:** Built-in templating with automatic XSS protection

#### 4. Role-Based Access Control (RBAC)
**Decision:** Implement decorator-based RBAC with two roles (Admin, Doctor).

**Rationale:**
- **Least Privilege Principle:** Doctors can only view/update; Admins have full CRUD but cant delete their own account
- **Decorator Pattern:** Reusable `@admin_required` and `@doctor_required` decorators reduce code duplication
- **Template-Level Enforcement:** Conditional rendering (`{% if session.role == 'admin' %}`) prevents UI confusion

#### 5. Session-Based Authentication
**Decision:** Use Flask's encrypted session cookies.

**Rationale:**
- **Simplicity:** No need for token management, refresh logic, or token storage
- **Security:** Server-side session validation with `SECRET_KEY` encryption
- **Revocation:** Logout immediately invalidates session 

#### 6. CSRF Protection with Flask-WTF
**Decision:** Enable global CSRF protection for all POST requests.

**Rationale:**
- **OWASP Top 10:** Mitigates CSRF attacks (A01:2021 - Broken Access Control)
- **Automatic Validation:** Flask-WTF validates tokens without manual checks
- **Token Rotation:** Each form submission gets unique token
- **Hidden Input:** `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">` transparent to users

#### 7. Password Hashing with Werkzeug
**Decision:** Use Werkzeug's `generate_password_hash` and `check_password_hash`.

**Rationale:**
- **No Plain Text:** Passwords never stored or logged in readable form
- **One-Way Hash:** Cannot reverse-engineer original password from hash


#### 8. Input Validation Strategy
**Decision:** Server-side validation with regex patterns and range checks.

**Rationale:**
- **Password Complexity:** Enforces strong passwords at registration
- **Numeric Ranges:** Age (0-120), BMI (10-100), Glucose (0-500) prevent data corruption
- **Early Rejection:** Failed validations return error messages before database queries

#### 9. Custom 404 Error Page
**Decision:** Implement branded 404 page with role-aware navigation.

**Rationale:**
- **User Experience:** Avoids generic Flask error page
- **Security:** Prevents information leakage
- **Navigation:** Authenticated users get "Dashboard" button; guests get "Login"/"Home"

#### 10. Pagination for Patient Records
**Decision:** Server-side pagination with configurable page size (10/25/50/100).

**Rationale:**
- **Performance:** Avoid loading 1000+ patient records at once
- **Usability:** Users can navigate large datasets efficiently
- **Scalability:** MongoDB `skip()` and `limit()` queries scale to millions of records

### Security Design Decisions


#### 1. Environment-Based Secrets
**Decision:** Store `SECRET_KEY`, `MONGO_URL`, `DB_NAME` in `.env` file.

**Rationale:**
- **12-Factor App:** configuration is kept out of the codebase and managed through environment variables
- **Security:** `.env` in `.gitignore` prevents secret leakage
- **Flexibility:** Easy to change secrets in environment
- **No Hardcoding:** Source code remains public-safe


## Security Notes

- CSRF protection enabled globally
- Passwords hashed using Werkzeug
- Session stores `user_id` and `role` only
- RBAC enforced via decorators and template conditionals
- Input validation for email, password complexity, and patient numeric fields
- Custom 404 error page with conditional navigation

## Acknowledgements

World Health Organization (WHO) for the dataset

Leeds Trinity University for the course module

Project developed by Lilian Ofuonye following the Secure Software Development Principles. 

