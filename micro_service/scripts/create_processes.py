# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    8.16.16   
#
# -----------------------------------------------------------------------------------------------


# Libraries
from datetime import datetime


# Globals
# -------------------------------------------
start_index = 0
end_index = 100


# App
# -------------------------------------------
for x in range(start_index, end_index):
    p = Process()
    p.name = 'process_{}'.format(x)
    p.received_time = datetime.now()
    p.total_records = 1000

    session.add(p)
    session.commit()



