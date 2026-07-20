# Sri Lanka Air Force (SLAF) Trade Training School Management Portal

An enterprise-grade, secure, modular, and responsive management portal for the Sri Lanka Air Force Trade Training School (SLAF TTS). This system replaces manual records, spreadsheet tracking, and disconnected systems with a centralized Single Source of Truth (SSOT).

---

## Features

1. **User & Access Management (RBAC)**: Secure authorization, token-based JWT credentials, dynamic permissions, account locking policies, and audit logs.
2. **Student Details Management (SSOT)**: The core master repository of trainee profiles, service data, emergency info, and printable QR codes.
3. **Daily Parade State Board**: Instant military strength reporting. Automatic updates flow into academic timetables and dashboards.
4. **Accommodation Management**: Interactive bed allocations, room logs, and billet vacancies.
5. **Academic & Performance Tracker**: Timetable mapping, lesson plans, course syllabus logs, examinations, and grade distributions.
6. **Executive Dashboard**: Command KPIs, interactive charts (Chart.js / Recharts), live strength tracking, and notification cards.
7. **Audit & Activity System**: In-depth trace log detailing administrative operations, database transactions, and user logins.

---

## Tech Stack

* **Frontend**: React.js (Vite), React Router DOM, Bootstrap 5, Bootstrap Icons, Axios, React Hook Form, Zod, Chart.js, FullCalendar.
* **Backend**: Python 3.13+, FastAPI, SQLAlchemy ORM, SQLite (local dev fallback) / MySQL 8.0, PyJWT, passlib (bcrypt).
* **Database**: MySQL 8.0+ / SQLite.
* **Containerization**: Docker, Docker Compose.

---

## Quick Start (Local Run)

### Method 1: Docker Compose (All Services with MySQL)

1. Ensure Docker Desktop is running.
2. Run the following command in the project root:
   ```bash
   docker-compose up --build
   ```
3. Open:
   - Frontend: [http://localhost](http://localhost) (Nginx served)
   - Backend APIs (Swagger docs): [http://localhost:8000/docs](http://localhost:8000/docs)

### Method 2: Manual Standalone Dev Server (Using SQLite Fallback)

To run without installing or starting MySQL locally:

#### Backend
1. Open a terminal, go to `backend/`
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server (automatically creates a local `database.db` SQLite file):
   ```bash
   python run.py
   ```
   *The backend will boot up on [http://localhost:8000](http://localhost:8000)*

#### Frontend
1. Open another terminal, go to `frontend/`
2. Install npm packages:
   ```bash
   npm install
   ```
3. Run Vite dev server:
   ```bash
   npm run dev
   ```
   *The frontend will run on [http://localhost:5173](http://localhost:5173)*

### Pre-Seeded Administrator Login
- **Username**: `admin`
- **Password**: `Admin@123`

---

## Directory Structure

```text
tts-management-portal/
├── backend/            # FastAPI Python server
│   ├── app/            # Application logic (Controllers, Services, Models)
│   ├── run.py          # Standalone launcher script
│   └── Dockerfile      # Backend build context
├── frontend/           # React + Vite client app
│   ├── src/            # Components, pages, assets, contexts
│   └── Dockerfile      # Frontend multi-stage deployment build
├── database/           # DDL scripts and seeding
└── docs/               # Mermaid architectural diagrams
```

---

## Licensing
Proprietary and Confidential. Copyright (c) 2026 Sri Lanka Air Force Trade Training School.
