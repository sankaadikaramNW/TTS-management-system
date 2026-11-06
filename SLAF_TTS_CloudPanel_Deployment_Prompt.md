# Deploy SLAF TTS Management Portal to CloudPanel

Act as a senior DevOps engineer. Deploy my existing SLAF Trade Training School (TTS) Management Portal to my Oracle Cloud VPS using CloudPanel.

## 1. Project Details

- **Local project path:** `F:\My projects\TTS management system`
- **Domain name:** `ttsmp.itwekala.com.lk`
- **VPS public IP:** `161.118.189.33`
- **Hosting panel:** CloudPanel
- **Frontend:** React / Vite
- **Backend:** Python / FastAPI
- **Database:** Identify the actual database configuration from the existing project.
- **Deployment configuration:** An existing `docker-compose.yml` is available in the project root.

## 2. Main Objective

Deploy the existing application to the VPS and make it accessible using:

`https://ttsmp.itwekala.com.lk`

Focus exclusively on application hosting and deployment. Do not investigate or troubleshoot the previously shown Cloudflare error unless it directly prevents testing the deployed application.

## 3. Inspect the Existing Project

Before making changes, inspect the following:

- `frontend/`
- `backend/`
- `database/`
- `docs/`
- `.env`
- `.env.example`
- `docker-compose.yml`
- `README.md`
- `implementation_plan.md`
- `package-lock.json`

Determine the correct frontend build command, FastAPI entry point, API prefix, database engine, required environment variables, file storage locations, and service dependencies.

Reuse the existing application architecture and configuration wherever possible. Do not rebuild the project from scratch or remove existing functionality.

## 4. Prepare the Production Environment

Using the existing CloudPanel installation:

1. Verify that the VPS and required services are accessible.
2. Configure the website for `ttsmp.itwekala.com.lk`.
3. Select an appropriate document root for the production frontend.
4. Prepare the backend as a persistent production service or use the existing Docker Compose architecture if suitable.
5. Configure NGINX or CloudPanel's supported routing to serve the frontend and forward API requests to FastAPI.
6. Configure the production database according to the actual project configuration.
7. Configure the production environment variables securely.
8. Ensure uploaded documents and other required application files are preserved.

Do not assume CloudPanel manages Docker directly. Check the existing server configuration and choose a compatible deployment method.

## 5. Frontend Deployment

- Install frontend dependencies using the existing lockfile.
- Run the appropriate production build.
- Deploy the generated files to the website document root.
- Configure the frontend to use the production backend API.
- Ensure React/Vite client-side routes work after refreshing a page.
- Do not expose the Vite development server in production.

## 6. Backend Deployment

- Identify the actual FastAPI application entry point.
- Install the required Python dependencies in an isolated environment or the existing Docker environment.
- Run FastAPI using a suitable production ASGI server.
- Configure it to restart automatically after a server reboot.
- Keep the backend listening on an appropriate private interface or internal port.
- Route public API requests through NGINX.
- Configure CORS and environment variables for the production domain.
- Check application logs for startup and database errors.

## 7. Database and Existing Data

- Identify whether the application uses SQLite, MySQL, or another database.
- Review `docker-compose.yml` and backend database settings.
- Preserve existing application data and relationships.
- Back up the database before performing migrations or deployment changes.
- Do not delete, reset, or recreate the existing production database.
- Keep database credentials out of source control and public directories.
- Ensure database data persists when services restart.

## 8. Production URL and Routing

Configure the application so that:

- `https://ttsmp.itwekala.com.lk/` serves the frontend.
- `https://ttsmp.itwekala.com.lk/api/` routes to the backend, adjusted to match the actual API prefix in the code.
- Static assets load correctly.
- Frontend navigation and page refreshes work.
- Existing authentication, role-based permissions, and protected endpoints continue to work.

Use the domain already provided. Do not register a new domain or create an unnecessary replacement website.

## 9. Deployment Safety

- Back up existing configuration and database files before changing them.
- Do not overwrite unrelated websites hosted on the VPS.
- Do not expose database ports or production secrets.
- Avoid unnecessary framework, package, or database upgrades.
- Do not delete source files, uploaded documents, or existing records.
- Ask for approval before destructive operations or changes that could cause significant downtime.

## 10. Testing and Completion

After deployment, verify:

1. The frontend production build succeeds.
2. The website files are served by CloudPanel.
3. The FastAPI backend starts successfully.
4. The backend can connect to the configured database.
5. The frontend can communicate with the backend.
6. Login and role-based permissions work.
7. Existing trainees, academic records, and other data remain available.
8. Core modules work, including Academic Management, Parade State, Attendance, Examination Results, Course Calendar, Accommodation, and Reports.
9. Services restart correctly after a restart.
10. Logs contain no exposed passwords, tokens, or other secrets.

If HTTPS or domain routing prevents public testing, verify the application locally on the VPS and report the limitation separately. Do not spend time troubleshooting unrelated Cloudflare configuration.

## 11. Final Report

Provide a concise deployment report containing:

- Deployment method selected.
- CloudPanel website configuration.
- Frontend document root.
- Backend service and internal port.
- Database engine and persistence configuration.
- Production API URL.
- Environment variables that must be configured, without revealing their secret values.
- Backup location.
- Commands used to start, stop, restart, and inspect logs.
- Tests completed and any remaining actions.

**Success criteria:** The existing SLAF TTS Management Portal is deployed on the Oracle Cloud VPS, managed through CloudPanel, and ready to use through the provided domain once domain routing is available.
