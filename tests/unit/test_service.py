from api.service import GoogleBigQuery
from tests.base import BaseTestCase
from unittest import mock
import requests
from requests import Response


class TestGoogleBigQuery(BaseTestCase):
    """
    Basic success and failure tests for the GoogleBigQuery class. Unfortunately, due to time I am not able to add more.
    I did want to be able to provide a small snapshot of the type of unit tests I write.
    """
    def setUp(self):
        self.query_service = GoogleBigQuery()

    def test_get_gdelt_data_success(self):
        response = Response()
        response.status_code = 200
        response._content = b'{"pageToken": "test", "rows": [{"test": "123"}]}'
        with mock.patch.object(self.query_service, 'get_access_token') as access_token:
            with mock.patch.object(requests, 'get', return_value=response) as get_data:
                test_response = self.query_service.get_gdelt_data('123')
                self.assertEqual(test_response, [{"test": "123"}])
                access_token.assert_called_once()
                get_data.assert_called_once()

    def test_get_gdelt_data_response_failure(self):
        response = Response()
        response.status_code = 400
        with mock.patch.object(self.query_service, 'get_access_token') as access_token:
            with mock.patch.object(requests, 'get', return_value=response) as get_data:
                self.assertRaises(SystemError, self.query_service.get_gdelt_data, '123')
                access_token.assert_called_once()
                get_data.assert_called_once()

    def test_get_access_token_success(self):
        response = Response()
        response.status_code = 200
        response._content = b'{"access_token": "test"}'
        with mock.patch.object(requests, 'post', return_value=response) as get_token:
            test_response = self.query_service.get_access_token()
            self.assertEqual(test_response, "test")
            get_token.assert_called_once()

    def test_get_access_token_failure(self):
        response = Response()
        response.status_code = 400
        with mock.patch.object(requests, 'post', return_value=response) as get_token:
            self.assertRaises(SystemError, self.query_service.get_access_token)
            get_token.assert_called_once()

    def test_get_total_rows_success(self):
        response = Response()
        response.status_code = 200
        response._content = b'{"totalRows": "12"}'
        with mock.patch.object(requests, 'get', return_value=response) as get_rows:
            test_response = self.query_service.get_row_count()
            self.assertEqual(test_response, 12)
            get_rows.assert_called_once()

    def test_get_access_token_failure(self):
        response = Response()
        response.status_code = 400
        with mock.patch.object(requests, 'get', return_value=response) as get_rows:
            self.assertRaises(SystemError, self.query_service.get_row_count)
            get_rows.assert_called_once()



