from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from models import Donation, User, db
from forms import DonationForm
from werkzeug.utils import secure_filename
import os
import uuid

donations_bp = Blueprint('donations', __name__)

def send_notification_email(subject, recipient_email, message):
    """Console email backend - prints to console"""
    print(f"\n=== EMAIL NOTIFICATION ===")
    print(f"To: {recipient_email}")
    print(f"Subject: {subject}")
    print(f"Message: {message}")
    print(f"==========================\n")
    
    # For real SMTP, uncomment and configure:
    # from flask_mail import Message, Mail
    # msg = Message(subject, recipients=[recipient_email], body=message)
    # mail.send(msg)

@donations_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.role != 'restaurant':
        flash('Only restaurants can create donations', 'danger')
        return redirect(url_for('dashboard'))
    
    form = DonationForm()
    if form.validate_on_submit():
        donation = Donation(
            restaurant_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            food_type=form.food_type.data,
            quantity=form.quantity.data,
            address=form.address.data,
            pickup_time=form.pickup_time.data,
            expiry_time=form.expiry_time.data
        )
        
        # Handle image upload
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            upload_path = os.path.join('static', 'uploads', unique_filename)
            
            # Create uploads directory if it doesn't exist
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            
            form.image.data.save(upload_path)
            donation.image_path = unique_filename
        
        db.session.add(donation)
        db.session.commit()
        
        # Send notification to all NGOs
        ngos = User.query.filter_by(role='ngo').all()
        for ngo in ngos:
            send_notification_email(
                f"New Food Donation Available: {donation.title}",
                ngo.email,
                f"A new food donation is available from {current_user.name}.\n\n"
                f"Details:\n"
                f"- Food Type: {donation.food_type}\n"
                f"- Quantity: {donation.quantity}\n"
                f"- Pickup Address: {donation.address}\n"
                f"- Available Until: {donation.expiry_time}\n\n"
                f"Visit the platform to claim this donation."
            )
        
        flash('Donation posted successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('donations/create.html', form=form)

@donations_bp.route('/list')
@login_required
def list_donations():
    page = request.args.get('page', 1, type=int)
    filter_available = request.args.get('available', 'false') == 'true'
    location_filter = request.args.get('location', '')
    
    query = Donation.query.filter(Donation.status == 'active')
    
    if filter_available:
        query = query.filter(Donation.expiry_time > datetime.utcnow())
    
    if location_filter:
        query = query.filter(Donation.address.contains(location_filter))
    
    donations = query.order_by(Donation.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('donations/list.html', donations=donations, 
                         filter_available=filter_available, location_filter=location_filter)

@donations_bp.route('/<int:id>')
@login_required
def detail(id):
    donation = Donation.query.get_or_404(id)
    return render_template('donations/detail.html', donation=donation)

@donations_bp.route('/<int:id>/claim', methods=['POST'])
@login_required
def claim(id):
    if current_user.role != 'ngo':
        flash('Only NGOs can claim donations', 'danger')
        return redirect(url_for('donations.detail', id=id))
    
    donation = Donation.query.get_or_404(id)
    
    if donation.status != 'active':
        flash('This donation is no longer available', 'danger')
        return redirect(url_for('donations.detail', id=id))
    
    if not donation.is_available():
        flash('This donation has expired', 'danger')
        return redirect(url_for('donations.detail', id=id))
    
    donation.status = 'claimed'
    donation.claimed_by_id = current_user.id
    donation.claimed_at = datetime.utcnow()
    
    db.session.commit()
    
    # Send notification to restaurant
    send_notification_email(
        f"Your Donation Has Been Claimed: {donation.title}",
        donation.restaurant.email,
        f"Your food donation has been claimed by {current_user.name}.\n\n"
        f"NGO Contact: {current_user.email}\n"
        f"Claimed at: {donation.claimed_at}\n\n"
        f"Please coordinate the pickup with the NGO."
    )
    
    flash('Donation claimed successfully! The restaurant will be notified.', 'success')
    return redirect(url_for('donations.detail', id=id))

@donations_bp.route('/api/donations')
def api_donations():
    donations = Donation.query.filter_by(status='active').filter(
        Donation.expiry_time > datetime.utcnow()
    ).order_by(Donation.created_at.desc()).all()
    
    donations_data = []
    for donation in donations:
        donations_data.append({
            'id': donation.id,
            'title': donation.title,
            'description': donation.description,
            'food_type': donation.food_type,
            'quantity': donation.quantity,
            'address': donation.address,
            'pickup_time': donation.pickup_time.isoformat(),
            'expiry_time': donation.expiry_time.isoformat(),
            'restaurant_name': donation.restaurant.name,
            'created_at': donation.created_at.isoformat()
        })
    
    return jsonify({
        'donations': donations_data,
        'total': len(donations_data)
    })