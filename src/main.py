from flask import Flask, Request, render_template, sessions, redirect
from flask_login import login_required, LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from src.models import model as models
from flask_admin import Admin, AdminIndexView
from src.auth import Users
from src.api.userAPI import userapi
from src.api.dashboard import dash
from src.api.profile import prof
from src.models.model import User
import secrets


# Generate and print a secret key

app = Flask(__name__)

CORS(app)

app.config.from_object(models.BaseModel.Config)
generate_secret_key = lambda: secrets.token_hex(24)
secret_key = generate_secret_key()
app.config['SECRET_KEY'] = secret_key


db = models.db

migrate = Migrate(app, db)

db.init_app(app)

# Register the blueprint
app.register_blueprint(userapi)
app.register_blueprint(dash)
app.register_blueprint(prof)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # Replace this logic with your own method of fetching a user from the database
    return User.query.get(int(user_id))

@app.route('/admin')
@login_required
def admin_panel():
    return redirect('/admin')  # Redirect to the admin panel


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


