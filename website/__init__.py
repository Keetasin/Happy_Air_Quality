from flask import Flask
from .views import views
from .templates.analytics import create_analytics_application
from .templates.prediction import create_prediction_application


def create_app():
    app = Flask(__name__)
    app.register_blueprint(views, url_prefix='/')
    create_analytics_application(app)
    create_prediction_application(app)
    return app


