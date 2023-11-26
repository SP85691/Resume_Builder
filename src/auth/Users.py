from datetime import datetime  # For setting created_at and updated_at fields
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user
from src.models.model import db  # Import the SQLAlchemy object from your application
from src.models.model import User  # Import your User model
from werkzeug.security import generate_password_hash, check_password_hash

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

