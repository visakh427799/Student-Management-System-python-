from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'student_management_system'

# Intialize MySQL
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('home.html')

#admin routes
#login route for admin
@app.route('/admin/login', methods=['GET','POST'])
def adminLogin():
    #if login route is of method get
    if request.method=="GET":
     return render_template('Admin/adminLogin.html')
    else:
    #login route post method
      #print(mysql)
      name=request.form['username']
      password=request.form['password']
      query='select * from users where name=%s  and password=%s'
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      result=cursor.execute(query,(name,password));
      account = cursor.fetchone()
      if account:
       session['adminloggedin'] = True
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
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      result=cursor.execute(query);
      account = cursor.fetchone()
      print(account)
      return render_template('Admin/dashboard.html',account=account)
    else:
      return redirect(url_for('adminLogin'))

@app.route('/admin/students', methods=['GET'])
def students():
    return render_template('Admin/students.html')

@app.route('/admin/faculties', methods=['GET'])
def faculties():
    return render_template('Admin/faculties.html')



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
