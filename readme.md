#  Board Backend API

A Django REST Framework based backend for the **Board** application. This project provides secure authentication, user management, board management, image uploads, and REST APIs that can be consumed by a frontend such as Next.js or React.

---

#  Tech Stack

- Python 3
- Django 6
- Django REST Framework
- JWT Authentication (Simple JWT)
- Social Authentication (Google OAuth)
- SQLite (Development)
- Pillow (Image Processing)
- CORS Headers
- WhiteNoise (Static Files)
- PythonAnywhere / Vercel Ready

---

#  Features

##  Authentication

- User Registration
- User Login
- JWT Access Token
- JWT Refresh Token
- User Logout
- Get Current User (`/auth/me`)
- Google Social Login

---

##  User Management

- User Profile
- Avatar Upload
- Profile Update

---

##  Board Management

- Create Board
- Update Board
- Delete Board
- View All Boards
- View Single Board

---

##  Media Support

- Avatar Image Upload
- Annotation/Image Storage
- Media File Serving

---

##  REST API

The backend exposes RESTful APIs that can be used by any frontend application such as:

- Next.js
- React
- Flutter
- Android
- iOS

---

#  Project Structure

```
board/
│
├── board/                 # Django Project Settings
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   ├── wsgi.py
│   └── asgi.py
│
├── boards/                # Main Application
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
│
├── media/
│   ├── avatars/
│   └── annotations/
│
├── staticfiles/
│
├── manage.py
└── requirements.txt
```

---

#  Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into project

```bash
cd board
```

Create Virtual Environment

```bash
python -m venv env
```

Activate Environment

### Windows

```bash
env\Scripts\activate
```

### Linux / macOS

```bash
source env/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Run Migrations

```bash
python manage.py migrate
```

Create Superuser

```bash
python manage.py createsuperuser
```

Run Development Server

```bash
python manage.py runserver
```

---

#  Main Dependencies

- Django
- Django REST Framework
- Simple JWT
- django-allauth
- social-auth-app-django
- Pillow
- django-cors-headers
- WhiteNoise

---

#  Authentication

This project uses **JWT Authentication**.

After login you will receive:

- Access Token
- Refresh Token

Include the access token in every protected request.

```
Authorization: Bearer <access_token>
```

---

#  Media Files

Uploaded files are stored inside:

```
media/
```

Including:

- User Avatars
- Annotation Images

---

#  Deployment

This backend can be deployed on:

- PythonAnywhere
- Render
- Railway
- VPS
- Docker
- AWS EC2

---

#  API Response Format

Successful Response

```json
{
    "success": true,
    "message": "Request successful",
    "data": {}
}
```

Error Response

```json
{
    "success": false,
    "message": "Something went wrong"
}
```

---

#  Developed With

- Django
- Django REST Framework
- Python

---

#  License
