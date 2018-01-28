# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    8.18.16   
#
# -----------------------------------------------------------------------------------------------


# Libraries
from flask import Blueprint


app_v2_0_0 = Blueprint('app_v2_0_0', __name__)

@app_v2_0_0.route('/hello')
def version_hello():
    return 'Hello v2.0.0'