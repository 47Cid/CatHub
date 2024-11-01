from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager

# Initialize extensions
csrf = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'THIS-CAN-BE-LEAK-VIA-SSTI'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Weak SameSite attribute for CSRF
app.config['CSRF_COOKIE_SAMESITE'] = 'Lax' 
 # Disable CSRF protection
app.config['WTF_CSRF_ENABLED'] = False 
app.config['SESSION_COOKIE_HTTPONLY'] = False

# Initialize extensions with the app
db.init_app(app)
csrf.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Import and register blueprints or routes here to avoid circular imports
with app.app_context():
   from app import routes, admin, api
