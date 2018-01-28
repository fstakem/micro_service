# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    8.16.16   
#
# -----------------------------------------------------------------------------------------------


# Libraries
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, Numeric

from micro_service.db.models.api import Base
from micro_service.db.models.base_model import BaseModel

class Process(BaseModel, Base):

    id                  = Column(Integer, primary_key=True)
    name                = Column(String(100))
    received_time       = Column(DateTime)
    sent_time           = Column(DateTime)
    start_time          = Column(DateTime)
    end_time            = Column(DateTime)
    total_records       = Column(Integer, default=0)
    correct_records     = Column(Integer, default=0)
    incorrect_records   = Column(Integer, default=0)
    record_errors       = Column(Integer, default=0)
    correct_rate        = Column(Numeric(20, 2), default=0.0)
    incorrect_rate      = Column(Numeric(20, 2), default=0.0)
    error_rate          = Column(Numeric(20, 2), default=0.0)
    is_finished         = Column(Boolean, default=False)

    def finish(self):
        if self.total_records > 0:
            self.correct_rate   = self.correct_records    / float(self.total_records)
            self.incorrect_rate = self.incorrect_records  / float(self.total_records)
            self.error_rate     = self.record_errors      / float(self.total_records)

        self.end_time = datetime.now()
        self.is_finished = True


    __tablename__ = 'process'
