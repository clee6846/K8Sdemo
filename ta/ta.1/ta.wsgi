#!/usr/bin/env python3.6
import sys
 
sys.path.append('/var/www/html/ta')
activate_this = '/var/www/html/ta/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this)) 
from ta import app as application
