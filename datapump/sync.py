import os
import requests
import sys
import json
from itertools import groupby, islice
from datetime import datetime, timedelta
import time
from time import mktime


import logging


# *******************************************************************
# Debug Output defines
# Comment to enable/disable
# ********************************************************************
debug_all = True
#debug_all = False



#logging.basicConfig(level=logging.INFO)
#log = logging

logging.basicConfig(level=logging.ERROR)
log = logging

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as fbdb
from firebase_admin import _utils

from firebase_token_generator import create_token

print (dir(firebase_admin))
print (dir(fbdb))
#if debug_all: log.info('sync: urllib3.__version__ %s', urllib3.__version__)



FIREBASE_URL = os.environ.get('FIREBASE_URL')
DATABASE_URL = os.environ.get('DATABASE_URL')
#FIREBASE_URL = 'https://seasmart.firebaseio.com/'
#DATABASE_URL = 'postgres://ualt8moiqdgaub:p7b34e14108c71def0466518fa6934848d544b6dc6ce8dc69f744431b0e7c06ca@ec2-34-202-89-215.compute-1.amazonaws.com:5432/dd2l1kva0c5agd'


FIREBASE_HSMURL = 'https://helmsmart-device-message.firebaseio.com/'
FIREBASE_PCDINURL = 'https://helmsmart-ios-pcdin.firebaseio.com/'
#FIREBASE_SECRET = 'https://helmsmart-device-message.firebaseio.com/'

FIREBASE_SECRET = 'cjqRZsxi7Tlnge0pSxCKFwKfhsQBkYIkvIedz3bm'


auth_payload = {"uid": "1", "auth_data": "foo", "other_auth_data": "bar"}
options = {"admin": True}
fbtoken = create_token(FIREBASE_SECRET, auth_payload, options)

credential=credentials.Certificate({
    "type": os.environ.get('FIREBASE_TYPE').replace('\\n', '\n'),
    "project_id": os.environ.get('FIREBASE_PROJECT_ID').replace('\\n', '\n'),
    "private_key_id": os.environ.get('FIREBASE_PRIVATE_KEY_ID').replace('\\n', '\n'),
    "private_key": os.environ.get('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL').replace('\\n', '\n'),
    "client_id": os.environ.get('FIREBASE_CLIENT_ID').replace('\\n', '\n'),
    "auth_uri": os.environ.get('FIREBASE_AUTH_ID').replace('\\n', '\n'),
    "token_uri": os.environ.get('FIREBASE_TOKEN_URI').replace('\\n', '\n'),
    "auth_provider_x509_cert_url": os.environ.get('FIREBASE_AUTH_PROVIDER').replace('\\n', '\n'),
    "client_x509_cert_url": os.environ.get('FIREBASE_CERT_URL').replace('\\n', '\n')
  })
 
fbapp = firebase_admin.initialize_app(credential, { 'databaseURL': 'https://helmsmart-ios-pcdin.firebaseio.com'})


#fbapp = firebase_admin.initialize_app()

#TODO: make these consistant with the constants
# defined in nmea module, which ignores the 
# partition column
DEVICE=0
PARTITION=1
URL = 2
PGN = 3
TIMESTAMP=4
SOURCE=5


# JLB - 071019 - added pcdin event type to firebase store
def dump_pcdinfirebase(device, eventtype, partition, data):

  if debug_all: log.info('sync: dump_pcdinfirebase start %s:%s', partition, device)
  #if debug_all: log.info('sync: dump_pcdinfirebase %s:%s', device, data)
  
  #var gDeviceKey="001EC010AD69"; // WinChuckWiFI
  #var gDeviceKey="D8803920A828"; //netDimmer Winchuck
  #var gDeviceKey="001EC024647E"; // SeaDreram 4G
  #var gDeviceKey = "001EC04CF47B"; // netDimmer Hub
  #var gDeviceKey = "001EC0359C27"; // WIHELMSK
  

  #if device == '001EC010AD69' or device == '001EC024647E'  or device == 'D8803920A828' or device == '001EC04CF47B' or device == '001EC0359C27' :
  if device != None:

    
    if eventtype == 'SIGNALK':
      try:
        # **************************************************
        # For Signal K
        # **************************************************



        
        ref= firebase_admin.db.reference('/DEVICE/' + device + '/' + eventtype)

 
      except ValueError as e:
        if debug_all: log.info('Sync: dump_pcdinfirebase1 SignalK ValueError in data %s:  ', data)

        if debug_all: log.info('Sync: dump_pcdinfirebase1 SignalK ValueError in data %s:  ' % str(e))

        pass

      except NameError as e:
        if debug_all: log.info('Sync: dump_pcdinfirebase1 SignalK NameError in data %s:  ', data)

        if debug_all: log.info('Sync: dump_pcdinfirebase1 SignalK NameError in data %s:  ' % str(e))
        
      except TypeError as e:
        if debug_all: log.info('Sync: dump_pcdinfirebase1 SignalK TypeError in data %s:  ', data)

        if debug_all: log.info('Sync: dump_pcdinfirebase1 SignalK TypeError in data %s:  ' % str(e))

      except AttributeError as e:
        if debug_all: log.info('Sync: dump_pcdinfirebase1 SignalK AttributeError in data %s:  ', data)

        if debug_all: log.info('Sync: dump_pcdinfirebase1 SignalK AttributeError in data %s:  ' % str(e))

      except:
        if debug_all: log.info('sync: dump_pcdinfirebase1 SignalK error %s:%s', partition, device)
        e = sys.exc_info()[0]

        if debug_all: log.info("Error: %s" % str(e))
        pass
      
    else:
      try:
        # **************************************************
        # For JSON and PCDIN 
        # **************************************************
        
        ref= firebase_admin.db.reference('/DEVICE/' + device + '/' + eventtype)
        #myDeviceData = {eventtype:data}
        myjson={eventtype:data}

        if debug_all: log.info('sync: dump_pcdinfirebase json %s:%s', eventtype, device)
        if debug_all: log.info('sync: dump_pcdinfirebase json %s:%s', device, data)

        
        ref.set(json.loads(data))

      except AttributeError as e:
        if debug_all: log.info('Sync: dump_pcdinfirebase1 AttributeError in data %s:  ', data)

        if debug_all: log.info('Sync: dump_pcdinfirebase1 AttributeError in data %s:  ' % str(e))


      except NameError as e:
        if debug_all: log.info('Sync: dump_pcdinfirebase1 NameError in data %s:  ', data)

        if debug_all: log.info('Sync: dump_pcdinfirebase1 NameError in data %s:  ' % str(e))

        

      except:
        if debug_all: log.info('sync: dump_pcdinfirebase1 error %s:%s', partition, device)
        e = sys.exc_info()[0]

        if debug_all: log.info("Error: %s" % str(e))


  
