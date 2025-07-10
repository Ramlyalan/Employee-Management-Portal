from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:YourNewPassword123!@localhost/employee_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Employee model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    department = db.Column(db.String(50))

# Home route - view all employees
@app.route('/')
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

# Add new employee
@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        new_emp = Employee(name=name, email=email, department=department)
        db.session.add(new_emp)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_employee.html')

# Edit employee
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    emp = Employee.query.get_or_404(id)
    if request.method == 'POST':
        emp.name = request.form['name']
        emp.email = request.form['email']
        emp.department = request.form['department']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_employee.html', emp=emp)

# Delete employee
@app.route('/delete/<int:id>')
def delete_employee(id):
    emp = Employee.query.get_or_404(id)
    db.session.delete(emp)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Create tables in MySQL if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)