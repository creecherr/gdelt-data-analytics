from flask_testing import TestCase
from app import create_app
from firebase_admin import credentials
from unittest import mock
import firebase_admin


class BaseTestCase(TestCase):
    def create_app(self):
        with mock.patch.object(credentials, 'Certificate'):
            with mock.patch.object(firebase_admin, 'initialize_app'):
                app = create_app()
                return app
