from flask import Flask, render_template, url_for
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.secret_key = "123"

# login_manager = LoginManager()
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)


class User(db.model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)


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
