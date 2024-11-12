from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db

def create_app():
    app = Flask(__name__)
    
    # Load configurations from Config class
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Enable CORS
    CORS(app)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)