# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    8.11.16   
#
# -----------------------------------------------------------------------------------------------


# Libraries
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import os 
import sys

from midmod.framework import load_config


# Load config
flask_env   = os.environ['ENV'].lower()
config      = load_config(flask_env)

# Setup system to find modules
print('')
print('Starting ipython with SQLAlchemy ->')
#working_dir = os.getcwd()
#sys.path.append(working_dir)
#sys.path.append(os.path.join(working_dir, 'db', 'models'))

# Import models
#from midmod.db.models.x import X

# Get password
db_password = os.environ['DB_PASSWORD']
db_connection_str = 'postgresql://{}:{}@{}/{}'.format(config['db_user'], db_password, config['db_host'], config['db_name'])

# Connect to db
print('Connecting to DB...')
engine = create_engine(db_connection_str)
engine.connect()
print('Connection successful')

# Create session
print('Creating session...')
SessionFactory = sessionmaker(bind=engine)
session = SessionFactory()
print('Session successfully created')