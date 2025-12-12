# Nextstay - Hotel Booking API

A modern, production-ready hotel booking management system built with FastAPI. Nextstay provides a comprehensive REST API for managing hotels, rooms, bookings, and user accounts with advanced features like caching, email notifications, and admin dashboard.

---

## 🌟 Features

- **User Management**
  - User registration and authentication with JWT tokens
  - Secure password hashing with bcrypt
  - Role-based access control

- **Hotel & Room Management**
  - Create, read, update, and delete hotels and rooms
  - Browse available hotels and rooms
  - Location-based hotel information (city-based filtering)

- **Booking System**
  - Create and manage bookings
  - View booking history
  - Automatic booking confirmation via email
  - Redis caching for improved performance

- **Admin Dashboard**
  - SQL Admin interface with authentication
  - Manage users, bookings, hotels, and rooms
  - Administrative control panel

- **Asynchronous Task Processing**
  - Celery integration for background jobs
  - Email notifications using SMTP
  - Task monitoring with Flower

- **Caching & Performance**
  - Redis-backed caching for optimized queries
  - Cache invalidation strategies
  - Improved API response times

- **Database Migrations**
  - Alembic for version control of database schema
  - Easy rollback and forward migrations

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.115.4
- **Server**: Uvicorn
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Async Driver**: asyncpg

### Authentication & Security
- **Password Hashing**: passlib with bcrypt
- **JWT Tokens**: python-jose with cryptography
- **Session Management**: Starlette SessionMiddleware

### Caching & Task Processing
- **Cache**: Redis
- **Task Queue**: Celery
- **Task Monitoring**: Flower

### Admin & Migrations
- **Admin Dashboard**: SQLAdmin
- **Database Migrations**: Alembic

### Data Validation
- **Schema Validation**: Pydantic V2
- **Settings Management**: Pydantic Settings

---

## 📋 Requirements

- Python 3.9+
- PostgreSQL database
- Redis server
- SMTP server for email notifications

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/AkromAbdaliev/Nextstay
cd Nextstay
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_db_user
DB_PASS=your_db_password
DB_NAME=nextstay_db

# Email Configuration (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# Security
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
```

### 5. Setup Database
```bash
# Create database
createdb nextstay_db

# Run migrations
alembic upgrade head
```

### 6. Start Redis Server
```bash
redis-server
```

### 7. Start Celery Worker (in a separate terminal)
```bash
celery -A app.tasks.celery worker --loglevel=info
```

### 8. Start the Application
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

---

## 📖 API Documentation

Once the server is running, interactive API documentation is available at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

| Endpoint                          | HTTP Method | Path                                      | Description                                             | User Type       |
|-----------------------------------|-------------|-------------------------------------------|---------------------------------------------------------|-----------------|
| Register User                     | POST        | `/auth/register`                           | Register a new user                                     | Public          |
| User Login                        | POST        | `/auth/login`                              | Authenticate user and return access token               | Public          |
| User Logout                       | POST        | `/auth/logout`                             | Logout user (deletes auth cookie)                       | Authenticated   |
| Get My Profile                    | GET         | `/auth/me`                                 | Get authenticated user's profile                        | Authenticated   |
| List Users                        | GET         | `/auth/users`                              | Get a list of all users (management)                    | Admin           |
| Get User By ID                    | GET         | `/auth/users/{user_id}`                    | Get details of a specific user by ID                    | Admin           |
| Create User (Admin)               | POST        | `/auth/users`                              | Create a new user (admin/management)                    | Admin           |
| Update User By ID (Admin)         | PUT         | `/auth/users/{user_id}`                    | Update user details by ID                               | Admin           |
| Delete User By ID (Admin)         | DELETE      | `/auth/users/{user_id}`                    | Delete a specific user by ID                            | Admin           |
| Get Hotels                        | GET         | `/hotels/`                                 | Retrieve list of hotels                                 | Public          |
| Get Hotel By ID                   | GET         | `/hotels/{hotel_id}`                       | Retrieve hotel details by ID                            | Public          |
| Create Hotel                      | POST        | `/hotels/`                                 | Create a new hotel                                      | Admin           |
| Update Hotel By ID                | PUT         | `/hotels/{hotel_id}`                       | Update hotel details by ID                              | Admin           |
| Delete Hotel By ID                | DELETE      | `/hotels/{hotel_id}`                       | Delete a hotel by ID                                    | Admin           |
| Get Available Rooms (Now)         | GET         | `/rooms/available?hotel_id={hotel_id}`     | Get currently available rooms for a hotel               | Public          |
| Get Available Rooms (Period)      | GET         | `/rooms/available/period`                  | Get available rooms for a hotel between two dates       | Public          |
| List Rooms                        | GET         | `/rooms/rooms?hotel_id={hotel_id}`         | Get all rooms for a hotel                               | Public          |
| Create Room                       | POST        | `/rooms/rooms?hotel_id={hotel_id}`         | Create a new room for a hotel                           | Admin           |
| Update Room By ID                 | PUT         | `/rooms/{room_id}`                         | Update details of a specific room                       | Admin           |
| Delete Room By ID                 | DELETE      | `/rooms/{room_id}`                         | Delete a specific room                                  | Admin           |
| List Bookings                     | GET         | `/bookings`                                | Get bookings for the authenticated user                 | Authenticated   |
| Get Booking By ID                 | GET         | `/bookings/{booking_id}`                   | Retrieve a specific booking (owner only)                | Authenticated   |
| Create Booking                    | POST        | `/bookings`                                | Create a new booking (sends confirmation email)         | Authenticated   |
| Update Booking By ID              | PUT         | `/bookings/{booking_id}`                   | Update a booking (owner only)                           | Authenticated   |
| Delete Booking By ID              | DELETE      | `/bookings/{booking_id}`                   | Cancel/delete a booking (owner only)                    | Authenticated   |
| Admin Dashboard                   | GET         | `/admin`                                   | SQLAdmin administrative dashboard                       | Admin           |
| Swagger UI                        | GET         | `/docs`                                    | Swagger UI for API documentation                        | Public          |
| Swagger JSON (without UI)         | GET         | `/openapi.json`                            | OpenAPI JSON for API documentation without UI           | Public          |
| ReDoc UI                          | GET         | `/redoc`                                   | ReDoc UI for API documentation                          | Public          |

---

## 🏗️ Project Structure

```
Nextstay/
├── app/
│   ├── admin/                 # Admin dashboard configuration
│   │   ├── auth.py           # Admin authentication
│   │   └── views.py          # Admin views
│   ├── bookings/             # Booking module
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── router.py         # API endpoints
│   │   ├── schemas.py        # Pydantic schemas
│   │   └── service.py        # Business logic
│   ├── core/                 # Core application setup
│   │   ├── config.py         # Configuration settings
│   │   ├── database.py       # Database connection
│   │   ├── exceptions.py     # Custom exceptions
│   │   └── admin_view.py     # Admin view configurations
│   ├── hotels/               # Hotels module
│   │   ├── models.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   └── service.py
│   ├── rooms/                # Rooms module
│   │   ├── models.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   └── service.py
│   ├── users/                # Users & Authentication module
│   │   ├── auth.py           # JWT and password utilities
│   │   ├── dependencies.py   # Dependency injection
│   │   ├── models.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   └── service.py
│   ├── tasks/                # Celery tasks
│   │   ├── celery.py         # Celery configuration
│   │   ├── email.py          # Email sending logic
│   │   └── tasks.py          # Task definitions
│   ├── services/             # Shared services
│   │   └── base.py           # Base service class
│   └── main.py               # Application entry point
├── migrations/               # Alembic database migrations
├── alembic.ini               # Alembic configuration
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. To use protected endpoints:

1. **Register a User**
   ```bash
   POST /auth/register
   Content-Type: application/json

   {
     "email": "user@example.com",
     "password": "your_password"
   }
   ```

2. **Login**
   ```bash
   POST /auth/login
   Content-Type: application/x-www-form-urlencoded

   username=user@example.com&password=your_password
   ```

3. **Use Token**
   Include the access token in the Authorization header:
   ```
   Authorization: Bearer <your_access_token>
   ```

---

## 📧 Email Notifications

Booking confirmations are automatically sent via email using Celery. Configure your SMTP settings in the `.env` file for email functionality to work properly.

---

## 🗄️ Database Migrations

### Create a New Migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback Migrations
```bash
alembic downgrade -1
```

---

## 🧪 Testing

(Add testing instructions if tests are implemented)

---

## 📊 Monitoring

### Celery Task Monitoring
Monitor Celery tasks with Flower:
```bash
celery -A app.tasks.celery flower
```
Flower UI will be available at `http://localhost:5555`

---

## 🚨 Error Handling

The API returns standardized error responses with appropriate HTTP status codes:

- **400**: Bad Request - Invalid input data
- **401**: Unauthorized - Invalid or missing credentials
- **404**: Not Found - Resource not found
- **409**: Conflict - Resource already exists
- **500**: Internal Server Error

---

## 🔄 Caching Strategy

The API uses Redis for caching:
- **Bookings list**: 120 seconds TTL
- Other frequently accessed data can be cached based on business requirements

---

## 🛡️ Security Considerations

- All passwords are hashed with bcrypt
- JWT tokens with expiration
- SMTP credentials stored in environment variables
- Database credentials never hardcoded
- CORS and middleware security configured

---

## 📝 Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DB_HOST` | Database hostname | localhost |
| `DB_PORT` | Database port | 5432 |
| `DB_USER` | Database user | postgres |
| `DB_PASS` | Database password | password123 |
| `DB_NAME` | Database name | nextstay_db |
| `SMTP_HOST` | SMTP server | smtp.gmail.com |
| `SMTP_PORT` | SMTP port | 587 |
| `SMTP_USER` | SMTP username | your_email@gmail.com |
| `SMTP_PASS` | SMTP password | app_password |
| `REDIS_HOST` | Redis hostname | localhost |
| `REDIS_PORT` | Redis port | 6379 |
| `SECRET_KEY` | JWT secret key | your_secret_key |
| `ALGORITHM` | JWT algorithm | HS256 |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📞 Support

For issues and questions, please open an issue on the repository or contact the development team.

---

## 🎯 Roadmap

- [ ] Unit and integration tests
- [ ] WebSocket support for real-time notifications
- [ ] Payment gateway integration
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Mobile app integration

---

**Built with ❤️ using FastAPI**
