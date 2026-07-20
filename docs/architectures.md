# SLAF TTS Management Portal System Architecture & Diagrams

This document contains architectural diagrams (Entity-Relationship, Use Case, Activity, Sequence, Class, Component, and Deployment) defined using Mermaid.

---

## 1. Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    roles ||--o{ users : has
    permissions ||--o{ role_permissions : defines
    roles ||--o{ role_permissions : map
    users ||--o{ login_history : records
    users ||--o{ audit_logs : triggers
    
    courses ||--o{ students : enrolled_in
    courses ||--o{ subjects : has
    subjects ||--o{ lessons : contains
    lessons ||--o{ lesson_plans : details
    
    students ||--o{ parade_states : log
    students ||--o{ accommodation_allocations : allocate
    accommodation_beds ||--o{ accommodation_allocations : allocated
    accommodation_rooms ||--o{ accommodation_beds : holds
    accommodation_billets ||--o{ accommodation_rooms : holds
    accommodation_buildings ||--o{ accommodation_billets : holds
    
    timetables ||--o{ academic_attendance : verify
    students ||--o{ academic_attendance : record
    exams ||--o{ exam_marks : grade
    students ||--o{ exam_marks : scores
```

---

## 2. Use Case Diagram

```mermaid
graph TD
    subgraph Users
        SA[Super Admin]
        CO[Commanding Officer]
        DS[Discipline Section]
        AS[Academic Section]
        AO[Accommodation Officer]
    end

    subgraph Portal Use Cases
        UC1[Manage Operators & User Accounts]
        UC2[Restore & Backup Database]
        UC3[View Live Strength Executive Dashboard]
        UC4[Export Trainee Details Dossier]
        UC5[Batch Update Daily Parade States]
        UC6[Configure Billets & Beds Maps]
        UC7[Assign Bed Allocations]
        UC8[Schedule Course Timetables]
        UC9[Enter Examination Grades & Marks]
    end

    SA --> UC1
    SA --> UC2
    SA --> UC3
    
    CO --> UC3
    CO --> UC4
    
    DS --> UC5
    DS --> UC4
    
    AO --> UC6
    AO --> UC7
    
    AS --> UC8
    AS --> UC9
```

---

## 3. Activity Diagram (Daily Parade Synchronization Workflow)

```mermaid
flowchart TD
    Start([Discipline Section Starts Status Updates]) --> SelectDate[Select Target Date & Fetch Trainees]
    SelectDate --> UpdateStatus[Modify Status Options e.g. Sick Report / AWOL]
    UpdateStatus --> ClickSave[Click Save Parade State]
    ClickSave --> SaveDB[(Write to parade_states Table)]
    SaveDB --> SSOT_Trigger{Trigger Sync Checks}
    
    SSOT_Trigger -->|Trainee Status updated| SyncTrainee[Update student.status in DB]
    SSOT_Trigger -->|Course schedule exists| SyncAcademic[Excused or Absent today's timetable periods]
    SSOT_Trigger -->|AWOL or Hospital flag| TriggerAlert[Add User Alarm Notification]
    
    SyncTrainee --> SyncFinish[Update Dashboard Live Counters]
    SyncAcademic --> SyncFinish
    TriggerAlert --> SyncFinish
    
    SyncFinish --> End([Notify User Success & Update Complete])
```

---

## 4. Sequence Diagram (User Login with Account Locking)

```mermaid
sequenceDiagram
    autonumber
    actor User as Portal Operator
    participant FE as React Client
    participant BE as FastAPI Backend
    participant DB as SQLite / MySQL DB

    User->>FE: Input username & password
    FE->>BE: POST /api/v1/auth/login
    BE->>DB: Query user record by username
    DB-->>BE: User data (failed_attempts=4, is_locked=False)
    
    alt Correct Password
        BE->>DB: Reset failed_attempts=0
        BE->>DB: Record LoginHistory status=SUCCESS
        BE-->>FE: JWT access_token & refresh_token
        FE-->>User: Navigate to Dashboard screen
    else Incorrect Password
        BE->>DB: Increment failed_attempts = 5
        BE->>DB: Set is_locked = True
        BE->>DB: Record LoginHistory status=LOCKED
        BE->>DB: Record AuditLog action=ACCOUNT_LOCKED
        BE-->>FE: HTTP 403 Forbidden (Account Locked)
        FE-->>User: Show "Account locked due to 5 failures" alert
    end
```

---

## 5. Class Diagram (Data Entities Layer)

```mermaid
classDiagram
    class TimeStampedModelMixin {
        +DateTime created_at
        +DateTime updated_at
        +DateTime deleted_at
        +soft_delete()
        +restore()
    }
    
    class User {
        +String id
        +String username
        +String email
        +String hashed_password
        +String full_name
        +String role_id
        +Boolean is_active
        +Boolean is_locked
        +Integer failed_login_attempts
    }
    
    class Student {
        +String id
        +String service_number
        +String initials
        +String full_name
        +String nic
        +Date dob
        +String gender
        +String rank
        +String trade
        +String status
        +String qr_code_data
    }
    
    class ParadeState {
        +String id
        +String student_id
        +Date date
        +String status
        +String remarks
        +String updated_by
    }

    User --|> TimeStampedModelMixin
    Student --|> TimeStampedModelMixin
    Student "1" *-- "many" ParadeState : has logs
```

---

## 6. Component Diagram (Layered Architecture)

```mermaid
graph LR
    subgraph Presentation Layer
        UI[React View components]
        Context[Auth & Theme Contexts]
        Services[Axios API Client Services]
    end

    subgraph Application Controller Layer
        Router[FastAPI API endpoints]
        Deps[Dependency injection & Auth guards]
    end

    subgraph Business Logic Layer
        ServiceLogic[Domain Services & SSOT Sync Triggers]
    end

    subgraph Data Repository Layer
        Repo[Generic Base repositories]
        Models[SQLAlchemy Database models]
    end

    UI --> Context
    UI --> Services
    Services -->|HTTP requests| Router
    Router --> Deps
    Router --> ServiceLogic
    ServiceLogic --> Repo
    Repo --> Models
    Models -->|SQL queries| Database[(SQLite / MySQL Database)]
```

---

## 7. Deployment Diagram (Containerized Network)

```mermaid
graph TD
    Browser[Client Browser Web Interface] -->|Port 80/443| Nginx[Nginx Container]
    Nginx -->|Proxy pass /api/| FastAPI[FastAPI Backend Container]
    
    subgraph Docker Bridge Network
        Nginx
        FastAPI
        FastAPI -->|Port 3306| MySQL[(MySQL 8 Database Container)]
    end
    
    FastAPI -->|Write static photos| UploadVolume[(Docker Volumes - Uploads)]
    MySQL -->|Persist Tables data| MySQLVolume[(Docker Volumes - MySQL data)]
```
