# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    8.11.16   
#
# -----------------------------------------------------------------------------------------------


# Libraries
import unittest
import time
import os
from multiprocessing import Process
import requests
import filecmp

from micro_service import app_path
from micro_service.micro_service import flask_app
from micro_service.framework import load_config


class TestMicroService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.host        = '127.0.0.1'
        cls.port        = '5000'
        cls.flask_env   = os.environ['ENV'].lower()
        cls.config      = load_config(cls.flask_env)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.create_simple_webserver()
        self.base_url = 'http://{}:{}'.format(TestMicroService.host, TestMicroService.port)
        self.create_session()

    def tearDown(self):
        self.teardown_simple_webserver()

    # Helper functions
    # -----------------------------------------------------
    def create_simple_webserver(self):
        self.web_server_process = Process(target=flask_app.run, args=(), kwargs={'debug': False}, name='server')
        self.web_server_process.start()
        time.sleep(1)

    def teardown_simple_webserver(self):
        self.web_server_process.terminate()

    def remove_all_files(self, path):
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))

    def create_session(self):
        self.session = requests.Session()
        self.session.get(self.base_url)
        self.token = self.session.cookies['_csrf_token']

    # Tests functions
    # -----------------------------------------------------
    def test_root(self):
        response = requests.get(self.base_url)

        assert response.status_code == 200, 'Response code incorrect: {}'.format(response.status_code)
        assert response.text == 'Root page', 'Response incorrect: {}'.format(response.text)

    def test_version_1_0_0(self):
        response = requests.get(self.base_url + '/v1_0_0/hello')

        assert response.status_code == 200, 'Response code incorrect: {}'.format(response.status_code)
        assert response.text == 'Hello v1.0.0', 'Response incorrect: {}'.format(response.text)

    def test_version_2_0_0(self):
        response = requests.get(self.base_url + '/v2_0_0/hello')

        assert response.status_code == 200, 'Response code incorrect: {}'.format(response.status_code)
        assert response.text == 'Hello v2.0.0', 'Response incorrect: {}'.format(response.text)

    def test_restful_all_version(self):
        response = requests.get(self.base_url + '/v1_0_0/restful_hello')

        assert response.status_code == 200, 'Response code incorrect: {}'.format(response.status_code)
        assert response.text == '"Restful hello yall"\n', 'Response incorrect: {}'.format(response.text)

    def test_restful_one_version(self):
        response = requests.get(self.base_url + '/v1_0_0/restful_hello/1')

        assert response.status_code == 200, 'Response code incorrect: {}'.format(response.status_code)
        assert response.text == '"Restful hello 1"\n', 'Response incorrect: {}'.format(response.text)

    def test_current_version(self):
        response = requests.get(self.base_url + '/hello')

        assert response.status_code == 200, 'Response code incorrect: {}'.format(response.status_code)
        assert response.text == 'Hello v2.0.0', 'Response incorrect: {}'.format(response.text)

    def test_upload_process(self):
        test_filename = 'linear_data.txt'
        test_path = os.path.join(app_path, 'micro_service/test/data/' + test_filename)
        output_path = os.path.join(TestMicroService.config['upload_folder'], test_filename)
        self.remove_all_files(TestMicroService.config['upload_folder'])

        with open(test_path) as payload:
            url = self.base_url + '/upload_process'
            headers = {'X-CSRFToken': self.token, 'Referer': url}
            post_data = {'file': payload}
            response = self.session.post(url, files=post_data, headers=headers)

            assert response.status_code == 200, 'Response code incorrect: {}'.format(response.status_code)
            assert response.text == test_filename, 'Response incorrect: {}'.format(response.text)
            assert filecmp.cmp(test_path, output_path) == True, 'Received file is not the same as one sent'
            os.remove(output_path)

    def test_update_process(self):
        # TODO - finish this with DB
        url = self.base_url + '/update_process/1'
        headers = {'X-CSRFToken': self.token, 'Referer': url}
        post_data = {'key':'value'}
        response = self.session.post(url, data={'key':'value'}, headers=headers)

        assert response.status_code == 200, 'Response code incorrect: {}'.format(response.status_code)
        assert response.text == 'fred', 'Response incorrect: {}'.format(response.text)

    def test_process(self):
        # TODO - finish this with DB
        response = requests.get(self.base_url + '/process/1')

        assert response.status_code == 200, 'Response code incorrect: {}'.format(response.status_code)
        assert response.text == 'Hello v2.0.0', 'Response incorrect: {}'.format(response.text)


if __name__ == '__main__':
    unittest.main()