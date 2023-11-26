from flask import Blueprint, render_template
from flask_login import login_required, current_user

dash = Blueprint('dashboard', __name__)

@dash.route('/dashboard')
@login_required
def dashboard():
    user = current_user 
    return render_template('dashboard.html', user=user)