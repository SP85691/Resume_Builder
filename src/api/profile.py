from flask import Blueprint, render_template
from flask_login import login_required, current_user

prof = Blueprint('profile', __name__)

@prof.route('/profile/<username>')
@login_required
def profile(username):
    user = current_user
    return render_template('profile.html', user=user)
