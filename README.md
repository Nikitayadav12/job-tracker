# Job Application Tracker API

A REST API built with Django REST Framework to track job applications, statuses, and notes.

## Tech Stack

- Python 3.13, Django 6.0, Django REST Framework
- JWT Authentication (djangorestframework-simplejwt)
- PostgreSQL (production) / SQLite (local dev)
- pytest (15 tests, 100% passing)
- Swagger/OpenAPI docs (drf-spectacular)
- Docker

## Features

- User registration and JWT login
- Full CRUD for job applications
- Status tracking: Applied → Screening → Interview → Offer → Rejected → Withdrawn
- Notes per application
- Filter by status, company, role, date
- Dashboard summary (counts by status)
- Auto-generated Swagger UI docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register/ | Register new user |
| POST | /api/auth/login/ | Login, get JWT tokens |
| POST | /api/auth/token/refresh/ | Refresh access token |
| GET | /api/auth/profile/ | Get current user profile |
| GET | /api/applications/ | List all applications (filterable) |
| POST | /api/applications/ | Create new application |
| GET | /api/applications/{id}/ | Get single application |
| PUT/PATCH | /api/applications/{id}/ | Update application |
| DELETE | /api/applications/{id}/ | Delete application |
| GET | /api/applications/{id}/notes/ | List notes |
| POST | /api/applications/{id}/notes/ | Add note |
| DELETE | /api/applications/{id}/notes/{nid}/ | Delete note |
| GET | /api/dashboard/summary/ | Status counts summary |
| GET | /api/schema/swagger-ui/ | Swagger UI |

## Setup (Local)

```bash
git clone https://github.com/Nikitayadav12/job-tracker.git
cd job-tracker
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env         # add your SECRET_KEY
python manage.py migrate
python manage.py runserver
```

## Run Tests

```bash
pytest -v
```

## Project Structure

```
job_tracker/
├── config/          # Django settings, urls
├── accounts/        # Custom user, auth endpoints
├── applications/    # Job applications, notes, filters
├── dashboard/       # Summary stats endpoint
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
└── requirements.txt
![Swagger UI](swagger_screenshot.png)
```
