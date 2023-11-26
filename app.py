from src.main import app, db

if __name__ == '__main__':
    # Use db.create_all() to create tables
    with app.app_context():
        # Use db.create_all() within the app context to create tables
        db.create_all()
    app.run(debug=True)