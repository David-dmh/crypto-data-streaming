from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# db.create_all()

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

#######################################################################
# test area

# class Properties(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     address = db.Column(db.String(1024))
#     passes = db.Column(db.Boolean)

class HouseModel(db.Model):
    __tablename__ = "houses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_address = db.Column(db.String())
    suburb = db.Column(db.String())
    state = db.Column(db.String())
    postcode = db.Column(db.String())
    price = db.Column(db.String())
    bedrooms = db.Column(db.String())
    bathrooms = db.Column(db.String())
    parking_spaces = db.Column(db.String())
    building_size = db.Column(db.String())
    building_size_unit = db.Column(db.String())
    land_size = db.Column(db.String())
    land_size_unit = db.Column(db.String())
    listing_company_name = db.Column(db.String())
    sold_date = db.Column(db.String())
    description = db.Column(db.String())
    listing_download_date = db.Column(db.String())
    
    def __init__(self, 
                 full_address, 
                 suburb,
                 state,
                 postcode,
                 price,
                 bedrooms,
                 bathrooms,
                 parking_spaces,
                 building_size,
                 building_size_unit,
                 land_size,
                 land_size_unit,
                 listing_company_name,
                 sold_date,
                 description,
                 listing_download_date):
        self.full_address = full_address
        self.suburb = suburb
        self.state = state
        self.postcode = postcode
        self.price = price
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.parking_spaces = parking_spaces
        self.building_size = building_size
        self.building_size_unit = building_size_unit
        self.land_size = land_size
        self.land_size_unit = land_size_unit
        self.listing_company_name = listing_company_name
        self.sold_date = sold_date
        self.description = description
        self.listing_download_date = listing_download_date


    def __repr__(self):
        return f"<House {self.address}>"

########################################################################
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
