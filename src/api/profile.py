from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from src.auth import Users
from src.models.model import User 
from src.models.model import db

prof = Blueprint('profile', __name__)

@prof.route('/profile/<username>')
@login_required
def profile(username):
    user = current_user
    return render_template('profile.html', user=user)

@prof.route('/update_profile/<username>')
@login_required
def update_profile(username):
    user = current_user
    return render_template('update_profile.html', user=user)

@prof.route('/update_profile/<username>', methods=['POST'])
@login_required
def update_profilePost(username):
    try:
        user = current_user
        # Get the login credentials from the request
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            address = request.form.get('address')
            city = request.form.get('city')
            state = request.form.get('state')
            zip_code = request.form.get('zip_code')
            country = request.form.get('country')

            result = Users.update_user(username=user.username, email=email, name=name, phone=phone, address=address, city=city, state=state, zip_code=zip_code, country=country)
            if result == "User updated successfully":
                return redirect('/profile/<username>')  # Redirect to the login page after successful signup
            else:
                return result  # Display the error message if signup failed

    except Exception as e:
        return f"Error: {str(e)}"
    
    return render_template('profile.html')