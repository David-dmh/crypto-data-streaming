from flask import Flask, request, render_template
from flask_cors import CORS

import db_connection

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("Index.html")

@app.route("/Data", methods=["GET"])
def database_info():
    """
    Returns all data in database under public schema.
    Args: None
    Returns: 
        - Response 200 and JSON string where values are list of records 
        indexed by table name as key 
        - Response 504 if database connection not possible
    """

    try:
        db = db_connection.DBConnection()

    except IOError:
        return "Database connection not possible", 504, {
            "ContentType": "text/plain"
        }

    return db.get_database_info(), 200, {"ContentType": "application/json"}


def run():
    """
    Start up Flask endpoint on port 80
    """
    app.run(debug=True, host="0.0.0.0", port=80)
