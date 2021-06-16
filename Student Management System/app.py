from flask import Flask, render_template
from routes import admin
app = Flask(__name__)


@app.route('/')
def index():
    return "Home"


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
