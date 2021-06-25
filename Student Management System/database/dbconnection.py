from flask import Flask, render_template
from flask_mysqldb import MySQL
import MySQLdb.cursors
app = Flask(__name__)
def dbconn():
    
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'student_management_system'  
    
    mysql = MySQL(app)
    return mysql





