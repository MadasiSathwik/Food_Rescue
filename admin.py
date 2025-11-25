from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import User, Donation, db
from functools import wraps
from sqlalchemy import func   # 🔹 NEW: for aggregation (counts, top lists)

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required', 'danger')
            return redirect(url_for('dashboard'))  # global /dashboard route
        return f(*args, **kwargs)
    return decorated_function


# 🧍 All users list (already good)
@admin_bp.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/users.html', users=users)


# 🍱 All donations list (with filter)
@admin_bp.route('/donations')
@login_required
@admin_required
def donations():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')
    
    query = Donation.query
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    donations = query.order_by(Donation.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template(
        'admin/donations.html',
        donations=donations,
        status_filter=status_filter
    )


# ✅ Update donation status (already good)
@admin_bp.route('/donation/<int:id>/update_status', methods=['POST'])
@login_required
@admin_required
def update_donation_status(id):
    donation = Donation.query.get_or_404(id)
    new_status = request.form.get('status')
    
    if new_status in ['active', 'claimed', 'completed', 'removed']:
        donation.status = new_status
        db.session.commit()
        flash(f'Donation status updated to {new_status}', 'success')
    else:
        flash('Invalid status', 'danger')
    
    return redirect(url_for('admin.donations'))


# 📊 NEW: Admin stats page – NGOs, restaurants, orders given/taken
@admin_bp.route('/stats')
@login_required
@admin_required
def stats():
    # Overall counts
    total_users = User.query.count()
    total_restaurants = User.query.filter_by(role='restaurant').count()
    total_ngos = User.query.filter_by(role='ngo').count()

    total_donations = Donation.query.count()
    active_donations = Donation.query.filter_by(status='active').count()
    claimed_donations = Donation.query.filter_by(status='claimed').count()
    completed_donations = Donation.query.filter_by(status='completed').count()

    # Top 5 restaurants by number of donations given
    top_restaurants = (
        db.session.query(
            User,
            func.count(Donation.id).label('donations_given')
        )
        .join(Donation, Donation.restaurant_id == User.id)
        .filter(User.role == 'restaurant')
        .group_by(User.id)
        .order_by(func.count(Donation.id).desc())
        .limit(5)
        .all()
    )

    # Top 5 NGOs by number of donations taken
    top_ngos = (
        db.session.query(
            User,
            func.count(Donation.id).label('donations_taken')
        )
        .join(Donation, Donation.claimed_by_id == User.id)
        .filter(User.role == 'ngo')
        .group_by(User.id)
        .order_by(func.count(Donation.id).desc())
        .limit(5)
        .all()
    )

    return render_template(
        'admin/stats.html',
        total_users=total_users,
        total_restaurants=total_restaurants,
        total_ngos=total_ngos,
        total_donations=total_donations,
        active_donations=active_donations,
        claimed_donations=claimed_donations,
        completed_donations=completed_donations,
        top_restaurants=top_restaurants,
        top_ngos=top_ngos,
    )
