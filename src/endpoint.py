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
    Returns all data stored in the database under public schema.

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
# def query_fact_prices_data():
#     """
#     Returns the prices data
#     Args: None
        
#     Returns: 
#         - Response 200 and JSON string - list of records 
#         (timestamp, price_in_usd, checksum) - see DBConnection class
#         - Response 504 if database connection not possible
#     """

#     try:
#         db = db_connection.DBConnection()
#     except IOError:
#         return "Database connection not possible", 504, {
#             "ContentType": "text/plain"
#         }
    
#     return db.query_fact_prices_data(), 200, {
#         "ContentType": "application/json"
#     }


# @app.route("/Info", methods=["GET"])
# def connection_stats():
#     """
#     Returns connection stats for database connection (debugging).

#     Args: None
    
#     Returns: 
#         - Response 200 and JSON string of connection stats - see 
#         DBConnection class for more info 
#         - Response 504 if database connection not possible
#     """

#     try:
#         db = db_connection.DBConnection()
#     except IOError:
#         return "Database connection not possible", 504, {
#             "ContentType": "text/plain"
#         }
    
#     return db.get_connection_stats(), 200, {"ContentType": "application/json"}


# @app.route("/insertSensorData", methods=["POST"])
# def insert_sensor_data():
#     """
#     Takes a post request with a JSON object of form:
#     {
#         "app_id": "cleancycle-application",
#         "dev_id": "",
#         "hardware_serial": "",
#         "port": 1,
#         "counter": 0,
#         "payload_raw": "",
#         "payload_fields": {
#             "0": 52.19398498535156,
#             "1": 0.1360626220703125,
#             "2": 38,
#             "3": 29,
#             "4": 52.19419860839844,
#             ....
#         },
#         "metadata": {
#             "time": "2019-02-25T16:00:46.840341614Z"
#         },
#         "downlink_url": ""
#     }

#     Payload fields:
#     - JSON object where keys 0,1,2,3 correspond to 
#     (Lat, Long, PM10, PM2.5) for first measurement
#     - Subsequent measurements can be obtained by grouping subsequent keys 
#     by 4
    
# Args: None

# Returns:
#     - Response 201 if data inserted successfully
#     - Response 400 if data has no payload
#     - Response 400 if data payload_fields are malformed - 
#         i.e. can't be grouped as records
#     - Response 504 if database connection not possible
#     """

#     try:
#         db = db_connection.DBConnection()
#     except IOError:
#         return "Database connection not possible", 504, {
#             "ContentType": "text/plain"
#         }

#     # this contains the prices data
#     if "payload_fields" in request.get_json():  
#         # i.e. we have the payload fields
#         sensor_data = request.get_json().get("payload_fields")
#         try:
#             db.insert_sensor_data(sensor_data.values())
#             return "Successful Insertion", 201, {"ContentType": "text/plain"}

#         except IOError:
#             return "Error: malformed payload fields data", 400, {
#                 "ContentType": "text/plain"
#             }

#     else:
#         return "Error no payload fields in JSON", 400, {
#             "ContentType": "text/plain"
#         }


def run():
    """
    Start up Flask endpoint on port 80
    """
    app.run(debug=True, host="0.0.0.0", port=80)
