from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash

def create_admin():
    with app.app_context():
        # Create the database tables
        db.create_all()
        print("Database created successfully.")
        
        # Check if the admin user already exists
        if User.query.filter_by(username='admin').first():
            print("Admin user already exists.")
            return
        
        hashed_password = generate_password_hash('admin', method='pbkdf2:md5')
        
        # Create an admin user 
        admin = User(username='admin', email='admin@example.com', password=hashed_password, is_admin=True)
        
        # Add the user to the database
        db.session.add(admin)
        
        # Commit the changes
        db.session.commit()
        
        print("Admin user created successfully.")
        print(f"Admin API Key: {admin.api_key}")


create_admin()