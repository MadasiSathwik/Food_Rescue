from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SelectField, TextAreaField, DateTimeLocalField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from datetime import datetime


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField(
        'Role',
        choices=[('restaurant', 'Restaurant'), ('ngo', 'NGO')],
        validators=[DataRequired()]
    )

    # 🔥 NEW FIELDS ADDED
    organization_name = StringField('Organization Name', validators=[Length(max=150)])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    address = TextAreaField('Address')

    # Passwords
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', 
                             validators=[DataRequired(), EqualTo('password')])


class DonationForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    food_type = StringField('Food Type', validators=[DataRequired(), Length(max=100)])
    quantity = StringField('Approximate Quantity', validators=[DataRequired(), Length(max=100)])
    address = StringField('Pickup Address', validators=[DataRequired(), Length(max=300)])
    pickup_time = DateTimeLocalField('Available From', validators=[DataRequired()])
    expiry_time = DateTimeLocalField('Expires At', validators=[DataRequired()])
    image = FileField('Image (optional)', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    
    def validate_expiry_time(self, field):
        if field.data <= self.pickup_time.data:
            raise ValueError('Expiry time must be after pickup time')
        if field.data <= datetime.now():
            raise ValueError('Expiry time must be in the future')
