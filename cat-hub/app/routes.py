from flask import render_template, url_for, flash, send_file, redirect, request, abort, send_from_directory, render_template_string
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.forms import RegistrationForm, LoginForm, CommentForm, SettingsForm
from app.models import User, Comment, AppSettings
from app import login_manager
from app.config.headers import sttf_headers as add_security_headers
import os

UPLOAD_FOLDER = os.getcwd()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Add security headers to all responses
@app.after_request
def after_request(response):
    return add_security_headers(response)

@app.route("/")
@app.route("/home")
def home():
    # Fetch the current settings
    settings = AppSettings.query.first()
    if not settings:
        settings = AppSettings(greeting_message='Hello')
        db.session.add(settings)
        db.session.commit()
    greetings = settings.greeting_message
    return render_template('home.html', user=current_user, greetings=greetings)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('An account with this email already exists. Please log in.', 'warning')
            return redirect(url_for('login'))
        
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:md5')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return f"Hello, {current_user.username}! This is your account page."

@app.route("/comments", methods=['POST', 'GET'])
@login_required
def comments():
    form = CommentForm()
    comments = Comment.query.all()  # Fetch all comments
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('comments'))
    
    api_key = current_user.api_key
    return render_template('comments.html', title='El Gato', form=form, comments=comments, api_key=api_key)

@app.route("/dev")
@login_required
def dev():
    settings = AppSettings.query.first() 
    greetings = settings.greeting_message
    
    html_content = '''
    <!DOCTYPE html>
    <html>
      <head>
        <title>Under Construction</title>
      </head>
      <body>
        <p>{greetings}, this page is still under development :)</p>
      </body>
    </html>
    '''
    # Format the HTML content with the greetings value
    rendered_html = html_content.format(greetings=greetings)
    return render_template_string(rendered_html)

@app.route("/delete_user/<int:user_id>", methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:  # Only allow admins to delete users
        flash('You do not have permission to delete users.', 'danger')
        return redirect(url_for('home'))
    
    user = User.query.get_or_404(user_id)  # Fetch the user by ID
    if user == current_user:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin'))
    
    db.session.delete(user)  # Delete the user from the database
    db.session.commit()
    flash(f'User {user.username} has been deleted.', 'success')
    return redirect(url_for('admin'))

@app.route('/files')
@login_required
def serve_file():
    filename = request.args.get('filename')
    if not filename:
        abort(400, "Filename query parameter is required")
    
    # Construct the full path
    safe_path = os.path.join(UPLOAD_FOLDER, filename)
    safe_path = os.path.abspath(safe_path)  # Get the absolute path
    print("Requested file path:", safe_path)  # Debug statement
    
    # Check if the file exists
    if not os.path.isfile(safe_path):
        print("File not found:", safe_path)  # Debug statement
        abort(404, "File not found")  # Not found if the file does not exist
    
    # Read and send the file contents
    return send_file(safe_path)