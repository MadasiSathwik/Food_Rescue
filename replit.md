# Food Wastage Reduction App

## Overview

A Flask-based web application that connects restaurants with NGOs to reduce food waste and fight hunger. The platform enables restaurants to donate surplus food, NGOs to browse and claim donations, and administrators to manage the entire ecosystem. The system includes role-based access control, real-time donation tracking, and a comprehensive admin panel for platform oversight.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Web Framework & Structure
- **Framework**: Flask 2.3.3 with Blueprint-based modular architecture
- **Rationale**: Chosen for lightweight, flexible web development with clear separation of concerns
- **Key Blueprints**:
  - `auth_bp`: Handles user authentication (login, registration, logout)
  - `donations_bp`: Manages donation lifecycle (create, browse, claim, complete)
  - `admin_bp`: Administrative functions (user management, donation oversight, statistics)

### Authentication & Authorization
- **Implementation**: Flask-Login for session management with role-based access control
- **Password Security**: Werkzeug's password hashing (generate_password_hash/check_password_hash)
- **User Roles**: Three-tier system (restaurant, ngo, admin)
- **Rationale**: Flask-Login provides simple integration with Flask's request context while maintaining security best practices

### Database Layer
- **ORM**: SQLAlchemy (Flask-SQLAlchemy 3.0.5)
- **Database**: Neon PostgreSQL (production-ready serverless PostgreSQL)
- **Connection**: Via DATABASE_URL environment variable stored in Replit secrets
- **Connection Pool Settings**:
  - `pool_recycle`: 300 seconds (handles connection timeouts)
  - `pool_pre_ping`: True (validates connections before use)
- **Data Models**:
  - `User`: Stores user credentials, role, and relationships to donations
  - `Donation`: Tracks food donations with status lifecycle (active → claimed → completed/removed)
- **Database Initialization**: Run `python create_db.py` to create tables and sample data
- **Rationale**: Neon PostgreSQL provides serverless, auto-scaling database with excellent performance and reliability

### Form Handling & Validation
- **Library**: Flask-WTF (WTForms 3.0.1) with CSRF protection
- **Email Validation**: email-validator library for robust email checking
- **File Upload**: Secure file handling with Werkzeug's `secure_filename` and UUID-based naming
- **Supported Formats**: JPG, PNG, JPEG images only
- **Rationale**: WTForms provides server-side validation with automatic CSRF token generation

### File Upload System
- **Storage**: Local filesystem under `static/uploads/`
- **Naming Strategy**: UUID prefix to prevent filename collisions
- **Image Processing**: Pillow 10.0.1 for potential image manipulation
- **Rationale**: Simple filesystem storage suitable for MVP; easily upgradeable to cloud storage (S3, Cloudinary) for production scale

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap 5.1.3 via CDN
- **Icons**: Bootstrap Icons 1.7.2
- **Responsive Design**: Mobile-first approach using Bootstrap's grid system
- **Rationale**: Bootstrap provides rapid UI development with minimal custom CSS

### Notification System
- **Current Implementation**: Console-based email backend (prints to terminal)
- **Future-Ready**: Commented Flask-Mail integration code prepared for SMTP
- **Rationale**: Console backend enables development/testing without SMTP configuration; easy swap to production email service

### Session & State Management
- **Session Storage**: Flask's secure cookie-based sessions
- **Secret Key**: Environment variable with fallback to development key
- **Login Persistence**: Flask-Login handles "remember me" functionality
- **Rationale**: Cookie-based sessions eliminate need for Redis/database session storage in early stages

### Pagination
- **Implementation**: SQLAlchemy's built-in pagination
- **Default Page Size**: 20 items per page
- **Rationale**: Prevents performance issues with large datasets while maintaining simple implementation

## External Dependencies

### Core Framework Dependencies
- **Flask 2.3.3**: Web framework
- **Werkzeug 2.3.7**: WSGI utilities and security helpers
- **Jinja2**: Template engine (bundled with Flask)

### Database & ORM
- **Flask-SQLAlchemy 3.0.5**: SQLAlchemy integration for Flask
- **Flask-Migrate 4.0.5**: Database migration tool (Alembic wrapper)
- **psycopg2-binary 2.9.9**: PostgreSQL adapter for production use

### Authentication & Forms
- **Flask-Login 0.6.3**: User session management
- **Flask-WTF 1.1.1**: Form handling with CSRF protection
- **WTForms 3.0.1**: Form validation library
- **email-validator 2.0.0**: Email address validation

### File Processing
- **Pillow 10.0.1**: Image processing library for upload handling

### Configuration Management
- **python-dotenv 1.0.0**: Environment variable management from .env files

### Frontend (CDN-based)
- **Bootstrap 5.1.3**: UI framework (no npm installation required)
- **Bootstrap Icons 1.7.2**: Icon library

### Future Integration Points
- **Email Service**: SMTP server or transactional email service (SendGrid, Mailgun, AWS SES)
- **Cloud Storage**: For production file uploads (AWS S3, Cloudinary, Google Cloud Storage)

### Current Configuration
- **Database**: Neon PostgreSQL with connection pooling (configured)
- **Email Backend**: Console-based for development
- **File Storage**: Local filesystem under `static/uploads/`
- **Environment Variables**: DATABASE_URL and SECRET_KEY stored in Replit secrets