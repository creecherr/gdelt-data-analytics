"""
The main controller and entry point for the API
"""
from flask import Blueprint, send_from_directory, jsonify
import logging
from flask_restful import Resource
from api.service import handler
from api.analysis import report_generator

logger = logging.getLogger('api_resource')
api = Blueprint('api', 'api', url_prefix='/v1')


class HealthCheck(Resource):
    @staticmethod
    @api.route('/healthChecks', methods=['GET'])
    def get():
        """
        For when we want to check if the service is up and running
        """
        logging.info("The system is healthy.")
        return jsonify("OK")


class Report(Resource):
    @staticmethod
    @api.route('/reports', methods=['GET'])
    def get_reports():
        try:
            report_generator()
            return send_from_directory('.', 'report.pdf')
        except Exception as e:
            return jsonify(str(e)), 500


class GdeltPipeline(Resource):
    @staticmethod
    @api.route('/trigger', methods=['POST'])
    def transfer_gdelt():
        try:
            handler()
            return jsonify("OK"), 201
        except Exception as e:
            return jsonify(e), 500
