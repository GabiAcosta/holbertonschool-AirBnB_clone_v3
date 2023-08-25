from flask import Flask, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

@app.errorhandler(404)
def error_404(exception):
    return jsonify(error="Not found"), 404

if __name__ == '__main__':
    if getenv("HBNB_API_HOST"):
        host = getenv("HBNB_API_HOST")
    else:
        host = "0.0.0.0"

    if getenv("HBNB_API_PORT"):
        port = getenv("HBNB_API_PORT")
    else:
        port = "5000"

    app.run(host=host, port=port, threaded=True)