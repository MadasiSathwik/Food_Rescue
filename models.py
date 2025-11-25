from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Basic details
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Role: 'restaurant', 'ngo', 'admin'
    role = db.Column(db.String(20), nullable=False)

    # Extra profile fields for NGOs / Restaurants
    organization_name = db.Column(db.String(150))  # e.g. "Robin Hood Army", "Domino's Madhapur"
    phone = db.Column(db.String(20))
    address = db.Column(db.String(300))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    # For restaurants: donations they created
    donations = db.relationship(
        'Donation',
        foreign_keys='Donation.restaurant_id',
        backref='restaurant',
        lazy='dynamic'
    )

    # For NGOs: donations they claimed
    claimed_donations = db.relationship(
        'Donation',
        foreign_keys='Donation.claimed_by_id',
        backref='claimed_by_ngo',
        lazy='dynamic'
    )

    # Password helpers
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # --- Stats helpers for your project ---

    @property
    def total_donations_given(self):
        """How many donations this user (restaurant) has created."""
        if self.role != 'restaurant':
            return 0
        return self.donations.count()

    @property
    def total_donations_taken(self):
        """How many donations this user (NGO) has claimed."""
        if self.role != 'ngo':
            return 0
        return self.claimed_donations.count()

    def __repr__(self):
        return f'<User {self.email} ({self.role})>'


class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Which restaurant created this donation
    restaurant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

    food_type = db.Column(db.String(100), nullable=False)  # e.g. "Veg", "Non-veg", "Snacks"
    quantity = db.Column(db.String(100), nullable=False)   # e.g. "20 plates", "10 boxes"

    address = db.Column(db.String(300), nullable=False)

    pickup_time = db.Column(db.DateTime, nullable=False)
    expiry_time = db.Column(db.DateTime, nullable=False)

    image_path = db.Column(db.String(300), nullable=True)

    # 'active', 'claimed', 'completed', 'removed'
    status = db.Column(db.String(20), default='active')

    # Which NGO claimed this donation (if any)
    claimed_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    claimed_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_available(self):
        return self.status == 'active' and datetime.utcnow() < self.expiry_time

    def time_left(self):
        if datetime.utcnow() > self.expiry_time:
            return "Expired"
        
        delta = self.expiry_time - datetime.utcnow()
        total_seconds = delta.total_seconds()
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        
        if hours > 24:
            days = hours // 24
            return f"{int(days)} days left"
        elif hours >= 1:
            return f"{int(hours)} hours left"
        else:
            return f"{int(minutes)} minutes left"

    def __repr__(self):
        return f'<Donation {self.title}>'
