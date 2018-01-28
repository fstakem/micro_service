# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    8.19.16   
#
# -----------------------------------------------------------------------------------------------


# Libraries
import os

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, Numeric

from micro_service.db.models.api import Base
from micro_service.db.models.base_model import BaseModel

class FileUpload(BaseModel, Base):

    id                  = Column(Integer, primary_key=True)
    name                = Column(String(100))
    path                = Column(String(500))
    size                = Column(Integer, default=0)
    size_mb             = Column(Numeric(20, 2), default=0.0)
    successful          = Column(Boolean, default=False)



    def __init__(self, name, path):
        self.name = name
        self.path = path

    def was_successful(self):
        self.size           = os.stat(self.path).st_size
        self.size_mb        = self.size / 1048576.0
        self.successful     = True

    __tablename__ = 'file_upload'