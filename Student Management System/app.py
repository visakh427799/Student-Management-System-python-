from flask import Flask, render_template
from flask_mysqldb import MySQL
#from routes import admin
from database import dbconnection;
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'student_management_system'
 
mysql = MySQL(app)


@app.route('/')
def index():
    #cur = mysql.connection.cursor()
    #cur.execute('CREATE TABLE test1 (name VARCHAR(255), address VARCHAR(255))')
    #mysql.connection.commit()
    #cur.close()
    return "Home"

#admin routes.

@app.route('/admin/dashboard', methods=['GET'])
def dashboard():
    return render_template('Admin/dashboard.html')

@app.route('/admin/students', methods=['GET'])
def students():
    return render_template('Admin/students.html')
    
@app.route('/admin/faculties', methods=['GET'])
def faculties():
    return render_template('Admin/faculties.html')


#user routes


@app.route('/s_welcome')
def s_welcome():
    return render_template('s_welcome.html')


@app.route('/s_profile')
def s_profile():
    return render_template('s_profile.html')


@app.route('/s_attendance')
def s_attendance():
    return render_template('s_attendance.html')


@app.route('/s_marks')
def s_marks():
    return render_template('s_marks.html')


@app.route('/s_timetable')
def s_timetable():
    return render_template('s_timetable.html')






if __name__ == "__main__":
    app.run(debug=True)
