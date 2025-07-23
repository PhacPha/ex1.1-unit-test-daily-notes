from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from mongoengine import connect
from config import Config

from routes.auth import auth
from routes.notes import notes

app = Flask(__name__)
app.config.from_object(Config)

# Configure CORS properly for development
CORS(app, 
     origins=["http://localhost:3000"],  # Allow frontend origin
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allow all necessary methods
     allow_headers=["Content-Type", "Authorization"],  # Allow necessary headers
     supports_credentials=True)  # Allow credentials if needed

JWTManager(app)

# Add error handlers for debugging
@app.errorhandler(500)
def internal_error(error):
    print(f"Internal server error: {error}")
    return {"msg": "Internal server error"}, 500

@app.errorhandler(Exception)
def handle_exception(e):
    print(f"Unhandled exception: {e}")
    import traceback
    traceback.print_exc()
    return {"msg": "An error occurred"}, 500

# เชื่อมต่อ MongoDB ด้วย mongoengine โดยตรง
connect(
    db=app.config["MONGODB_SETTINGS"]["db"],
    host=app.config["MONGODB_SETTINGS"]["host"],
    port=app.config["MONGODB_SETTINGS"]["port"]
)

# Add a simple test endpoint
@app.route('/api/test', methods=['GET', 'OPTIONS'])
def test():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
        return response
    return jsonify({"msg": "Backend is working!", "status": "ok"})

# Register Blueprints
app.register_blueprint(auth, url_prefix="/api")
app.register_blueprint(notes, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5001)