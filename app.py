from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask("SmartTrack")

# Configure PostgreSQL database connection (replace with your Render PostgreSQL connection string)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://smart_track_user:7hzAF8qUNWYRjkdZ87VVhjXKc3IrWy6I@dpg-cvnd6ru3jp1c738hiudg-a/smart_track'
# Initialize the database
db = SQLAlchemy(app)

# Define the Attendance model
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)

# Define the Files model
class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)

# Route for the dashboard
@app.route('/')
def dashboard():
    return render_template('index.html')

# Route for managing attendance
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        name = request.form['name']
        status = request.form['status']
        new_record = Attendance(name=name, status=status)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('attendance'))  # Refresh page after submitting data
    
    records = Attendance.query.all()
    return render_template('attendance.html', records=records)

# Route for managing files
@app.route('/files', methods=['GET', 'POST'])
def files():
    if request.method == 'POST':
        filename = request.form['filename']
        status = request.form['status']
        new_file = Files(filename=filename, status=status)
        db.session.add(new_file)
        db.session.commit()
        return redirect(url_for('files'))  # Refresh page after submitting data
    
    records = Files.query.all()
    return render_template('files.html', records=records)

# Main entry point of the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't already exist
    app.run(debug=True)
