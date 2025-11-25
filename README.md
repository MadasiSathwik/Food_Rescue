# Food Wastage Reduction App

A complete web application built with Flask that connects restaurants with NGOs to reduce food waste and fight hunger. Restaurants can donate surplus food, NGOs can claim donations, and admins can manage the platform.

## Project Structure

```
food-wastage-app/
├── app.py                 # Main Flask application
├── models.py              # Database models (User, Donation)
├── forms.py               # WTForms for validation
├── auth.py                # Authentication blueprint
├── donations.py           # Donations management blueprint
├── admin.py               # Admin panel blueprint
├── create_db.py           # Database initialization script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── run.sh                # Setup and run script
├── static/
│   ├── css/custom.css    # Custom styles
│   └── uploads/          # Uploaded images directory
└── templates/            # Jinja2 HTML templates
    ├── base.html         # Base template with navbar
    ├── index.html        # Home page
    ├── auth/             # Authentication templates
    ├── donations/        # Donation-related templates
    ├── dashboard/        # Role-specific dashboards
    └── admin/            # Admin panel templates
```

## Features

### User Roles

- **Restaurant**: Create and manage food donation posts
- **NGO**: Browse, filter, and claim available donations
- **Admin**: Manage users and donations, view platform statistics

### Core Functionality

- User registration and login with role selection
- Password hashing and secure authentication
- Food donation creation with image upload
- Donation browsing with filters (location, availability)
- Donation claiming system
- Email notifications (console backend included)
- Admin panel for platform management
- REST API endpoint for donations data

### Security Features

- Form validation with Flask-WTF
- Password hashing with Werkzeug
- Role-based access control
- CSRF protection
- File upload validation

## Setup Instructions

### 1. Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### 2. Quick Setup (using run.sh)

```bash
chmod +x run.sh
./run.sh
```

### 3. Manual Setup

#### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Set Environment Variables

```bash
cp .env.example .env
# Edit .env file with your configurations
export FLASK_ENV=development
export SECRET_KEY=your-secret-key-here
```

#### Initialize Database

```bash
python create_db.py
```

#### Create Upload Directory

```bash
mkdir -p static/uploads
```

#### Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Demo Accounts

After running `create_db.py`, you can login with these accounts:

- **Admin**: admin@example.com / admin123
- **Restaurant**: restaurant@example.com / restaurant123
- **NGO**: ngo@example.com / ngo123

## API Documentation

### GET /donations/api/donations

Returns active donations in JSON format.

**Response:**

```json
{
  "donations": [
    {
      "id": 1,
      "title": "Fresh Vegetables",
      "description": "Surplus vegetables from daily prep",
      "food_type": "Fresh Produce",
      "quantity": "10-15 kg",
      "address": "123 Green Street, Downtown",
      "pickup_time": "2024-01-15T10:00:00",
      "expiry_time": "2024-01-16T18:00:00",
      "restaurant_name": "Green Restaurant",
      "created_at": "2024-01-15T09:00:00"
    }
  ],
  "total": 1
}
```

### Sample API Calls

```bash
# Get all active donations
curl -X GET http://localhost:5000/donations/api/donations

# With authentication (if needed)
curl -X GET http://localhost:5000/donations/api/donations \
  -H "Content-Type: application/json"
```

## Email Configuration

### Console Backend (Default)

By default, emails are printed to the console. Check your terminal for email notifications when:

- A new donation is created (sent to all NGOs)
- A donation is claimed (sent to the restaurant)

### SMTP Configuration (Optional)

To use real email delivery, uncomment and configure these environment variables in `.env`:

```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

Then uncomment the SMTP code in `donations.py` in the `send_notification_email` function.

## Testing Guide

### Manual Testing Steps

1. **User Registration & Login**

   ```
   - Visit http://localhost:5000
   - Click "Register" and create restaurant account
   - Create NGO account with different email
   - Test login with both accounts
   ```

2. **Restaurant Workflow**

   ```
   - Login as restaurant user
   - Click "Create New Donation"
   - Fill form with food details and image
   - Submit and verify donation appears on dashboard
   - Check console for email notifications to NGOs
   ```

3. **NGO Workflow**

   ```
   - Login as NGO user
   - Browse available donations
   - Use filters (location, available now)
   - Click "View Details" on a donation
   - Claim the donation
   - Check console for email to restaurant
   - Verify donation shows as "claimed" status
   ```

4. **Admin Functions**

   ```
   - Login as admin user
   - Visit "Manage Users" to see all registered users
   - Visit "Manage Donations" to see all donations
   - Change donation status using dropdown
   - View platform statistics on dashboard
   ```

5. **API Testing**

   ```bash
   # Test the REST API
   curl -X GET http://localhost:5000/donations/api/donations

   # Should return JSON with active donations
   ```

### Expected Behaviors

- ✅ Passwords are hashed (not stored in plain text)
- ✅ Users can only access features for their role
- ✅ Email notifications appear in console
- ✅ Expired donations show "Expired" status
- ✅ Claimed donations cannot be claimed again
- ✅ Image uploads work and display correctly
- ✅ Forms validate input server-side
- ✅ API returns proper JSON response

## Database Schema

### Users Table

- `id`: Primary key
- `name`: User's full name
- `email`: Unique email address
- `password_hash`: Hashed password
- `role`: 'restaurant', 'ngo', or 'admin'
- `created_at`: Registration timestamp

### Donations Table

- `id`: Primary key
- `restaurant_id`: Foreign key to User
- `title`: Donation title
- `description`: Detailed description
- `food_type`: Type of food
- `quantity`: Approximate quantity
- `address`: Pickup address
- `pickup_time`: When food is ready
- `expiry_time`: When food expires
- `image_path`: Optional uploaded image
- `status`: 'active', 'claimed', 'completed', 'removed'
- `claimed_by_id`: NGO that claimed (nullable)
- `claimed_at`: Claim timestamp
- `created_at`: Creation timestamp

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please create an issue in the repository or contact the development team.

---

**Built with ❤️ to reduce food waste and fight hunger in our communities.**
