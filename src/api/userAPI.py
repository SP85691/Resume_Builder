from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from src.auth import Users


userapi = Blueprint('userapi', __name__)

bcrypt = Bcrypt()
jwt = JWTManager()

@userapi.route('/login')
def login():
    return render_template('login.html')

@userapi.route('/login', methods=['POST'])
def loginPost():
    try:       
        # Get the login credentials from the request
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            result = Users.Login_User(email=email, password=password)
            if result == "Login successful":
                    return redirect(url_for('index'))  # Redirect to the login page after successful signup
            else:
                return result
        
    except Exception as e:
        return f"Error: {str(e)}"
    
    return render_template('index.html')

@userapi.route('/signup')
def signup():
    return render_template('register.html')

@userapi.route('/signup', methods=['POST'])
def signupPost():
    try:
        # Get the login credentials from the request
        if request.method == 'POST':
            name = request.form.get('name')
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            result = Users.create_user(username=username, email=email, password=password, name=name)
            if result == "User created successfully":
                return redirect('/login')  # Redirect to the login page after successful signup
            else:
                return result  # Display the error message if signup failed

    except Exception as e:
        return f"Error: {str(e)}"
    
    return render_template('login.html')

@userapi.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))