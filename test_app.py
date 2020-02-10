import unittest
import os
import json
import flask
from flask import request, jsonify

import app
from app import BadDataError
from app import check_log_level
from app import check_port_value
from app import get_input


HOME_URL = 'http://127.0.0.1:5000/'
BASE_URL = 'http://127.0.0.1:5000/api/v1.0/info'
BAD_ITEM_URL = '{}/5'.format(BASE_URL)
GOOD_ITEM_URL = '{}/3'.format(BASE_URL)


class TestInfo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        return super().setUpClass()


    @classmethod
    def tearDownClass(cls):
        return super().tearDownClass()

    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True
        os.environ['SERVICE_NAME'] = 'unittest'
        os.environ['VERSION'] = '0.0.1'
        os.environ['GIT_COMMIT_SHA'] = '1290a2f'
        os.environ['LOG_LEVEL'] = 'CRITICAL'
        os.environ['SERVICE_PORT'] = '4567'


    def tearDown(self):
        pass

    def test_valid_level(self):
        print('test valid log_level value')
        self.assertIsNone(check_log_level('ERROR'))

    def test_valid_port(self):
        print('test valid service port')
        self.assertIsNone(check_port_value('12345'))

    def test_invalid_level(self):
        print('test invalid log_level value')
        with self.assertRaises(BadDataError):
            check_log_level('NOPE')

    def test_invalid_port(self):
        print('test invalud service_port value - out of valid range')
        with self.assertRaises(BadDataError):
            check_port_value('99999')

    def test_alpha_port(self):
        print('test invalid service_port - contains non numerics')
        with self.assertRaises(BadDataError):
            check_port_value('99A99')

    def test_info(self):
        print('test invalid route and return 404')
        self.assertEqual(self.app.get(HOME_URL).status_code, 400)

    def test_info(self):
        print('test valid scenario')
        response = self.app.get(BASE_URL)
        expected_result = {'service_name': 'unittest', 'version': '0.0.1', 'git_commit_sha': '1290a2f', 'environment': {'service_port': '4567', 'log_level': 'CRITICAL'}}
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(json.loads(response.get_data()), expected_result)

    def test_no_environ_service_name(self):
        print('test missing environment variable - service name')
        del os.environ['SERVICE_NAME']
        response = self.app.get(BASE_URL)
        expected_result = {'status': 422, 'message': 'Environment Information is not currently available'}
        self.assertEqual(response.status_code, 422)
        self.assertAlmostEqual(json.loads(response.get_data()), expected_result)

    def test_no_environ_version(self):
        print('test missing environment variable - version')
        del os.environ['VERSION']
        response = self.app.get(BASE_URL)
        expected_result = {'status': 422, 'message': 'Environment Information is not currently available'}
        self.assertEqual(response.status_code, 422)
        self.assertAlmostEqual(json.loads(response.get_data()), expected_result)

    def test_no_environ_sha(self):
        print('test missing environment variable - git_commit_sha')
        del os.environ['GIT_COMMIT_SHA']
        response = self.app.get(BASE_URL)
        expected_result = {'status': 422, 'message': 'Environment Information is not currently available'}
        self.assertEqual(response.status_code, 422)
        self.assertAlmostEqual(json.loads(response.get_data()), expected_result)

    def test_no_environ_log_level(self):
        print('test missing environment variable - log_level')
        del os.environ['LOG_LEVEL']
        response = self.app.get(BASE_URL)
        expected_result = {'status': 422, 'message': 'Environment Information is not currently available'}
        self.assertEqual(response.status_code, 422)
        self.assertAlmostEqual(json.loads(response.get_data()), expected_result)

    def test_no_environ_port(self):
        print('test missing environment variable - service_port')
        del os.environ['SERVICE_PORT']
        response = self.app.get(BASE_URL)
        expected_result = {'status': 422, 'message': 'Environment Information is not currently available'}
        self.assertEqual(response.status_code, 422)
        self.assertAlmostEqual(json.loads(response.get_data()), expected_result)

if __name__ == '__main__':
    unittest.main()