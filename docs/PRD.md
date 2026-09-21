# SRI LANKA AIR FORCE TRADE TRAINING SCHOOL (SLAF TTS)
# PRODUCT REQUIREMENTS DOCUMENT (PRD.md)

---

## 1. Product Overview

The **Sri Lanka Air Force (SLAF) Trade Training School (TTS) Management Portal** is a centralized web-based ERP and operational administration system designed to manage all vocational training pipelines, trainee life cycles, daily military muster accountability, academic assessments, accommodation logistics, and disciplinary occurrence reporting.

This Product Requirements Document (PRD) defines **WHAT** the system provides to its end users, specifying the complete functional baseline, user workflows, business rules, validation constraints, and acceptance criteria across all system modules.

---

## 2. Product Vision

To establish an authoritative, secure, transparent, and seamless digital environment that optimizes military vocational training administration across all Sri Lanka Air Force trades, empowering commanders, instructors, and administrative staff with real-time operational insights, accurate academic tracking, and automated military strength accountability.

---

## 3. Product Goals

1. **Zero Data Redundancy**: Establish a Single Source of Truth (SSOT) where trainee, course, batch, instructor, and billet data are entered once and referenced universally.
2. **Instant Operational Strength Accountability**: Reduce morning muster consolidation time from hours to seconds through digital parade state submissions and automatic instructor approvals.
3. **Transparent Academic Progression**: Provide intuitive, chronological Phase Test progress visualization for every trainee with accurate percentage and grading calculations.
4. **Automated Cross-Module Synchronization**: Eliminate discrepancies by automatically reflecting parade state absences (Sick Report, Hospital, Leave, AWOL) into classroom attendance registers and exam eligibility rolls.
5. **Standardized Military Documentation**: Provide publication-quality formal PDF and Excel reports adhering to official SLAF TTS document presentation standards.
6. **Robust Access Governance**: Enforce least-privilege role-based access control (RBAC), password hygiene policies, and immutable action audit logging.

---

## 4. Target Users

- **Commanding Officer (CO)**: Executive decision-maker overseeing school strength, training output, and disciplinary posture.
- **Officer Commanding Training (OCT) / Academic Staff**: Officers and NCOs planning courses, batch allocations, calendars, examinations, and mark sheets.
- **Discipline Section Officers & NCOs**: Personnel responsible for daily morning parade states, nominal rolls, trainee profiles, and occurrence reporting.
- **Accommodation Officer / Billet NCOs**: Personnel managing living billets, bunk beds, and trainee room allocations.
- **Trade Instructors**: Service instructors delivering syllabus lessons, recording timetable attendance, and evaluating phase tests.
- **System Administrators**: Technical IT personnel managing user accounts, security parameters, and system health.

---

## 5. User Roles

| Role | Description | Key Modules Accessible |
| :--- | :--- | :--- |
| **Super Administrator** | Full administrative and security privileges. | All modules, system settings, RBAC, logs. |
| **System Administrator** | Core operational database administration. | User management, master data, audit logs. |
| **Commanding Officer** | Executive oversight and formal sign-offs. | Executive dashboard, reports, parade approvals. |
| **Discipline Section** | Trainee master profiles and daily muster. | Student management, parade states, occurrences. |
| **Academic Section** | Syllabus, course lifecycle, exams, calendars. | Academic module, exams, marks, course calendar. |
| **Accommodation Officer** | Trainee quarters and bed allocations. | Buildings, billets, bunk beds, allocations. |
| **Instructor** | Direct class delivery and evaluations. | Class registers, exams, lesson plans, approvals. |
| **Viewer** | Read-only inspection privileges. | Dashboard, student rosters, general summaries. |

---

## 6. User Problems and Business Solutions

| Business Problem | Operational Impact | TTS Portal Solution |
| :--- | :--- | :--- |
| **Fragmented Nominal Rolls** | Trainee bio-data existed in separate paper files across squadrons and trades. | Centralized Trainee Management with unique Service Number indexing, digital QR badge, and profile search. |
| **Delayed Strength Muster** | Morning parade states took hours to manually collate from billets and trades. | Two-stage digital Parade State with trade-level submission, auto-assigned instructor routing, and instant strength calculation. |
| **Academic Progress Gaps** | Instructors could not easily view a trainee's chronological marks trend across Phase Tests. | Dedicated Trainee Academic Progress dashboard with dynamic Chart.js line charts (0–100%) and KPI summaries. |
| **Exam Eligibility Disconnect** | Trainees admitted to hospital or on AWOL could accidentally appear on exam lists. | Automatic sync between approved parade states and examination marksheets with formal officer override capabilities. |
| **Bunk Bed Double Booking** | Physical accommodation records led to bed over-allocation and untracked vacancies. | Interactive Billet Management splitting physical bunk beds into distinct TOP and BOTTOM positions with live vacancy maps. |
| **Unformatted Screen Prints** | Printing from browser produced messy UI screenshots rather than formal military letters. | Dedicated server-side compiled classical PDF and Excel reports with official bilingual headers, tables, and signature blocks. |

---

## 7. Functional Requirements

---

### Module A: Trainee Personnel Details Management

#### Requirement ID: `PRD-TRN-001`
- **Status**: `[IMPLEMENTED]`
- **Purpose**: Manage the comprehensive master personnel record for every military trainee undergoing instruction at SLAF TTS.
- **Target Users**: Discipline Section, Academic Section, System Administrators, Commanding Officer.
- **Main Functions**:
  1. Trainee registration with validation of unique Service Number and NIC.
  2. Search, filter, and paginate trainee directory by Trade, Course, Batch, Rank, and Status.
  3. Edit personal, military, and emergency contact details.
  4. Upload and manage official profile photographs.
  5. Generate and print scannable Digital QR Badges.
- **User Workflow**:
  - User navigates to `/students` -> clicks "Add New Trainee" (`/students/new`).
  - Active course/batch dropdown is populated from Academic single source of truth.
  - User inputs details -> clicks Save -> Trainee profile created with QR code -> redirect to `/students/:id`.
- **Inputs**: Service Number, Rank, Initials, Full Name, NIC, Date of Birth, Gender, Trade, Course ID, Batch, Enlistment Date, Phone, Email, Emergency Contact Name/Phone, Blood Group, Medical Category, Permanent Address, Photo.
- **Outputs**: Trainee Master Profile, Scannable QR Code Data, Photo URL, Printable Trainee Dossier.
- **Business Rules**: `BR-TRN-001` (Service Number unique); `BR-TRN-002` (Course must be active).
- **Permissions**: `student:read` (View), `student:write` (Create/Edit/Delete).
- **Validation Requirements**: Service number required and non-duplicate; NIC format validation; End date >= Start date.
- **Acceptance Criteria**:
  - New trainee record saved successfully and visible in nominal roll.
  - Unique constraint violation returns clear HTTP 400 error message.
  - QR Code generates valid JSON payload containing Service Number, Rank, Name, and Trade.

---

### Module B: Trainee Personal Profile & Dossier

#### Requirement ID: `PRD-TRN-002`
- **Status**: `[IMPLEMENTED]`
- **Purpose**: Provide a dedicated single-page comprehensive dossier for an individual trainee combining personal, military, academic, and disciplinary records.
- **Target Users**: Commanding Officer, Discipline Section, Academic Section, Instructors.
- **Main Functions**:
  1. High-level visual profile card with rank insignia, photo, and status badge.
  2. Military service specifications (Service No, Rank, Trade, Course, Intake, Enlistment Date).
  3. Personal and emergency contact breakdown with blood group and medical classification.
  4. Scannable digital QR badge with one-click print modal.
  5. Embedded Academic Progress tracker (Module C).
  6. Embedded Personal Occurrence log (Module H).
  7. One-click generation of Classical Official Trainee Dossier PDF.
- **User Workflow**: User opens `/students/:id` -> reviews integrated tabs and embedded sections -> clicks "Print Official Dossier" to view formal layout.
- **Permissions**: `student:read`.
- **Acceptance Criteria**: Profile loads within 300ms, displaying complete linked academic and disciplinary history without page reloads.

---

### Module C: Trainee Personal Academic Progress

#### Requirement ID: `PRD-ACA-001`
- **Status**: `[IMPLEMENTED]`
- **Purpose**: Track, compute, and visualize a trainee's Phase Test examination performance progression throughout their enrolled course using actual database records.
- **Target Users**: Trainees, Instructors, Academic Section, Commanding Officer.
- **Main Functions**:
  1. Retrieve all chronological Phase Test results for the selected trainee from `exam_marks` and `exams` tables.
  2. Compute real-time performance summary KPIs:
     - **Tests Completed** (count of evaluated tests)
     - **Average Percentage** (cumulative arithmetic mean)
     - **Latest Percentage** (most recent phase score)
     - **Highest Percentage** (peak phase score)
     - **Lowest Percentage** (lowest phase score)
     - **Passed Tests** (count of scores >= pass marks)
     - **Failed Tests** (count of scores < pass marks)
  3. Render a responsive **Line Chart** displaying marks progression:
     - **X-axis**: Phase Test Name / Phase (`Phase 1`, `Phase 2`, etc.) in chronological order.
     - **Y-axis**: Percentage (%) scaled from `0%` to `100%`.
     - **Pass Benchmark Line**: Horizontal reference line at `50%` pass threshold.
     - **Interactive Tooltips**: Display Phase Test title, Subject Name, Date, Obtained Marks, Max Marks, Grade, and Status.
  4. Render a detailed **Phase Test Results Breakdown Table**:
     | Column | Content |
     | :--- | :--- |
     | **#** | Chronological Index (1, 2, 3...) |
     | **Phase Test** | Phase Name & Exam Type |
     | **Subject / Academic Area** | Subject Name & Code |
     | **Date** | Date of examination |
     | **Max Marks** | Maximum allocated marks (e.g., 100) |
     | **Obtained Marks** | Actual score achieved |
     | **Percentage** | Calculated percentage with visual progress bar |
     | **Grade** | Standard SLAF grade (Distinction A+, Distinction A, Credit B, Pass C, Fail F) |
     | **Status** | Pass, Fail, Absent, Sick Report, or Overridden |
     | **Remarks** | Specific remarks or override justifications |
  5. **Empty State Handling**: When no Phase Test records exist, display:
     `"No Phase Test results available."` with an explanatory notice.
  6. **Data Integrity Guarantee**: Absolutely NO hardcoded or dummy academic figures. Data is pulled strictly from live relational queries.
- **Mathematical Calculation**:
  $$\text{Percentage} = \left(\frac{\text{Obtained Marks}}{\text{Maximum Marks}}\right) \times 100$$
- **Grading Scale**:
  - $\ge 85\%$: Distinction (A+)
  - $75\% - 84.99\%$: Distinction (A)
  - $65\% - 74.99\%$: Credit (B)
  - $50\% - 64.99\%$: Pass (C)
  - $< 50\%$: Fail (F)
- **API Endpoint**: `GET /api/v1/students/{student_id}/academic-progress` (and alias `GET /api/v1/academic/trainees/{trainee_id}/academic-progress`).
- **Permissions**: `student:read` or `academic:read`.
- **Acceptance Criteria**:
  - Phase tests render in exact date/phase chronological sequence.
  - Average, Highest, Lowest, and Latest metrics correctly update upon new mark entries.
  - Zero-data state cleanly displays the specified fallback message without rendering broken charts.

---

### Module D: Daily Parade State & Military Strength Management

#### Requirement ID: `PRD-PAR-001`
- **Status**: `[IMPLEMENTED]`
- **Purpose**: Manage daily morning muster, track attendance/absence categories, enforce two-stage instructor approvals, and compute official Daily Strength.
- **Target Users**: Discipline Section (NCOs), Assigned Instructors, Commanding Officer.
- **Main Functions**:
  1. **Daily Muster Recording**: Daily nominal roll selection by Date, Trade, Course, and Batch.
  2. **Status Categorization**: Mark personnel as `Present`, `Sick Report`, `Hospital`, `Leave`, `Temporary Duty`, `Course Visit`, `Detached Duty`, or `AWOL`.
  3. **Automatic Instructor Identification**: The system automatically determines the responsible approving Instructor from the ongoing Course/Batch assignment (`batch.instructor_id`). Submitting operators **cannot** manually search or select an arbitrary instructor.
  4. **Draft Auto-Saving**: Save in-progress muster records as `DRAFT` without triggering downstream changes.
  5. **Formal Submission**: Submit completed trade parade state (`SUBMITTED`), creating an in-app alert for the assigned instructor.
  6. **Instructor Review & Approval**: Assigned instructor reviews per-trainee muster and clicks `Approve` (`APPROVED`) or `Return for Correction` (`REJECTED`) with mandatory justification.
  7. **Downstream Synchronization**:
     - Approving a parade state automatically updates `students.status` in the master table.
     - Automatically creates or updates `academic_attendance` records for that day (marking non-present trainees as `Excused` or `Absent`).
     - If `AWOL` or `Hospital` status is confirmed, automated critical alert notifications are dispatched to the Commanding Officer and Super Administrator.
  8. **Official Daily Strength Integration**: Only `APPROVED` parade states contribute to the official executive Daily Strength counters.
  9. **Historical Audit Immutability**: The approving officer's ID is permanently sealed on the approved submission record, preserving audit integrity even if instructor assignments subsequently change.
- **Monitoring & Compliance**:
  - Live status tracking across all required trades: `NOT SUBMITTED`, `PENDING APPROVAL`, `APPROVED`, `RETURNED FOR CORRECTION`.
  - Dedicated endpoints for `/monitoring/outstanding` and `/monitoring/date-range`.
- **Permissions**: `parade:read` (View), `parade:write` (Submit Draft/Muster), `parade:approve` (Instructor Approval/Return), `parade:manage_officers` (Officer I/C Assignment).
- **Acceptance Criteria**:
  - Non-assigned instructors attempting approval receive HTTP 403 Forbidden.
  - Unapproved parade states do not alter the executive Daily Strength card.
  - Approved parade state immediately updates that day's classroom attendance registry.

---

### Module E: Classroom Attendance Registry

#### Requirement ID: `PRD-ATT-001`
- **Status**: `[IMPLEMENTED]`
- **Purpose**: Manage daily classroom attendance for course cohorts, valid for the full day, integrated with the daily parade muster.
- **Target Users**: Instructors, Academic Section.
- **Main Functions**:
  1. Full-day daily classroom attendance marking per Course and Batch (individual period selection is not required; attendance applies to the entire training day).
  2. Auto-population of excused absences from morning approved Parade State.
  3. Batch attendance marking (`Mark All Present`, individual status toggles).
  4. Course-wise and student-wise attendance percentage reporting.
- **Permissions**: `academic:read`, `academic:write`.
- **Acceptance Criteria**: Daily attendance is recorded per date and course/batch, applying for the full day without requiring period-by-period breakdown, and reflects parade absence reasons automatically with remark `"Auto-synced on parade approval"`.

---

### Module F: Examination & Result Sheets

#### Requirement ID: `PRD-EXM-001`
- **Status**: `[IMPLEMENTED]`
- **Purpose**: Administer Phase Tests and Final Examinations, enforce parade-based eligibility, manage marks entry, and publish Marksheets.
- **Target Users**: Academic Section, Instructors, Commanding Officer.
- **Main Functions**:
  1. Schedule Phase Tests and Final Examinations for specific Courses and Subjects.
  2. Set Maximum Marks, Pass Marks, and examination dates.
  3. Enforce Parade Eligibility: Trainees with non-eligible parade statuses (`SICK_REPORT`, `HOSPITAL`, `LEAVE`, `AWOL`) cannot sit examinations by default.
  4. Formal Officer Eligibility Override: Authorized academic officers can override eligibility with a mandatory reason, stamping `is_overridden=True`, authorizer ID, and timestamp.
  5. Bulk marks entry with instant pass/fail evaluation and grade assignment.
  6. Generate printable classical Examination Result Marksheets (PDF/Excel).
- **Permissions**: `academic:read`, `academic:write`.
- **Acceptance Criteria**: Ineligible trainees are locked from mark entry unless formally overridden; mark updates immediately reflect on the Trainee Academic Progress chart.

---

### Module G: Accommodation & Billeting Management

#### Requirement ID: `PRD-ACC-001`
- **Status**: `[IMPLEMENTED]`
- **Purpose**: Manage physical living quarters, billets, and bunk beds, track occupancy rates, and allocate bed positions to trainees.
- **Target Users**: Accommodation Officer, Discipline Section.
- **Main Functions**:
  1. Manage Accommodation Buildings (Officers, Airmen, Airwomen quarters).
  2. Manage Billets with block, location, physical bunk bed count, and total sleeping capacity.
  3. Manage Physical Bunk Beds, splitting each into two distinct positions: `TOP` and `BOTTOM`.
  4. Position Status Tracking: `Available`, `Occupied`, `Reserved`, `Maintenance`.
  5. Interactive Visual Allocation Map showing occupied and vacant bed positions.
  6. Trainee Bed Allocation, Transfer between billets/positions, and Vacating.
  7. Full allocation history tracking (who allocated, who vacated, reason, dates).
- **Business Rules**: `BR-ACC-001` (Only 1 trainee per position); `BR-ACC-002` (Vacating immediately frees position).
- **Permissions**: `room:read`, `room:write`.
- **Acceptance Criteria**: Allocating a bed changes position status to `Occupied`; vacating changes position status to `Available` and records a history entry.

---

### Module H: Personal Occurrence Reporting (Achievements & Misconduct)

#### Requirement ID: `PRD-OCC-001`
- **Status**: `[IMPLEMENTED]`
- **Purpose**: Maintain an authoritative disciplinary and merit record for every trainee, logging achievements, commendations, infractions, punishments, and offenses.
- **Target Users**: Discipline Section, Commanding Officer, Instructors.
- **Main Functions**:
  1. Record occurrences categorized as `ACHIEVEMENT` or `MISCONDUCT_OFFENSE`.
  2. Quick lookup of trainee by exact Service Number.
  3. Store Occurrence Date, Title, Detailed Description, Remarks, and Author/Modifier IDs.
  4. Trainee dossier integration: Displays directly inside the Trainee Profile (`/students/:id`).
  5. Search and filter occurrences across dates, trades, batches, and occurrence types.
  6. Soft-deletion governed by permissions.
  7. Export official Trainee Conduct and Occurrence Dossier (PDF/Excel).
- **Permissions**: `personal_occurrence:read`, `personal_occurrence:write`, `personal_occurrence:delete`.
- **Acceptance Criteria**: Logged occurrences immediately appear on the trainee's profile and in formal PDF dossier exports.

---

### Module I: Course Calendar & Academic Lifecycle

#### Requirement ID: `PRD-ACA-002`
- **Status**: `[IMPLEMENTED]`
- **Purpose**: Manage course phases, syllabus progression, theory/practical period allocations, and automated batch closure.
- **Target Users**: Academic Section, Instructors.
- **Main Functions**:
  1. Define sequential training phases for each course with Serial Numbers.
  2. Track Theory Periods, Practical Periods, Total Periods, and Working Days.
  3. Validate Commencement and Completion Dates within course overall boundaries.
  4. Track Instructor Assignment Status (`ASSIGNED` / `NOT_ASSIGNED`).
  5. Visual Gantt / FullCalendar schedule view.
  6. **Automated Batch Closure**: Automatically transitions courses and batches to `PASSED OUT` when `end_date < today`.
- **Permissions**: `academic:read`, `academic:write`.
- **Acceptance Criteria**: Date modifications check for existing timetable/calendar conflicts and block invalid ranges.

---

### Module J: Enterprise Reports & Formal Printing

#### Requirement ID: `PRD-REP-001`
- **Status**: `[IMPLEMENTED]`
- **Purpose**: Generate server-compiled, official Sri Lanka Air Force documentation in PDF and Excel formats.
- **Target Users**: All authenticated users (governed by role permissions).
- **Main Functions**:
  1. **Trainee Nominal Roll / Dossier Report**: Detailed personal, military, and academic roster.
  2. **Parade State & Strength Report**: Daily muster summary, trade breakdown, and absence lists.
  3. **Examination Results & Marksheet Report**: Official course exam marks, pass/fail status, and grade averages.
  4. **Classroom Attendance Register Report**: Subject and session attendance summaries.
  5. **Billeting & Accommodation Report**: Billet occupancy, bunk vacancy, and allocation registers.
  6. **Outstanding Parade State Compliance Report**: Multi-day trade compliance tracking.
  7. **Personal Occurrence Dossier**: Complete merit and disciplinary history.
  8. **Format Requirements**:
     - Strict A4 layout (Portrait or Landscape).
     - Official bilingual SLAF TTS header and crest.
     - Summary KPI statistics block.
     - Bordered, striped data tables with repeating headers on multi-page documents.
     - Formal military signature blocks (Prepared By, Verified By, Approved By).
     - Native Excel (`.xlsx`) generation via OpenPyXL and PDF generation via ReportLab.
- **Permissions**: `reports:read`.
- **Acceptance Criteria**: Report generation executes purely on backend; downloaded files open cleanly in Adobe Acrobat and Microsoft Excel.

---

### Module K: User Management, RBAC & Security Administration

#### Requirement ID: `PRD-ADM-001`
- **Status**: `[IMPLEMENTED]`
- **Purpose**: Administer system operators, enforce password security policies, manage roles and granular permissions, and review security logs.
- **Target Users**: Super Administrators, System Administrators.
- **Main Functions**:
  1. Provision, edit, lock, and deactivate user accounts.
  2. Assign pre-seeded roles or attach direct user permission overrides.
  3. Enforce enterprise password policy (minimum 12 chars, upper, lower, number, special char).
  4. Track failed login attempts; automatically lock account after 5 consecutive failures.
  5. Prevent password reuse against the last 5 historically used passwords.
  6. Review immutable Audit Logs detailing operator IP, User Agent, action, and changes.
  7. Review Login History with success, failed, and locked connection timestamps.
- **Permissions**: `system:audit` (and Super/System Admin role membership).
- **Acceptance Criteria**: Locked users cannot authenticate; direct permission additions take effect immediately on next token refresh.

---

## 8. Summary of Requirement Identifiers

| Requirement ID | Module | Implementation Status |
| :--- | :--- | :--- |
| `PRD-TRN-001` | Trainee Details Management & Directory | `[IMPLEMENTED]` |
| `PRD-TRN-002` | Trainee Personal Profile & Dossier | `[IMPLEMENTED]` |
| `PRD-ACA-001` | Trainee Academic Progress (Line Chart & KPIs) | `[IMPLEMENTED]` |
| `PRD-ACA-002` | Course Calendar & Academic Lifecycle | `[IMPLEMENTED]` |
| `PRD-ACA-003` | Trade, Course & Batch Masters | `[IMPLEMENTED]` |
| `PRD-ACA-004` | Lesson Plan Documents (Cloudinary Storage) | `[IMPLEMENTED]` |
| `PRD-PAR-001` | Daily Parade State & Two-Stage Workflow | `[IMPLEMENTED]` |
| `PRD-PAR-002` | Outstanding Parade State Monitoring | `[IMPLEMENTED]` |
| `PRD-ATT-001` | Classroom Attendance Registry | `[IMPLEMENTED]` |
| `PRD-EXM-001` | Examination, Marksheets & Eligibility Overrides | `[IMPLEMENTED]` |
| `PRD-ACC-001` | Accommodation & Bunk Bed Position Management | `[IMPLEMENTED]` |
| `PRD-OCC-001` | Personal Occurrence Reporting | `[IMPLEMENTED]` |
| `PRD-REP-001` | Enterprise Reports & Formal Printing Engine | `[IMPLEMENTED]` |
| `PRD-ADM-001` | User Management, RBAC & Security Policies | `[IMPLEMENTED]` |
| `PRD-AUD-001` | Audit Logging & Login History Tracking | `[IMPLEMENTED]` |
| `PRD-BIO-001` | Biometric Muster Integration | `[FUTURE]` |
| `PRD-MOB-001` | Trainee Self-Service Mobile Application | `[FUTURE]` |
