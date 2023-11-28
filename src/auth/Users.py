from datetime import datetime  # For setting created_at and updated_at fields
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user
from src.models.model import db  # Import the SQLAlchemy object from your application
from src.models.model import User  # Import your User model
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
def create_user(username, email, password, name, phone=None, address=None, city=None, state=None, zip=None, country=None):
    # Check if the username and email are not already in use
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return "Username or email already exists"

    # Create a new User instance
    hashed_password = generate_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        password=hashed_password,  # Remember, you might want to hash the password before saving it
        name=name,
        phone=phone,
        address=address,
        city=city,
        state=state,
        zip=zip,
        country=country,
        created_at=datetime.now(),  # Set the creation timestamp
        updated_at=datetime.now()   # Set the update timestamp
    )

    # Add the new user to the database session
    db.session.add(new_user)

    try:
        # Commit the session to the database
        db.session.commit()
        return "User created successfully"
    except Exception as e:
        # Rollback the session in case of an exception
        db.session.rollback()
        return str(e)  # Return the error message
    
def Login_User(email, password):
    try:
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)  # Logging in the user
            return "Login successful"
        elif user:
            return "Invalid password"
        else:
            return "User not found"

    except Exception as e:
        return f"Error: {str(e)}"
    
def update_user(username, email, name, phone=None, address=None, city=None, state=None, zip_code=None, country=None):
    try:
        # Fetch the user based on the provided username
        user = User.query.filter_by(username=username).first()

        if user:
            user.name = name
            user.email = email
            user.phone = phone
            user.address = address
            user.city = city
            user.state = state
            user.zip = zip_code
            user.country = country
            user.updated_at = datetime.now()

            # Commit changes to the database
            db.session.commit()

            # Create a dictionary with user information
            user_info = {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'address': user.address,
                'city': user.city,
                'state': user.state,
                'zip_code': user.zip,
                'country': user.country,
                'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M:%S')  # Format the datetime
            }

            return jsonify({'message': 'User profile updated successfully', 
                            'User Info': user_info})
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

