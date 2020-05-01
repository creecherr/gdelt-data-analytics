from flask import Flask, Blueprint
from flask_restful import Api
from api.resources import HealthCheck, Report, GdeltPipeline
from firebase_admin import credentials
import firebase_admin
import os
asset_bp = Blueprint('asset', __name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object(None)
    from api.resources import api
    app.register_blueprint(api)
    #using docker secrets to store the credtials file
    cred = credentials.Certificate("/run/secrets/credentials")
    firebase_admin.initialize_app(cred)

    api = Api(app)
    api.add_resource(HealthCheck, '/v1/healthCheck')
    api.add_resource(Report, '/v1/report')
    api.add_resource(GdeltPipeline, '/v1/trigger')
    return app


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=port, debug=True)
