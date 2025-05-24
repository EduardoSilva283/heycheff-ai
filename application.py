from flask import Flask
from src.site.main import bp_site

def create_app():
    app = Flask(__name__)

    app.register_blueprint(bp_site, url_prefix='/')

    return app
