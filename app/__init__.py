from flask import Flask
from config import Config
from app.db import init_db
from app.routes import register_routes

def create_app():
    app = Flask(
        __name__, 
        template_folder="../templates",
        static_folder="../static"
    )
    
    app.config.from_object(Config)

    register_routes(app)
    init_db()

    return app