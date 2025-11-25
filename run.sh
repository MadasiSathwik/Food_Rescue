#!/bin/bash

# Food Wastage Reduction App - Run Script

echo "Setting up Food Wastage Reduction App..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Create uploads directory
mkdir -p static/uploads

# Initialize database with sample data
echo "Initializing database..."
python create_db.py

# Set environment variables
export FLASK_ENV=development
export SECRET_KEY=dev-secret-key-change-this

echo "Starting Flask application..."
echo "Visit http://localhost:5000 in your browser"
echo ""
echo "Sample login credentials:"
echo "- Admin: admin@example.com / admin123"
echo "- Restaurant: restaurant@example.com / restaurant123"
echo "- NGO: ngo@example.com / ngo123"
echo ""

python app.py