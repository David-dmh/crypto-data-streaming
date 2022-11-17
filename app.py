from flask import Flask, render_template

app = Flask(__name__)

@app.route('/Home', methods=['GET'])
def home_url():
    """"""
    return render_template("Home.html")
  

@app.route('/Listings', methods=['GET'])
def listings_url():
    """"""



@app.route('/AnalyticsSuite', methods=['GET'])
def analyticssuite_url():
    """"""




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
