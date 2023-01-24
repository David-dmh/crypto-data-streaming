from flask import Flask, render_template, url_for
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "123"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def Home():
    return render_template("Index.html")

@app.route("/Register")
def Register():
    return render_template("Register.html")

@app.route("/Login")
def Login():
    return render_template("Login.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
