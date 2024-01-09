from datetime import datetime
import pytz

#####
"""Get the menu items"""
#####

today = datetime.now(pytz.timezone('America/Los_Angeles') ).strftime("%Y%m%d")
print(today)