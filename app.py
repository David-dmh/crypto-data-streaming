from flask import Flask, request, url_for, redirect, render_template

app = Flask(__name__)

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
