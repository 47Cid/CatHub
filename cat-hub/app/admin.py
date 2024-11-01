from flask import render_template, url_for, flash, redirect, request, render_template_string
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.forms import RegistrationForm, LoginForm, CommentForm, SettingsForm
from app.models import User, Comment, AppSettings
from app import login_manager


@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:  # Ensure only admin can access
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))

    form = SettingsForm()

    # Fetch all users for the admin page
    users = User.query.all()

    # Fetch the current settings or create a new one if none exist
    settings = AppSettings.query.first()
    if not settings:
        settings = AppSettings(greeting_message='Hello')
        db.session.add(settings)
        db.session.commit()

    # Update the greeting message
    if form.validate_on_submit():
        settings.greeting_message = form.greeting_message.data
        db.session.commit()

        return redirect(url_for('admin'))

    # Set the form's initial data to the current greeting message
    form.greeting_message.data = settings.greeting_message
    return render_template('admin.html', form=form, user=current_user, users=users)
