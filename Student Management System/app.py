from flask import Flask,render_template
from routes import admin
app = Flask(__name__)


@app.route('/')
def index():
    return "Home"

if __name__ == "__main__":
 app.run(debug=True)
