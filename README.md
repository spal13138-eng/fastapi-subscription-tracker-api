![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)

# Subscription Tracker API

A real-world backend API built with FastAPI for managing user subscriptions such as Netflix, Spotify, gym memberships, cloud services, and more.

This project allows users to register, log in, manage subscriptions, track renewals, filter data, search subscriptions, and monitor upcoming expirations.

---

## Features

* User Registration
* User Login with JWT Authentication
* Password Hashing using bcrypt
* Protected Routes
* Create Subscription
* Get All Subscriptions
* Get Subscription By ID
* Update Subscription
* Delete Subscription
* Search Subscription By Name
* Filter By Category
* Filter By Status
* Pagination Support
* Upcoming Renewals
* Automatic End Date Calculation
* Billing Cycle Support
* User-Specific Subscriptions

---

## Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* JWT Authentication
* Passlib + bcrypt
* Alembic
* Uvicorn

---

## Project Structure

```text
app/
├── routers/
├── models/
├── schemas/
├── database/
├── oauth2/
├── utils/
├── config/
├── main.py
```

---

## Database Models

### User

* id
* email
* password
* created_at

### Subscription

* id
* name
* category
* amount
* billing_cycle
* start_date
* end_date
* status
* reminder
* created_at
* updated_at
* owner_id

---

## API Endpoints

### Authentication

* POST `/users` → Register User
* POST `/login` → Login User

### Subscriptions

* POST `/subscriptions` → Create Subscription
* GET `/subscriptions` → Get All Subscriptions
* GET `/subscriptions/{id}` → Get Subscription By ID
* PUT `/subscriptions/{id}` → Update Subscription
* DELETE `/subscriptions/{id}` → Delete Subscription

### Filters and Search

* GET `/subscriptions?limit=10&skip=0` → Pagination
* GET `/subscriptions/search?name=netflix` → Search By Name
* GET `/subscriptions?category=Entertainment` → Filter By Category
* GET `/subscriptions?status=active` → Filter By Status
* GET `/subscriptions/upcoming-renewals` → Get Upcoming Renewals

---

## Billing Cycle Logic

The API automatically calculates `end_date` based on `billing_cycle`.

* Monthly → 30 days
* Quarterly → 90 days
* Yearly → 365 days
* Weekly → 7 days

Example:

```python
start_date = datetime.utcnow().date()

if billing_cycle == "monthly":
    end_date = start_date + timedelta(days=30)
```

---

## Authentication Flow

1. User registers with email and password
2. Password is hashed before storing in database
3. User logs in using email and password
4. Backend returns JWT access token
5. User sends token in Authorization header
6. Protected routes verify token before allowing access

Example Header:

```text
Authorization: Bearer your_jwt_token
```

---

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd subscription-tracker-api
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/subscription_tracker
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 6. Run the Server

```bash
uvicorn app.main:app --reload
```

---

## API Documentation

FastAPI automatically generates Swagger UI documentation.

* Swagger Docs: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

---

## Future Improvements

* Email Reminder System
* Dashboard Analytics
* CSV Export
* Docker Support
* Deployment
* Frontend Integration
* Role-Based Access Control

---

## Author

Built by Shiva as a real-world backend project for learning FastAPI, authentication, databases, and API development.
