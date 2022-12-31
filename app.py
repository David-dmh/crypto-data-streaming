from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Properties(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(1024))
    passes = db.Column(db.Boolean)

db.create_all()

# test area ############################################################

# @app.get("/")
# def home():
#     houses_list = db.session.query(Properties).all()
#     return render_template("base.html", houses_list=houses_list)
 
# @app.post("/add")
# def add():
#     address = request.form.get("address")
#     new_houses = Properties(address=address, passes=False)
#     db.session.add(new_houses)
#     db.session.commit()
#     return redirect(url_for("home"))

# @app.get("/update/<int:houses_id>")
# def update(houses_id):
#     houses = db.session.query(Properties).filter(Properties.id == houses_id).first()
#     houses.passes = not houses.passes
#     db.session.commit()
#     return redirect(url_for("home"))

# @app.get("/delete/<int:houses_id>")
# def delete(houses_id):
#     houses = db.session.query(Properties).filter(Properties.id == houses_id).first()
#     db.session.delete(houses)
#     db.session.commit()
#     return redirect(url_for("home"))

########################################################################
@app.route("/Home")
def Home():
    return render_template("Home.html")

@app.route("/Listings", methods=["GET", "POST"])
def Listings():
    if request.method == "POST":
        return redirect(url_for("Home"))

    return render_template("Listings.html")

@app.route("/AnalyticsSuite", methods=["GET", "POST"])
def AnalyticsSuite():
    if request.method == "POST":
        return redirect(url_for("Home"))

    return render_template("AnalyticsSuite.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
