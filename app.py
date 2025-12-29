import os
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user

from models import db, User, Donation
from auth import auth_bp
from donations import donations_bp
from admin import admin_bp


def create_app():
    app = Flask(__name__)

    # =========================
    # Configuration
    # =========================
    app.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY', 'dev-secret-key-change-this'
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'sqlite:///food_wastage.db'
    )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # =========================
    # Initialize extensions
    # =========================
    db.init_app(app)

    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # =========================
    # Register blueprints
    # =========================
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(donations_bp, url_prefix='/donations')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # =========================
    # Jinja2 filters
    # =========================
    @app.template_filter('time_left')
    def time_left_filter(donation):
        return donation.time_left()

    # =========================
    # Routes
    # =========================
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))

        recent_donations = (
            Donation.query
            .filter_by(status='active')
            .order_by(Donation.created_at.desc())
            .limit(6)
            .all()
        )
        return render_template('index.html', donations=recent_donations)

    @app.route('/dashboard')
    @login_required
    def dashboard():
        if current_user.role == 'restaurant':
            donations = (
                current_user.donations
                .order_by(Donation.created_at.desc())
                .limit(10)
                .all()
            )
            return render_template('dashboard/restaurant.html', donations=donations)

        elif current_user.role == 'ngo':
            available_donations = (
                Donation.query
                .filter_by(status='active')
                .order_by(Donation.created_at.desc())
                .limit(10)
                .all()
            )
            claimed_donations = (
                current_user.claimed_donations
                .order_by(Donation.claimed_at.desc())
                .limit(10)
                .all()
            )
            return render_template(
                'dashboard/ngo.html',
                available_donations=available_donations,
                claimed_donations=claimed_donations
            )

        elif current_user.role == 'admin':
            total_users = User.query.count()
            total_donations = Donation.query.count()
            active_donations = Donation.query.filter_by(status='active').count()
            claimed_donations = Donation.query.filter_by(status='claimed').count()

            return render_template(
                'dashboard/admin.html',
                total_users=total_users,
                total_donations=total_donations,
                active_donations=active_donations,
                claimed_donations=claimed_donations
            )

        return render_template('dashboard/default.html')

    # =========================
    # ✅ AUTO-CREATE DB TABLES (FIX)
    # =========================
    with app.app_context():
        db.create_all()

    return app


# =========================
# App instance (for Gunicorn)
# =========================
app = create_app()

# =========================
# Local development only
# =========================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
