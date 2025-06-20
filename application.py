from flask import Flask
from src.site.main import bp_site
from src.recommendation.routes import recommendation_bp
from src.conversion_recipe.routes import conversion_bp

    
def create_app():
    app = Flask(__name__)

    app.register_blueprint(bp_site, url_prefix='/')
    app.register_blueprint(recommendation_bp, url_prefix='/recommendation')
    app.register_blueprint(conversion_bp, url_prefix='/conversion')

    return app
