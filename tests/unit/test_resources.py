from api.resources import HealthCheck, Report
from api.analysis import report_generator
from tests.base import BaseTestCase
from unittest import mock
import mock


class TestHealthCheck(BaseTestCase):
    def setUp(self):
        self.health_check = HealthCheck()

    def test_health_check_returns_ok_response(self):
        response = self.health_check.get()
        self.assertEqual('200 OK', response.status)
        self.assertEqual(200, response.status_code)
