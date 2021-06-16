from flask import Flask,render_template
app = Flask(__name__)

@app.route('/user/home',methods=['GET'])
def home():
    return "User Home"
