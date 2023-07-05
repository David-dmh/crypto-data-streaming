import sys
from requests import session
from flask import \
    abort, jsonify, redirect, render_template, request, url_for
from flask_migrate import Migrate
import cryptocompare
import psycopg2

from init import create_app
from models import db, DimCoinModel, FactPriceModel

app = create_app()

# bootstrap database migrate commands
db.init_app(app)
migrate = Migrate(app, db)

# # google-login 
# def login_is_required(function):
#     def wrapper(*args, **kwargs):
#         if "google_id" not in session:
#             return abort(401)
#         else:
#             return function()
#     return wrapper

# routes
@app.route("/", methods=["GET", "POST"])
# @login_is_required
def Index():
    return render_template("Index.html")


@app.route("/Home", methods=["GET", "POST"])
# @login_is_required
def Home():
    return render_template("Home.html")


@app.route("/Prices", methods=["GET", "POST"])
# @login_is_required
def Prices():

    try: 
        conn = psycopg2.connect(
            database="crypto", 
            user="usr",  
            password="pwd", 
            host="localhost",
        )

    except:
        raise Exception()
    
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM public.fact_price")
    data = mycursor.fetchall()

    return render_template("Prices.html", data=data)


@app.route("/AnalyticsSuite", methods=["GET", "POST"])
# @login_is_required
def AnalyticsSuite():
    return render_template("AnalyticsSuite.html")


# # login-related routes
# @app.route("/Index")
# def Index():
#     return render_template("Index.html")


# @app.route("/Login")
# def Login():
#     session["google_id"] = "Test"
#     return redirect("/Home")


# # @app.route("/Callback")
# # def Callback():
# #     pass 


# @app.route("/Logout")
# def Logout():
#     session.clear()
#     return redirect("/Index")
#     # return render_template("Index.html")

# if running this module as a standalone program
# (cf. command in the Python Dockerfile)
if __name__ == "__main__":
    app.run(host="0.0.0.0")
