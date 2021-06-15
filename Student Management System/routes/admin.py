from flask import Flask,render_template
app = Flask(__name__)

@app.route('/admin/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

