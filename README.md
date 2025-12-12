# Healthcare Stroke Management System

A secure, web-based Flask application designed to help healthcare professionals record, manage, and analyze patient data
to assess stroke risk.
Built with a strong focus on security, usability, and data privacy, the system supports role-based access for clinicians and
administrator in a hospital setting.

## Features

- Secure User Authentication
- Patient Data Management (Demographics, Medical History, Lifestyle)
- Admin Dashboard for reviewing system users and users records
- Clinician Dashboard for reviewing predictions and managing patient records
- Secure Session Handling & Input Validation
- Zero Trust Architecture and OWASP-aligned security practices

## System Architecture

#### The application follows a three-layered architecture aligned with SSDLC principles:

| Layer                  | Description                                            | Security Controls                                                                                                                        |
| ---------------------- | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **Presentation Layer** | Flask HTML templates (Jinja2), forms, and Tailwind UI | Input validation, CSRF protection                                                                                                        |
| **Application Layer**  | Flask backend (business logic, RBAC, authentication)   | RBAC, session management, exception handling                                                                                             |
| **Data Layer**         | SQLite (Auth), MongoDB (Patients Record)               | Encryption-at-rest (password hashes), least privilege DB access, integrity checks, injection (SQL/NoSQL injection, XSS) prevention      |

## Tech Stack

| Category           | Technology                                                                          |
| ------------------ | ----------------------------------------------------------------------------------- |
| **Framework**      | Flask (Python 3.x)                                                                  |
| **Frontend**       | HTML5, Tailwind (CDN), Jinja2 Templates                                             |
| **Databases**      | SQLite (auth), MongoDB (patients record)                                            |
| **Authentication** | Flask session, CSRF (Flask-WTF), password hashing (Werkzeug)                        |
| **Security**       | CSRF, XSS prevention (Jinja2 autoescape), input validation, RBAC, env-based secrets |
| **Environment**    | Python Virtual env (`venv`)                                                         |
| **Dev Tools**      | Unittest (built-in), pytest (optional)                                              |

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/CS-LTU/com7033-assignment-julianaifionu.git

# Go to project directory
cd com7033-assignment-julianaifionu
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and set:

- `MONGO_URL` — your MongoDB connection string
- `DB_NAME` — MongoDB database name (e.g., HealthcareDB)
- `SECRET_KEY` — a secure, randomly generated secret key

Example:

```
MONGO_URL=mongodb://localhost:27017
DB_NAME=HealthcareDB
SECRET_KEY=supersecretkey-CHANGE-ME
```

For development or testing, you may keep defaults or modify them as needed.

## Run the Application

```bash
# ensure you are in the project root
# typical Flask entry via app factory
python -c "from app import create_app; app=create_app(); app.run(host='127.0.0.1', port=5000, debug=True)"
```

Access it at 👉 http://localhost:5000/

## Run all Tests

Using unittest (module discovery):

```bash
python -m unittest discover -s app/tests -p "*.py" -v
```

Or run a specific test file:

```bash
python app/tests/unit_test1.py
```

## API & Routes Reference

### Authentication Routes (`/`)

| Method | Route | Access | Description | Required Fields |
|--------|-------|--------|-------------|-----------------|
| GET | `/` | Public | Landing page | - |
| GET/POST | `/login` | Public | User login | email, password |
| GET/POST | `/register` | Public | User registration | first_name, last_name, email, password, confirm_password, role |
| GET/POST | `/forgot-password` | Public | Initiate password reset | email |
| GET/POST | `/reset-password` | Session | Complete password reset | password, confirm_password |
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
- **Scalability:** Easy to replace or upgrade individual layers (e.g., migrate to PostgreSQL without changing UI)

#### 2. Dual Database Strategy (SQLite + MongoDB)
**Decision:** Use SQLite for user authentication and MongoDB for patient records.

**Rationale:**
- **SQLite for Auth:**
  - Relational structure suits user-role relationships
  - ACID compliance critical for authentication data
  - Local file-based storage reduces external dependencies for auth
  - Simpler backup and recovery for critical user data

- **MongoDB for Patients:**
  - Flexible schema accommodates evolving medical data fields
  - Document model maps naturally to patient records (embedded health indicators)
  - Better performance for large-scale patient data retrieval
  - Future-proof for unstructured data (medical images, PDFs)

#### 3. Flask Framework Selection
**Decision:** Choose Flask over Django or FastAPI.

**Rationale:**
- **Lightweight:** Minimal overhead for focused healthcare application
- **Flexibility:** Freedom to choose security libraries (Flask-WTF for CSRF) without opinionated defaults
- **Learning Curve:** Simpler for understanding security implementation at lower level
- **Jinja2 Integration:** Built-in templating with automatic XSS protection

#### 4. Role-Based Access Control (RBAC)
**Decision:** Implement decorator-based RBAC with two roles (Admin, Doctor).

**Rationale:**
- **Least Privilege Principle:** Doctors can only view/update; Admins have full CRUD
- **Decorator Pattern:** Reusable `@admin_required` and `@doctor_required` decorators reduce code duplication
- **Template-Level Enforcement:** Conditional rendering (`{% if session.role == 'admin' %}`) prevents UI confusion
- **Defense in Depth:** Server-side decorator + client-side template checks

#### 5. Session-Based Authentication (Not JWT)
**Decision:** Use Flask's encrypted session cookies instead of JWT tokens.

**Rationale:**
- **Simplicity:** No need for token management, refresh logic, or token storage
- **Security:** Server-side session validation with `SECRET_KEY` encryption
- **Revocation:** Logout immediately invalidates session (no token expiry wait)
- **Stateful:** Suitable for web application (not API-first architecture)

#### 6. CSRF Protection with Flask-WTF
**Decision:** Enable global CSRF protection for all POST/PUT/PATCH/DELETE requests.

**Rationale:**
- **OWASP Top 10:** Mitigates CSRF attacks (A01:2021 - Broken Access Control)
- **Automatic Validation:** Flask-WTF validates tokens without manual checks
- **Token Rotation:** Each form submission gets unique token
- **Hidden Input:** `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">` transparent to users

#### 7. Password Hashing with Werkzeug
**Decision:** Use Werkzeug's `generate_password_hash` and `check_password_hash`.

**Rationale:**
- **Industry Standard:** Uses PBKDF2 with salt by default
- **No Plain Text:** Passwords never stored or logged in readable form
- **One-Way Hash:** Cannot reverse-engineer original password from hash
- **Built-in:** No external dependencies (bcrypt, Argon2) for course project

#### 8. Input Validation Strategy
**Decision:** Server-side validation with regex patterns and range checks.

**Rationale:**
- **Defense in Depth:** Never trust client-side validation (can be bypassed)
- **Email Validation:** Regex prevents invalid formats before database insertion
- **Password Complexity:** Enforces strong passwords at registration
- **Numeric Ranges:** Age (0-120), BMI (10-100), Glucose (0-500) prevent data corruption
- **Early Rejection:** Failed validations return error messages before database queries

#### 9. Custom 404 Error Page
**Decision:** Implement branded 404 page with role-aware navigation.

**Rationale:**
- **User Experience:** Avoids generic Flask error page
- **Security:** Prevents information leakage (no stack traces, file paths)
- **Navigation:** Authenticated users get "Dashboard" button; guests get "Login"/"Home"
- **Branding:** Maintains consistent theme (emerald/slate colors)

#### 10. Pagination for Patient Records
**Decision:** Server-side pagination with configurable page size (10/25/50/100).

**Rationale:**
- **Performance:** Avoid loading 1000+ patient records at once
- **Usability:** Users can navigate large datasets efficiently
- **Scalability:** MongoDB `skip()` and `limit()` queries scale to millions of records
- **URL State:** Page number in URL allows bookmarking/sharing specific views

### Security Design Decisions

#### 1. No Audit Logging (Conscious Trade-off)
**Decision:** Omit audit trail for initial version.

**Rationale:**
- **Scope Management:** Focus on core CRUD and security features first
- **Performance:** Avoid write overhead for every operation
- **Future Enhancement:** Designed MongoDB `logs` collection schema for easy addition
- **Acceptable Risk:** Educational project; production systems would require this

#### 2. Environment-Based Secrets
**Decision:** Store `SECRET_KEY`, `MONGO_URL`, `DB_NAME` in `.env` file.

**Rationale:**
- **12-Factor App:** Configuration separate from code
- **Security:** `.env` in `.gitignore` prevents secret leakage
- **Flexibility:** Easy to change secrets per environment (dev/test/prod)
- **No Hardcoding:** Source code remains public-safe

#### 3. Jinja2 Autoescape for XSS Prevention
**Decision:** Rely on Jinja2's default autoescape feature.

**Rationale:**
- **Built-in Protection:** All `{{ variable }}` outputs HTML-escaped automatically
- **Zero Configuration:** Enabled by default in Flask
- **Prevents XSS:** User input like `<script>alert('XSS')</script>` rendered as text
- **Manual Override:** Use `{{ variable|safe }}` only when absolutely necessary

## Entity Relationship Diagram for SQLite DB

![ERD](screenshots/erd.png)

## MongoDB Schema Diagram

**Collection:** `patients`

| Field             | Type          | Description                            |
| ----------------- | ------------- | -------------------------------------- |
| \_id              | ObjectId      | Primary key                            |
| id                | int           | Patient ID                             |
| gender            | string        | Gender                                 |
| age               | int           | Age                                    |
| hypertension      | int (0/1)     | Hypertension indicator                 |
| heart_disease     | int (0/1)     | Heart disease indicator                |
| ever_married      | string        | Marital status                         |
| work_type         | string        | Type of work                           |
| Residence_type    | string        | Urban/Rural                            |
| avg_glucose_level | float         | Glucose level                          |
| bmi               | float         | Body Mass Index                        |
| smoking_status    | string        | Smoking category                       |
| stroke            | int (0/1)     | Stroke history indicator               |
| created_at        | datetime      | Timestamp when created                 |

---

**Collection:** `logs` (optional, future audit trail)

| Field   | Type     | Description                     |
| ------- | -------- | --------------------------------|
| \_id    | ObjectId | Primary key                     |
| action  | string   | Description of the action taken |
| details | object   | Metadata about the action       |
| ts      | datetime | Timestamp of the logged event   |

## Security Notes

- CSRF protection enabled globally (Flask-WTF)
- Passwords hashed using Werkzeug
- Session stores `user_id` and `role` only
- RBAC enforced via decorators and template conditionals
- Input validation for email, password complexity, and patient numeric fields
- Custom 404 error page with conditional navigation

## Acknowledgements

World Health Organization (WHO) for the dataset

Flask communities for excellent documentation

LTU for the course module

Developed by [Juliana Ifionu](https://www.linkedin.com/in/julianaifionu/) as part of a secure software development
project under SSDLC principles.
