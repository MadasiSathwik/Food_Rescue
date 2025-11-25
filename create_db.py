#!/usr/bin/env python3
from app import create_app
from models import db, User, Donation
from datetime import datetime, timedelta

def create_sample_data():
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        
        # Create admin user
        admin = User(name='Admin User', email='admin@example.com', role='admin')
        admin.set_password('admin123')
        
        # Create sample restaurant
        restaurant = User(name='Green Restaurant', email='restaurant@example.com', role='restaurant')
        restaurant.set_password('restaurant123')
        
        # Create sample NGO
        ngo = User(name='Food Help NGO', email='ngo@example.com', role='ngo')
        ngo.set_password('ngo123')
        
        db.session.add_all([admin, restaurant, ngo])
        db.session.commit()
        
        # Create sample donations
        now = datetime.now()
        
        donation1 = Donation(
            restaurant_id=restaurant.id,
            title='Fresh Vegetables and Fruits',
            description='We have excess fresh vegetables and fruits from our daily prep. Includes carrots, lettuce, tomatoes, and seasonal fruits.',
            food_type='Fresh Produce',
            quantity='10-15 kg',
            address='123 Green Street, Downtown',
            pickup_time=now + timedelta(hours=1),
            expiry_time=now + timedelta(days=1),
            status='active'
        )
        
        donation2 = Donation(
            restaurant_id=restaurant.id,
            title='Prepared Sandwiches',
            description='Freshly made sandwiches that were prepared for a cancelled event. Still good for several hours.',
            food_type='Prepared Food',
            quantity='20 sandwiches',
            address='123 Green Street, Downtown',
            pickup_time=now + timedelta(minutes=30),
            expiry_time=now + timedelta(hours=6),
            status='active'
        )
        
        donation3 = Donation(
            restaurant_id=restaurant.id,
            title='Bakery Items - End of Day',
            description='Bread, pastries, and baked goods from today. Perfect for distribution before expiry.',
            food_type='Baked Goods',
            quantity='30 items approx',
            address='123 Green Street, Downtown',
            pickup_time=now + timedelta(hours=2),
            expiry_time=now + timedelta(hours=12),
            status='active'
        )
        
        db.session.add_all([donation1, donation2, donation3])
        db.session.commit()
        
        print("Database created successfully!")
        print("\nSample login credentials:")
        print("Admin: admin@example.com / admin123")
        print("Restaurant: restaurant@example.com / restaurant123")
        print("NGO: ngo@example.com / ngo123")
        print("\nSample donations have been created.")

if __name__ == '__main__':
    create_sample_data()