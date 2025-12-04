from datetime import datetime

def return_date_time():
  now = datetime.now()
  formatted = now.strftime("%Y%m%d%H%M")[:-3]  
  print(type(formatted))
  print("Current date and time:", formatted)
  return formatted

