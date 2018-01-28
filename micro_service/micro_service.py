# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    8.10.16   
#
# -----------------------------------------------------------------------------------------------


# Libraries
import os
import time
from datetime import datetime
import random

from werkzeug.utils import secure_filename

from flask import request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_seasurf import SeaSurf
from flask_cors import cross_origin, CORS

from micro_service import app_path
from micro_service.framework import load_config, setup_logger, create_flask_app
from micro_service.framework import register_versions, create_celery, allowed_file


from micro_service.db.models.process import Process


# Config
flask_env   = os.environ['ENV'].lower()
config      = load_config(flask_env)
logger      = setup_logger(config)
flask_app   = create_flask_app(config)
csrf        = SeaSurf(flask_app)
db          = SQLAlchemy(flask_app)
_           = register_versions(flask_app)
celery      = create_celery(flask_app)
_           = CORS(flask_app)



# Globals
# -----------------------------------------------------
async_tasks = []


# App code
# -----------------------------------------------------
@flask_app.route('/')
def root():
    return 'Root page'

@flask_app.route('/version')
def version():
    return config['version']

@flask_app.route('/long_task', methods=['POST'])
def long_task():
    task = long_task.apply_async()
    response = { 'url': url_for('long_task_status', task_id=task.id) }

    return jsonify(response), 202

@flask_app.route('/long_task_status/<task_id>', methods=['GET'])
def long_task_status(task_id):
    task = long_task.AsyncResult(task_id)
    response = {}

    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': task.info.get('end', 'problem')
        }
    else:
        response = {
            'state': task.state,
            'status': str(task.info)
        }

    return jsonify(response)

@flask_app.route('/process/<id>', methods=['GET'])
def process(id):
    processes = db.session.query(Process).filter(Process.id==id)

    if processes.count() > 0:
        return processes[0].to_json()

    return jsonify({})

@flask_app.route('/run_process/<id>', methods=['GET'])
def run_process(id):
    processes = db.session.query(Process).filter(Process.id==id)

    if processes.count() > 0:
        process = processes[0]
        process.start_time = datetime.now()

        db.session.add(process)
        db.session().commit()

        task = run_process.apply_async()
        response = { 'url': url_for('process_status', task_id=task.id) }
        async_tasks[task.id] = id

        return jsonify(response), 202

    return jsonify({}), 404

@flask_app.route('/process_status/<id>', methods=['GET'])
def process_status(id):
    task = run_process.AsyncResult(id)
    response = {}

    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': task.info.get('end', 'problem')
        }
    elif task.state == 'SUCCESS':
        process_dict = finish_process(id)

        response = {
            'state': task.state,
            'status': task.info.get('end', 'problem'),
            'process': process_dict
        }
    else:
        response = {
            'state': task.state,
            'status': str(task.info)
        }

    return jsonify(response)

@csrf.exempt
@flask_app.route('/upload_process', methods=['POST'])
@cross_origin(supports_credentials=True)
def upload_process():
    if 'file' not in request.files:
        return '', 400

    file = request.files['file']
    if file.filename == '':
        return '', 400

    if file and allowed_file(file.filename):
        return save_uploaded_file(file)

@csrf.exempt
@flask_app.route('/update_process/<id>', methods=['POST'])
@cross_origin(supports_credentials=True)
def update_process(id):
    return 'fred'
    #processes = db.session.query(Process).filter(Process.id==id)

    #if processes.count() > 0:
    #    process = processes[0]

    #    db.session.add(process)
    #    db.session().commit()


# Helper functions
# -----------------------------------------------------
@celery.task(bind=True, ignore_results=False)
def long_task(self):
    print('Starting long task...')
    for task_number in range(10):
        print(task_number)
        time.sleep(1)
    print('End long task')

    return { 'end': 'success' }

@celery.task(bind=True, ignore_results=False)
def run_process(self, length):
    print('Starting process...')

    for i in range(length):
        print('processed: {}'.format(i))
        time.sleep(1)

    print('End process')

    return { 'end': 'success' }

def finish_process(id):
    process_id = async_tasks[id]
    async_tasks.pop('key', id)

    if process_id:
        processes = db.session.query(Process).filter(Process.id==id)

        if processes.count() > 0:
            process = processes[0]
            process.total_records       = random.randint(0, 5000)  
            process.correct_records     = random.randint(0, process.total_records)    
            process.incorrect_records   = random.randint(0, process.total_records - process.correct_records)
            process.record_errors       = random.randint(0, process.total_records - process.correct_records - process.incorrect_records) 
            process.finish()

            db.session.add(process)
            db.session.commit()

            return process.to_dict()
    
    return {}

def save_uploaded_file(file):
    filename = secure_filename(file.filename)
    file_path = os.path.join(flask_app.config['UPLOAD_FOLDER'], filename)

    #file_upload = FileUpload(filename, file_path)
    #db.session.add(file_upload)
    #db.session.commit()

    file.save(file_path)
    if os.path.isfile(file_path):
        pass
        #file_upload.was_successful()
        #db.session.commit()
    else:
        return ('', 400)

    return filename
