from flask import Flask,render_template
app = Flask(__name__)

@app.route('/admin/dashboard', methods=['GET'])
def dashboard():
    return render_template('Admin/dashboard.html')

@app.route('/admin/students', methods=['GET'])
def students():
    return render_template('Admin/students.html')
    
@app.route('/admin/faculties', methods=['GET'])
def faculties():
    return render_template('Admin/faculties.html')


