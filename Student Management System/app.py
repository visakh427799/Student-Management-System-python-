from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.utils import secure_filename
import os
import re


app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'student_management_system'

UPLOAD_FOLDER = './static/styles/Admin/images/events'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Intialize MySQL
mysql = MySQL(app)


@app.route('/')
def index():
    cursor =mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from students')
    result=cursor.fetchone()
    print(result)
    return render_template('home.html')


#admin routes
#login route for admin
@app.route('/admin/login', methods=['GET','POST'])
def adminLogin():
    #if login route is of method get
    if request.method=="GET":
        if 'adminloggedin' in session:
          return redirect(url_for('dashboard'))
        else:     
          return render_template('Admin/adminLogin.html')
    else:
    #login route post method
      #print(mysql)
      username=request.form['username']
      password=request.form['password']
      query='select * from users where username=%s  and password=%s'
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      result=cursor.execute(query,(username,password));
      account = cursor.fetchone()
      if account:
       session['adminloggedin'] =True
       return jsonify({'status':True})
       #return render_template('Admin/dashboard.html')
      else:
       message="Invalid credentials"
       return jsonify({'status':False})
       #return render_template('Admin/adminLogin.html',message=message)
        
@app.route('/admin/logout', methods=['GET'])
def adminLogout():
    session.pop('adminloggedin', None)
    return redirect(url_for('adminLogin'))
 
@app.route('/admin/dashboard', methods=['GET'])
def dashboard():
    if 'adminloggedin' in session:
      query='select * from admin'
      query2='select count(id) as total from students'
      query3='select count(id) as total1 from faculties'
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      result=cursor.execute(query);
      account = cursor.fetchone()
      result2=cursor.execute(query2);
      totalStudents = cursor.fetchone()
      result3=cursor.execute(query3);
      totalFaculties = cursor.fetchone()
      print(account)
     
      return render_template('Admin/dashboard.html',account=account,totalStudents=totalStudents,totalFaculties=totalFaculties)
    else:
      return redirect(url_for('adminLogin'))

@app.route('/admin/students', methods=['GET'])
def students():
    query='select * from students'
    query2='select count(id) as total from students'
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result=cursor.execute(query);
    allstudents = cursor.fetchall()
    result2=cursor.execute(query2);                 
    totalStudents = cursor.fetchone()
    return render_template('Admin/students.html',allstudents=allstudents,totalStudents=totalStudents)

@app.route('/admin/studentProfile/<id>/<roll>', methods=['GET'])
def studentProfile(id,roll):
   print(id,roll)
   query='select * from students where id=%s and admission_number=%s'
   cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
   result=cursor.execute(query,(id,roll));
   account = cursor.fetchone()
   return render_template('Admin/studentProfile.html',account=account)
@app.route('/admin/facultyProfile/<id>/<f_id>', methods=['GET'])
def facultyProfile(id,f_id):
   query='select * from faculties where id=%s and faculty_id=%s'
   cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
   result=cursor.execute(query,(id,f_id));
   account = cursor.fetchone()
   return render_template('Admin/facultyProfile.html',account=account)


@app.route('/admin/editStudentProfile/<id>/<roll>', methods=['GET'])
def editStudentProfile(id,roll):
   print(id,roll)
   query='select * from students where id=%s and admission_number=%s'
   cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
   result=cursor.execute(query,(id,roll));
   account = cursor.fetchone()
   return render_template('Admin/editStudentProfile.html',account=account)


@app.route('/admin/editStudentProfile',methods=['POST'])
def editSprofile():
    fname=request.form['fname']
    admission=request.form['adnum']
    phone=request.form['phn']
    email=request.form['em']
    address=request.form['add']
    gender=request.form['gen']
    religion=request.form['rel']
    dob=request.form['dob']
    course=request.form['cor']
    batch=request.form['bat']
    propic=request.files['file'].filename
    sid=request.form['stid']
    if not propic:
      propic=request.form['previmg']
    print(propic)
    query='UPDATE `students` SET `admission_number`=%s,`fname`=%s ,`gender`=%s,`dob`=%s,`religion`=%s, `phone`=%s,`address`=%s,`email`=%s,`course`=%s,`batch`=%s,`profile_img`=%s WHERE `id` =%s;'
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result=cursor.execute(query,(admission,fname,gender,dob,religion,phone,address,email,course,batch,propic,sid))
    mysql.connection.commit()
    if result:
          return redirect(url_for('studentProfile',id=sid,roll=admission))
    else:
          return redirect(url_for('editStudentProfile',id=sid,roll=admission))

@app.route('/admin/faculties', methods=['GET'])
def faculties():
    query='select * from faculties'
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result=cursor.execute(query)
    faculty = cursor.fetchall()
    return render_template('Admin/faculties.html',faculty=faculty)

@app.route('/admin/events',methods=['GET'])
def adminEvents():
    query='select * from events'
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result=cursor.execute(query)
    events = cursor.fetchall()
    print(events)
    return render_template('Admin/events.html',events=events)

@app.route('/admin/addevent', methods=['GET','POST'])
def addEvents():
    if request.method=="GET":
     return render_template('Admin/addEvent.html')
    else:
     event_name=request.form['event-name'] 
     event_desc=request.form['event-desc'] 
     event_dte=request.form['event-date']
     f=request.files['file']
     event_img=request.files['file'].filename
     f.save(os.path.join(app.config['UPLOAD_FOLDER'], event_img))
     event_id='2';
     print(event_desc)
     print(event_name)
     print(event_img)
     print(event_dte)
     query='insert into `events` (`event_name`, `event_date`, `event_description`, `event_image`) values(%s,%s,%s,%s)'
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     result=cursor.execute(query,(event_name,event_dte,event_desc,event_img))
     mysql.connection.commit()
     if result:
         return redirect(url_for('adminEvents'))
     else:
         return  render_template('Admin/addEvent.html')
     



@app.route('/admin/cancelevent', methods=['POST'])
def cancelEvent():
    id=request.form['id']
    print(id)
    query='DELETE FROM events WHERE event_id=%s'
    cursor = mysql.connection.cursor()
    result=cursor.execute(query,(id));
    mysql.connection.commit()
    if result:
       return jsonify({'status':True})


@app.route('/admin/deletestudent', methods=['POST'])
def deleteStudent():
    s_id=request.form['id']
    print(s_id)
    cursor =mysql.connection.cursor()
    result=cursor.execute('DELETE FROM students WHERE admission_number=%s',(s_id,))
    mysql.connection.commit()
    if result:
       return jsonify({'status':True})

@app.route('/admin/approve', methods=['POST'])
def approveStudent():
    s_id=request.form['id']
    print(s_id)
    cursor =mysql.connection.cursor()
    result=cursor.execute('UPDATE students SET approval=%s where admission_number=%s',('1',s_id,))
    mysql.connection.commit()
    if result:
       return jsonify({'status':True})
    
#user routes

@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['email'] = account['email']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

# http://localhost:5000/python/logout - this will be the logout page

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users


@app.route('/s_welcome')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s',
                       (session['id'],))
        account = cursor.fetchone()

        return render_template('s_welcome.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users


@app.route('/s_profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s',
                       (session['id'],))
        account = cursor.fetchone()

        # Show the profile page with account info
        return render_template('s_profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/s_attendance')
def s_attendance():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s',
                       (session['id'],))
        account = cursor.fetchone()
        return render_template('s_attendance.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/s_marks')
def s_marks():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s',
                       (session['id'],))
        account = cursor.fetchone()
        return render_template('s_marks.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/s_timetable')
def s_timetable():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s',
                       (session['id'],))
        account = cursor.fetchone()
        return render_template('s_timetable.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
