from flask import Flask
from config import Config
import threading
import time
import requests

def ping_self():
    while True:
        try:
            print("⏰ Pinging keep-alive endpoint to keep server active...")
            requests.get("https://ml-model-for-fraud-detection-and-risk.onrender.com/api/keep-alive")
        except Exception as e:
            print(f"[Keep-Alive Ping Error] {e}")
        time.sleep(180)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.routes.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Start background thread
    if not app.config.get('TESTING', False):
        threading.Thread(target=ping_self, daemon=True).start()

    return app