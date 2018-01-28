# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    8.11.16   
#
# -----------------------------------------------------------------------------------------------


# Libraries
from flask import Blueprint
from flask_restful import Api, Resource, url_for


app_v1_0_0 = Blueprint('app_v1_0_0', __name__)

@app_v1_0_0.route('/hello')
def version_hello():
    return 'Hello v1.0.0'


# Restful
rest_api = Api(app_v1_0_0)

class RestfulHellos(Resource):

    def get(self):
        return 'Restful hello yall'


class RestfulHello(Resource):

    def get(self, id):
        return 'Restful hello {}'.format(id)

rest_api.add_resource(RestfulHellos, '/restful_hello')
rest_api.add_resource(RestfulHello, '/restful_hello/<int:id>')