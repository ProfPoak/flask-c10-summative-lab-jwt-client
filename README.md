# Personal Journal API

A secure Flask REST API for a personal journaling app. Users can sign up, log in, and create private journal entries that only they can view, edit, or delete. Authentication is handled with JWT, and passwords are hashed with Bcrypt — no user can ever see or modify another user's entries. The included client is only for testing Auth routes and does not include any journal functionality.

## Features

- User registration and login with hashed passwords (Flask-Bcrypt)
- JWT-based authentication (Flask-JWT-Extended)
- Full CRUD for journal entries, scoped to the logged-in user
- Paginated journal entry index
- Route protection: all journal endpoints require a valid JWT, and every query is filtered by the requesting user's ID

## Tech Stack

- Flask
- Flask-RESTful
- Flask-SQLAlchemy
- Flask-Migrate (Alembic)
- Flask-Bcrypt
- Flask-JWT-Extended
- SQLite

## Installation

1. Clone the repository and move into the project folder:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. Install dependencies with Pipenv:
   ```bash
   pipenv install
   pipenv shell
   ```

3. Move into the `server` directory:
   ```bash
   cd server
   ```

4. Set up the database:
   ```bash
   flask db upgrade
   ```

5. Seed the database with sample users and journal entries:
   ```bash
   python seed.py
   ```

## Running the App

Start the Flask server:
```bash
python app.py
```

The API will be available at `http://localhost:5555`.

## Authentication

This API uses **JWT** (JSON Web Tokens) for authentication. After signing up or logging in, you'll receive a `token`. Include it on all protected requests as a header:

```
Authorization: Bearer <your-token>
```

## API Endpoints

### Auth

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/signup` | Creates a new user with a username and password. Returns a JWT and the new user on success. | No |
| `POST` | `/login` | Authenticates a user by username and password. Returns a JWT and the user on success. | No |
| `GET` | `/check_session` | Returns the currently logged-in user based on the JWT. | Yes |

### Journal Entries

All journal endpoints require a valid JWT and are automatically scoped to the logged-in user — you can only view, update, or delete your own entries.

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/journal` | Returns a paginated list of the logged-in user's journal entries, newest first. Accepts optional `page` and `per_page` query parameters. | Yes |
| `POST` | `/journal` | Creates a new journal entry for the logged-in user. Requires `title` and `entry` in the request body. The entry date is set automatically by the server. | Yes |
| `PATCH` | `/journal/<id>` | Updates the `title` and/or `entry` fields of a journal entry owned by the logged-in user. Returns a 404 if the entry doesn't exist or belongs to another user. | Yes |
| `DELETE` | `/journal/<id>` | Deletes a journal entry owned by the logged-in user. Returns a 404 if the entry doesn't exist or belongs to another user. | Yes |

### Example: Creating a Journal Entry

```
POST /journal
Authorization: Bearer <your-token>
Content-Type: application/json

{
  "title": "A good day",
  "entry": "Today I finally got the auth flow working."
}
```

### Example: Paginated Index

```
GET /journal?page=1&per_page=5
Authorization: Bearer <your-token>
```

Response:
```json
{
  "entries": [ ... ],
  "page": 1,
  "per_page": 5,
  "total_pages": 4,
  "total_entries": 18,
  "has_next": true,
  "has_prev": false
}
```

## Project Structure

```
server/
├── app.py                  # API routes and resources
├── config.py                # Flask app, database, and extension configuration
├── models.py                 # SQLAlchemy models and Marshmallow schemas
├── seed.py                   # Seeds the database with sample data
└── migrations/                # Flask-Migrate/Alembic migration files
```
