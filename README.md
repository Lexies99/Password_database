# Password_database

### Central Identity Provider & Single Sign-On (SSO) Microservice for Multi-Application Ecosystems

`Password_database` is an independent, centralized authentication and identity management service. It guarantees that users across multiple web applications (e.g. **GIMPA Thesis Repository** and **SOTSS Library Application**) use a single unified password with instantaneous synchronization, role-based access control, and complete audit logging.

---

## 🏗 System Architecture

```
                                  [ User Browser ]
                                         │
                   ┌─────────────────────┴─────────────────────┐
                   ▼                                           ▼
      ┌─────────────────────────┐                 ┌─────────────────────────┐
      │   Thesis Repository     │                 │   SOTSS Library App     │
      │ thesis.manamatech...    │                 │ libraryapp.manamatech...│
      └────────────┬────────────┘                 └────────────┬────────────┘
                   │                                           │
                   │   POST /api/v1/auth/verify-credentials    │
                   └─────────────────────┬─────────────────────┘
                                         ▼
                   ┌───────────────────────────────────────────┐
                   │            Password_database              │
                   │      (Central Identity Provider IdP)      │
                   │                                           │
                   │  - Argon2id / Bcrypt Cryptographic Hash   │
                   │  - Single Source of Truth for Passwords   │
                   │  - Instant Multi-App Synchronization      │
                   │  - Comprehensive Security Audit Logs      │
                   │  - Primary + Secondary Role Management    │
                   └───────────────────────────────────────────┘
```

---

## 🚀 Key Features

1. **One Password Everywhere:** Users maintain a single password across all connected services without manual cross-database duplication.
2. **Instant Password Propagation:** Updating a password in any connected app or admin panel immediately takes effect everywhere.
3. **Advanced Role Management:** Supports both Primary Roles (e.g., Lecturer, Dean, HOD, Student) and Secondary Additional Roles (e.g., System Administrator, Department Editor).
4. **Security Audit Logging:** Tracks all authentication attempts (successful/failed), IP addresses, client applications, and credential modifications.
5. **OpenAPI / Swagger Documentation:** Interactive API explorer available at `/docs`.

---

## 📡 API Endpoints

### 1. Central Authentication & SSO
* `POST /api/v1/auth/verify-credentials`
  * **Payload:** `{"email": "user@gimpa.edu.gh", "password": "Password123!", "client_app": "library_app"}`
  * **Response:** Returns verification status, user details, role matrix, and signed JWT token.
* `POST /api/v1/auth/sync-password`
  * **Payload:** `{"email": "user@gimpa.edu.gh", "new_password": "NewPassword123!", "old_password": "OldPassword123!"}`
  * Updates password centrally and logs the audit event.

### 2. User & Role Management
* `GET /api/v1/users` - List users with filtering by role and search query.
* `POST /api/v1/users` - Create / provision a new user account.
* `GET /api/v1/users/{email}` - Retrieve user profile and role matrix.
* `POST /api/v1/users/assign-role` - Assign primary or secondary roles.

### 3. Diagnostics & Health
* `GET /api/v1/health` - Check service and database connectivity.
* `GET /docs` - Interactive OpenAPI Swagger UI.

---

## 🛠 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/Lexies99/Password_database.git
cd Password_database
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your desired database connection and secret keys
```

### 3. Seed Initial Accounts & Run
```bash
python scripts/seed_initial_users.py
python scripts/run_server.py
```
Open **http://localhost:8020/docs** in your browser.

---

## 🐳 Docker Deployment

```bash
docker-compose up -d --build
```

---

## 📄 License
MIT License. Developed for GIMPA Institutional Systems.
