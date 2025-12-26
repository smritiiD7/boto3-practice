from datetime import datetime
from enum import Enum

class FileTypeEnum(Enum):
    JPG = 'jpg'
    JPEG = 'jpeg'
    PNG = 'png'
    PDF = 'pdf'
    CSV = 'csv'
    OTHER = 'other'

class FileStatusEnum(Enum):
   FILE_MANUALLY_UPLOADED = 'FILE_MANUALLY_UPLOADED'
   FILE_TRANSFERRED_TO_DESTINATION = 'FILE_TRANSFERRED_TO_DESTINATION'
   FILE_DELETED_FROM_SOURCE = 'FILE_DELETED_FROM_SOURCE'


def return_date_time():
  now = datetime.now()
  formatted = now.strftime("%Y%m%d%H%M")[:-3]  
  print(type(formatted))
  print("Current date and time:", formatted)
  return formatted

