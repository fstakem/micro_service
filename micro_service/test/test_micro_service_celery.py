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
import json
from multiprocessing import Process
import requests

from celery import current_app
from celery.bin import worker
from celery.task.control import discard_all

from micro_service.micro_service import flask_app


class TestMicroService(unittest.TestCase):

    @classmethod
    def setupClass(cls):
        cls.host = '127.0.0.1'
        cls.port = '5000'

    @classmethod
    def tearDownClass(cls):
        pass

    def setup(self):
        self.create_simple_webserver()
        self.create_rabbitmq()
        self.base_url = 'http://{}:{}/'.format(TestMicroService.host, TestMicroService.port)

    def tearDown(self):
        self.teardown_rabbitmq()
        self.teardown_simple_webserver()

    # Helper functions
    # -----------------------------------------------------
    def create_simple_webserver(self):
        self.web_server_process = Process(target=flask_app.run, kwargs={'debug': False}, name='server')
        self.web_server_process.start()
        time.sleep(1)

    def teardown_simple_webserver(self):
        self.web_server_process.terminate()

    def create_rabbitmq(self):
        self.rabbitmq_process = Process(target=self.run_rabbitmq)
        self.rabbitmq_process.start()
        time.sleep(1)
        discard_all()

    def teardown_rabbitmq(self):
        self.rabbitmq_process.terminate()

    def run_rabbitmq(self):
        w = worker.worker(app=celery)
        options = {
            'broker': flask_app.config['CELERY_BROKER_URL'],
            'loglevel': 'INFO',
            'traceback': True
        }
        w.run(**options)

    def get_session(self):
        session = requests.Session()
        session.get(self.base_url)
        token = session.cookies['_csrf_token']

        return (session, token)

    def get_task_response(url_ending):
        response = requests.get(self.base_url + url_ending)
        response_data = json.loads(response.text)

        return response_data

    # Tests functions
    # -----------------------------------------------------
    def test_long_task(self):
        session, token = self.get_session()
        url = self.base_url + 'long_task'
        headers = { 'X-CSRFToken': token, 'Referer': url }
        response = session.post(url, headers=headers)

        assert response.status_code == 202, 'Response code was incorrect'

        start_task = json.loads(response.text)
        response_data = get_task_response(start_task['url'])

        assert response_data['status'] == 'Pending...', 'The initial task status was incorrect'
        assert response_data['state'] == 'PENDING', 'The initial task state is incorrect'
        time.sleep(12)

        response_data = get_task_response(start_task['url'])

        assert response_data['status'] == 'success', 'The final task status was incorrect'
        assert response_data['state'] == 'SUCCESS', 'The final task state is incorrect'

    def test_run_process(self):
        pass