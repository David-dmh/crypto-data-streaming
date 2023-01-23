from flask import Flask, render_template
from flask_login import LoginManager

app = Flask(__name__)

login_manager = LoginManager()

@app.route("/")
def hello_world():
    return render_template("Index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
