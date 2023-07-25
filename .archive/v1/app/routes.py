from flask import jsonify

# routes factory
def init_routes(app):

    @app.route("/status", methods=["GET"])
    def get_api_base_url():
        return jsonify(
            {
                "msg": "crypto api is up", 
                "success": True, 
                "data": None
            }
        ), 200