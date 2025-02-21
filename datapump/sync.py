import os
import requests
import sys
import json
from itertools import groupby, islice
from datetime import datetime, timedelta
import time
from time import mktime
from signalk import createSIGKpath

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
#DATABASE_URL = os.environ.get('HEROKU_POSTGRESQL_MAUVE_URL')
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


from influxdb import InfluxDBClient as InfluxDBCloud
from influxdb.client import InfluxDBClientError
from influxdb.client import InfluxDBServerError

#from influxdb_client import InfluxDBClient
#from influxdb_client import Point, WritePrecision
#from influxdb_client.client.write_api import SYNCHRONOUS

from influxdb_client_3 import InfluxDBClient3, Point



from splicer import Schema, Field




#TODO: make these consistant with the constants
# defined in nmea module, which ignores the 
# partition column
DEVICE=0
PARTITION=1
URL = 2
PGN = 3
TIMESTAMP=4
SOURCE=5

class DateEncoder(json.JSONEncoder):
  def default(self, obj):
    if hasattr(obj, 'isoformat'):
      return obj.isoformat()
    else:
      return str(obj)

def ensure_database(conn, schema):
 
  fact_info = [
    (i,fact_schema(f))
    for i,f in enumerate(schema.fields)
    if f.type == "RECORD"
  ]

  #cursor = conn.cursor()

  #execute_stmts(cursor, ensure_tables(fact_info))
  #conn.commit()
  #execute_stmts(cursor, ensure_data(conn))
  #conn.commit()

  return fact_info


def fact_schema(fact_field):
  """
  Given a pgn field creates the schema appropriate for
  housing it in the warehouse.
  """
  #020614 JLB added datetime_id field
  header = [
    Field(name='partition', type='STRING'),
    Field(name="date_id", type="INTEGER"),
    Field(name="time_id", type="INTEGER"),
    Field(name="datetime_id", type="INTEGER"), 
    Field(name="device", type="VARCHAR"),    
    Field(name="source", type="VARCHAR"),
    Field(name="event_timestamp", type="DATETIME")
  ]
  return Schema(header + fact_field.fields, name=fact_field.name)
    

def dump_json(schema, records):
  field_pos = list(enumerate(schema.fields[3:]))
  
  def to_dict(record):
 
    data =  {
      f.name:record[i]
      for i,f in field_pos[:3]
    }

    for i,f in field_pos[3:]:
      v = record[i]
      if v:
        data['payload'] = v
        data['description'] = f.name
        return data



  data = [to_dict(r) for r in records]
  #if debug_all: log.info('data =  %s ', data)
  return json.dumps(data, cls=DateEncoder)

"""
# Used for PGs 130311
def getSKTemperatureInstance(pgn_type, pgn_instance):

  path = ""
  pgninstanceString = ""
  
  if pgn_instance != "":
    pgninstanceString = str(pgn_instance) + '.'
  
  if pgn_type == 'Sea Temperature': 
    path = 'environment.water.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Temperature': 
    path = 'environment.outside.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Temperature': 
    path = 'environment.inside.' + pgninstanceString + 'temperature'
    
  elif pgn_type == 'Engine Room Temperature': 
    path = 'environment.inside.engineRoom.' + pgninstanceString + 'temperature'
 
  elif pgn_type == 'Main Cabin Temperature': 
    path = 'environment.inside.mainCabin.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Live Well': 
    path= 'tanks.liveWell.default.' + pgninstanceString + 'temperature'
    #pathWithIndex: 'tanks.liveWell.<index>.temperature'

  elif pgn_type == 'Bait Well': 
    path = 'tanks.baitWell.default.' + pgninstanceString + 'temperature'
    #pathWithIndex: 'tanks.baitWell.<index>.temperature'

  elif pgn_type == 'Refridgeration': 
    path = 'environment.inside.refrigerator.' + pgninstanceString + 'temperature'

  elif pgn_instance == 'Heating': 
    path = 'environment.inside.heating.' + pgninstanceString + 'temperature'

  elif pgn_instance == 'Dew Point': 
    path = 'environment.outside.' + pgninstanceString + 'dewPointTemperature'

  elif pgn_instance == 'Wind Chill A': 
    path = 'environment.outside.' + pgninstanceString + 'apparentWindChillTemperature'

  elif pgn_instance == 'Wind Chill T': 
    path = 'environment.outside.' + pgninstanceString + 'theoreticalWindChillTemperature'

  elif pgn_type == 'Heat Index': 
    path = 'environment.outside.' + pgninstanceString + 'heatIndexTemperature'

  elif pgn_type == 'Freezer': 
    path = 'environment.inside.freezer.' + pgninstanceString + 'temperature'
 
  elif pgn_type == 'EGT': 
    path = 'propulsion.exhaust.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Reserved 128': 
    path = 'propulsion.manifold.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Reserved 129': 
    path = 'propulsion.fuel.supply.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Reserved 130': 
    path = 'propulsion.fuel.return.' + pgninstanceString + 'temperature'
    
    
  elif pgn_type == 'Reserved 134': 
    path = 'propulsion.egt.manifold.' + pgninstanceString + 'temperature'
    
  elif pgn_type == 'Fuel Flow': 
    path = 'propulsion.fuelflow.' + pgninstanceString + 'temperature'    

  elif pgn_type == 'Inside Zone0': 
    path = 'environment.inside.0.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone1': 
    path = 'environment.inside.1.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone2': 
    path = 'environment.inside.2.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone3': 
    path = 'environment.inside.3.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone4': 
    path = 'environment.inside.4.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone5': 
    path = 'environment.inside.5.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone6': 
    path = 'environment.inside.6.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone7': 
    path = 'environment.inside.7.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone8': 
    path = 'environment.inside.8.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone9': 
    path = 'environment.inside.9.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone10': 
    path = 'environment.inside.10.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone11': 
    path = 'environment.inside.11.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone12': 
    path = 'environment.inside.12.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone13': 
    path = 'environment.inside.13.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone14': 
    path = 'environment.inside.14.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Inside Zone15': 
    path = 'environment.inside.15.' + pgninstanceString + 'temperature'
    
  elif pgn_type == 'Outside Zone0': 
    path = 'environment.outside.0.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone1': 
    path = 'environment.outside.1.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone2': 
    path = 'environment.outside.2.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone3': 
    path = 'environment.outside.3.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone4': 
    path = 'environment.outside.4.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone5': 
    path = 'environment.outside.5.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone6': 
    path = 'environment.outside.6.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone7': 
    path = 'environment.outside.7.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone8': 
    path = 'environment.outside.8.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone9': 
    path = 'environment.outside.9.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone10': 
    path = 'environment.outside.10.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone11': 
    path = 'environment.outside.11.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone12': 
    path = 'environment.outside.12.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone13': 
    path = 'environment.outside.13.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone14': 
    path = 'environment.outside.14.' + pgninstanceString + 'temperature'

  elif pgn_type == 'Outside Zone15': 
    path = 'environment.outside.15.' + pgninstanceString + 'temperature'
    

  return path

# Used for PGs 130311
def getSKHumidityInstance(pgn_instance):

  path = ""
  
  if pgn_instance == 'Inside Humidity': 
    path = 'environment.inside.humidity'

  elif pgn_instance == 'Outside Humidity': 
    path = 'environment.outside.humidity'

  elif pgn_instance == 'Reserved': 
    path = 'environment.outside.humidity'

  return path

# Used fro PGNs 130306
def getSKWindSpeedInstance(pgn_instance):

  path = ""
  
  if pgn_instance == 'TWIND True North': 
    path = 'environment.wind.speedTrue'

  elif pgn_instance == 'TWIND Mag North': 
    path = 'environment.wind.speedTrue'

  elif pgn_instance == 'Apparent Wind': 
    path = 'environment.wind.speedApparent'
    
  elif pgn_instance == 'TWIND VCGR': 
    path = 'environment.wind.speedOverGround'


  return path

# Used fro PGNs 130306
def getSKWindDirectionInstance(pgn_instance):

  path = ""
  
  if pgn_instance == 'TWIND True North': 
    path = 'environment.wind.directionTrue'

  elif pgn_instance == 'TWIND Mag North': 
    path = 'environment.wind.directionMagnetic'

  elif pgn_instance == 'Apparent Wind': 
    path = 'environment.wind.angleTrueWater'

  return path

# Used fro PGNs 129026
def getSKCOGInstance(pgn_instance):

  path = ""
  
  if pgn_instance == 'True': 
    path = 'navigation.courseOverGroundTrue'

  elif pgn_instance == 'Magnetic': 
    path = 'navigation.courseOverGroundMagnetic'


  return path


 # Converts NMEA 2000 field descriptions to Signal 

def createSIGKpath(pgn_number, n2kkey, pgn_payload):

  
  skpath_json = {}

  try:
      
    # ********************************************************************************************
    # Environmential Data  
    if pgn_number == 130311:
      #if debug_all: log.info('sync: createSIGKpath 130311 %s:%s', n2kkey, pgn_payload.get('temperature_instance'))
      
      if n2kkey == 'temperature':
        skpath = getSKTemperatureInstance(pgn_payload.get('temperature_instance'), "")
        if pgn_payload.get('temperature') is not None:
          skvalue = pgn_payload.get('temperature')
          skpath_json = {"path":skpath,"value":skvalue}
        else:
          return {}

      elif n2kkey == 'atmospheric_pressure':
        skpath = 'environment.outside.pressure'
        if pgn_payload.get('atmospheric_pressure') is not None:
          skvalue = pgn_payload.get('atmospheric_pressure')
          skpath_json = {"path":skpath,"value":skvalue}
        else:
          return {}

      elif n2kkey == 'humidity':
        skpath = getSKHumidityInstance(pgn_payload.get('humidity_instance'))        
        if pgn_payload.get('humidity') is not None:
          skvalue = ( pgn_payload.get('humidity') / 100)
          skpath_json = {"path":skpath,"value":skvalue}
        else:
          return {}

    # ********************************************************************************************

   


    # ********************************************************************************************
    # End of   createSIGKpath 
    return skpath_json
    # ********************************************************************************************

  except NameError as e:
    if debug_all: log.info('Sync: createSIGKpath SignalK NameError in data %s:  ', data)

    if debug_all: log.info('Sync: createSIGKpath SignalK NameError in data %s:  ' % str(e))
    pass
    
  except TypeError as e:
    if debug_all: log.info('Sync: createSIGKpath SignalK TypeError in data %s:  ', data)

    if debug_all: log.info('Sync: createSIGKpath SignalK TypeError in data %s:  ' % str(e))
    pass

  except AttributeError as e:
    if debug_all: log.info('Sync: createSIGKpath SignalK AttributeError in data %s:  ', data)

    if debug_all: log.info('Sync: createSIGKpath SignalK AttributeError in data %s:  ' % str(e))
    pass

  except:
    if debug_all: log.info('sync: createSIGKpath SignalK error %s:%s', partition, device)
    e = sys.exc_info()[0]

    if debug_all: log.info("Error: %s" % e)
    pass

  return skpath_json


"""

    
def convert_influxdbcloud_json(mytime, value, key):

  try:

    #mydtt = time.strptime(mytime, "%Y-%m-%d %H:%M:%S")    
    #mydtt = datetime.strptime(mytime, "%Y-%m-%d %H:%M:%S")
    #"2009-11-10T23:00:00Z"
    mydtt = mytime.timetuple()
    ts = int(mktime(mydtt) * 1000)
    #ts = mytime.replace(' ','T')
    #ts = ts + 'Z'


    

    tagpairs = key.split(".")
    #if debug_all: log.info('freeboard: convert_influxdbcloud_json tagpairs %s:  ', tagpairs)

    myjsonkeys={}
    #deviceid
    tag0 = tagpairs[0].split(":")
    #sensor
    tag1 = tagpairs[1].split(":")
    #source
    tag2 = tagpairs[2].split(":")
    #instance
    tag3 = tagpairs[3].split(":")
    #type
    tag4 = tagpairs[4].split(":")
    #parameter
    tag5 = tagpairs[5].split(":")

    #"deviceid:001EC010AD69.sensor:environmental_data.source:0.instance:0.type:Outside_Temperature.parameter:temperature.HelmSmart"
    #myjsonkeys = { 'deviceid':tag0[1], 'sensor':tag1[1], 'source':tag2[1], 'instance':tag3[1], 'type':tag4[1], 'parameter':tag5[1]}
    myjsonkeys = { 'deviceid':tag0[1], 'sensor':tag1[1], 'instance':tag3[1], 'type':tag4[1], 'parameter':tag5[1]}
    #if debug_all: log.info('freeboard: convert_influxdbcloud_json tagpairs %s:  ', myjsonkeys)

    #values = {'value':value}
    values = {tag5[1]:value, 'source':tag2[1]}
    measurement = 'HS_'+str(tag0[1])
    #ifluxjson ={"measurement":tagpairs[6], "time": ts, "tags":myjsonkeys, "fields": values}
    ifluxjson ={"measurement":measurement, "time": ts, "tags":myjsonkeys, "fields": values}
    #if debug_all: log.info('freeboard: convert_influxdbcloud_json %s:  ', ifluxjson)

    return ifluxjson

  except AttributeError as e:
    if debug_all: log.info('Sync: AttributeError in convert_influxdbcloud_json %s:  ', mytime)
    #e = sys.exc_info()[0]

    if debug_all: log.info('Sync: AttributeError in convert_influxdbcloud_json %s:  ' % str(e))
    
  except TypeError as e:
    if debug_all: log.info('Sync: TypeError in convert_influxdbcloud_json %s:  ', mytime)
    #e = sys.exc_info()[0]

    if debug_all: log.info('Sync: TypeError in convert_influxdbcloud_json %s:  ' % str(e))
    
  except NameError as e:
    if debug_all: log.info('Sync: NameError in convert_influxdbcloud_json %s:  ', mytime)
    #e = sys.exc_info()[0]

    if debug_all: log.info('Sync: NameError in convert_influxdbcloud_json %s:  ' % str(e))
    
  except:
    if debug_all: log.info('Sync: Error convert_influxdbcloud_json %s:', mytime)

    e = sys.exc_info()[0]
    if debug_all: log.info("Sync.py Error in convert_influxdbcloud_json: %s" % e)



#083016 JLB added to convert PushSmart record to influxdb cloudJSON
def convert_influxdb_cloud_tcpjson(value,  key):
  ifluxjson ={}
  
  try:

    PGN = "000000"
    #mydtt = datetime.strptime(mytime, "%Y-%m-%d %H:%M:%S")

    #dtt = mytime.timetuple()
    #ts = int(mktime(dtt) * 1000)
    ts = int(time.time() * 1000)

    """
    cols = []
    cols.append('time')
    cols.append('psvalue')

    
    vals = []
    vals.append(ts)
    vals.append(value)
    ifluxjson ={"points": [vals], "name":key, "columns": cols}
    """
    #key = 'deviceid:{}.sensor:tcp.source:0.instance:0.type:pushsmart.parameter:raw.HelmSmart'.format(deviceid)

    valuepairs = value.split(",")
    # check if we have proper formatted pushsmart string
    if len(valuepairs) != 5:
      PGN = "000001"
      values = {'raw':'***' + value}

    elif valuepairs[0] != '$PCDIN':
      PGN = "000002"
      values = {'raw':'***' + value}

    #Check PGN length is correct
    elif len(valuepairs[1]) != 6:
      PGN = "000003"
      values = {'raw':'***' + value}

    #check if timestamp length is correct
    elif len(valuepairs[2]) != 8:
      PGN = "000004"
      values = {'raw':'***' + value}

    #check if source length is correct
    elif len(valuepairs[3]) != 2:
      PGN = "000005"
      values = {'raw':'***' + value}

    #check if payload is terminated with * checksum
    elif len(valuepairs[4]) < 8:    
      PGN = "000006"
      values = {'raw':'***' + value}

    #check if payload is terminated with * checksum
    elif (valuepairs[4][len(valuepairs[4])-3] != '*') and (valuepairs[4][len(valuepairs[4])-4] != '*'):
    #elif valuepairs[4].find('*') == -1:    
      PGN = "000007"
      values = {'raw':'***' + value}

    else:
      PGN = valuepairs[1]
      values = {'raw':value}


      
    #Example KEY
    #key = 'deviceid:{}.sensor:tcp.source:0.instance:0.type:pushsmart.parameter:raw.HelmSmart'.format(deviceid)
    tagpairs = key.split(".")
    #log.info('freeboard: convert_influxdbcloud_json tagpairs %s:  ', tagpairs)

    myjsonkeys={}

    tag0 = tagpairs[0].split(":")
    tag1 = tagpairs[1].split(":")
    tag2 = tagpairs[2].split(":")
    tag3 = tagpairs[3].split(":")
    tag4 = tagpairs[4].split(":")
    tag5 = tagpairs[5].split(":")

    #"deviceid:001EC010AD69.sensor:environmental_data.source:0.instance:0.type:Outside_Temperature.parameter:temperature.HelmSmart"
    #myjsonkeys = { 'deviceid':tag0[1], 'sensor':tag1[1], 'source':tag2[1], 'instance':tag3[1], 'type':tag4[1], 'parameter':tag5[1]}
    myjsonkeys = { 'deviceid':tag0[1], 'sensor':tag1[1], 'source':tag2[1], 'instance':tag3[1], 'type':PGN, 'parameter':'raw'}
    #log.info('freeboard: convert_influxdbcloud_json myjsonkeys %s:  ', myjsonkeys)

    #values = {'value':value}
    #values = {tag5[1]:value}
    measurement = 'HS_'+str(tag0[1])+'_raw'
    #ifluxjson ={"measurement":tagpairs[6], "time": ts, "tags":myjsonkeys, "fields": values}
    ifluxjson ={"measurement":measurement, "time": ts, "tags":myjsonkeys, "fields": values}
    #log.info('freeboard: convert_influxdbcloud_json %s:  ', ifluxjson)


    return ifluxjson

  except AttributeError as e:
    if debug_all: log.info('Sync: AttributeError in convert_influxdb_cloud_tcpjson %s:  ', mytime)
    #e = sys.exc_info()[0]

    if debug_all: log.info('Sync: AttributeError in convert_influxdb_cloud_tcpjson %s:  ' % str(e))
    
  except TypeError as e:
    if debug_all: log.info('Sync: TypeError in convert_influxdb_cloud_tcpjson %s:  ', mytime)
    #e = sys.exc_info()[0]

    if debug_all: log.info('Sync: TypeError in convert_influxdb_cloud_tcpjson %s:  ' % str(e))
    
  except NameError as e:
    if debug_all: log.info('Sync: NameError in convert_influxdb_cloud_tcpjson %s:  ', mytime)
    #e = sys.exc_info()[0]

    if debug_all: log.info('Sync: NameError in convert_influxdb_cloud_tcpjson %s:  ' % str(e))
    
  except:
    if debug_all: log.info('Sync: Error convert_influxdb_cloud_tcpjson %s:', mytime)

    e = sys.exc_info()[0]
    if debug_all: log.info("Sync.py Error in convert_influxdb_cloud_tcpjson: %s" % e)


#022025 JLB added influxdb Cloud insert test
def insert_influxdbCloud_TCPseries(deviceid, message):
  if debug_all: log.info("start of insert_influxdbCloud_TCPseries insert...")

  try:
    
    IFDBCToken = os.environ.get('InfluxDBCloudToken')
    IFDBCOrg = os.environ.get('InfluxDBCloudOrg')
    IFDBCBucket = os.environ.get('InfluxDBCloudBucket')
    IFDBCURL = os.environ.get('InfluxDBCloudURL')

    IFDBhost = os.environ.get('IFDBhost')
    IFDBport = os.environ.get('IFDBport')
    IFDBusername = os.environ.get('IFDBusername')
    IFDBpassword = os.environ.get('IFDBpassword')
    IFDBdatabase = os.environ.get('IFDBdatabase')
    database="PushSmart_TCP"
    
    #shim = Shim(host, port, username, password, database)
    #db = influxdb.InfluxDBClient(host, port, username, password, database)
    #dbc = InfluxDBCloud(IFDBhost, IFDBport, IFDBusername, IFDBpassword, IFDBdatabase,  ssl=True)

    #dbc = InfluxDBCloud(url=IFDBCURL, token=IFDBCToken)
    client = InfluxDBClient3(host=IFDBCURL, token=IFDBCToken, org=IFDBCOrg)


    data = {
      "point1": {
        "deviceid": "001EC010AD69",
        "source": "82",
        "raw": "$PCDIN,01FD09,E7K6OT0A,82,FF410001A555FFFF*45",
      },
      "point2": {
        "deviceid": "001EC010AD69",
        "source": "82",
        "raw": "$PCDIN,01FD07,E7K6OT05,82,FF41A76CA5550504*3C",
      },
      "point3": {
        "deviceid": "001EC010AD69",
        "source": "82",
        "raw": "$PCDIN,01FD06,E7K6OT04,82,FFFFFFA76C0504FF*4D",
      },
      "point4": {
        ",deviceid": "001EC010AD69",
        "source": "82",
        "raw": "$PCDIN,01FD02,E7K6OT03,82,FF240051B2F8FFFF*40",
      },
    }

    for key in data:
      point = (
        Point("HS_001EC010AD69_raw")
        .tag("deviceid", data[key]["deviceid"])
        .field(data[key]["source"], data[key]["raw"])
      )
      client.write(database=database, record=point)




    #client.write(database=database, record=point)

    #client = InfluxDBClient(url=IFDBCURL, token=IFDBCToken)  

  except InfluxDBClientError as e:
    if debug_all: log.info('Sync: inFlux error in insert_influxdbCloud_TCPseries write %s:  ' % str(e))
    
  except TypeError as e:
    if debug_all: log.info('Sync: TypeError in insert_influxdbCloud_TCPseries write %s:  ', deviceid)
    #e = sys.exc_info()[0]

    if debug_all: log.info('Sync: TypeError in insert_influxdbCloud_TCPseries write %s:  ' % str(e))
    
  except KeyError as e:
    if debug_all: log.info('Sync: KeyError in insert_influxdbCloud_TCPseries write %s:  ', deviceid)
    #e = sys.exc_info()[0]

    if debug_all: log.info('Sync: KeyError in insert_influxdbCloud_TCPseries write %s:  ' % str(e))   
    
  except:
    if debug_all: log.info('Sync: Error in insert_influxdbCloud_TCPseries write %s:  ', deviceid)
    e = sys.exc_info()[0]
    if debug_all: log.info("Error: %s" % e)
    
  if debug_all: log.info("inserted into insert_influxdbCloud_TCPseries!")



  
#101414 JLB added influxdb insert test
def insert_influxdb_TCPseries(deviceid, message):
  if debug_all: log.info("start of influxdb_TCPseries insert...")
  """
  host = 'pinheads-wedontneedroads-1.c.influxdb.com' 
  port = 8086
  username = 'root'
  password = 'c73d5a8b1b07d17b'
  database = 'pushsmart'
  database = 'pushsmart-final'
  key = 'deviceid:{}.sensor:tcp.source:0.instance:0.type:pushsmart.parameter:raw.HelmSmart'.format(deviceid)
  

  db = InfluxDBClient(host, port, username, password, database)
  """
  
  #IFDBhost = 'hilldale-670d9ee3.influxcloud.net' 
  #IFDBport = 8086
  #IFDBusername = 'helmsmart'
  #IFDBpassword = 'Salm0n16'
  #IFDBdatabase = 'pushsmart-raw'

  IFDBhost = os.environ.get('IFDBhost')
  IFDBport = os.environ.get('IFDBport')
  IFDBusername = os.environ.get('IFDBusername')
  IFDBpassword = os.environ.get('IFDBpassword')
  IFDBdatabase = os.environ.get('IFDBdatabase')
  
  
  #shim = Shim(host, port, username, password, database)
  #db = influxdb.InfluxDBClient(host, port, username, password, database)
  dbc = InfluxDBCloud(IFDBhost, IFDBport, IFDBusername, IFDBpassword, IFDBdatabase,  ssl=True)
  
  key = 'deviceid:{}.sensor:tcp.source:0.instance:0.type:pushsmart.parameter:raw.HelmSmart'.format(deviceid)
  
  tcpmessages = message.split("\r\n")

  influxdata = []
  for record in tcpmessages:
    
    influxdata_record = convert_influxdb_cloud_tcpjson(record,  key)
    
    if influxdata_record != {}:
      influxdata.append(influxdata_record)

  #if debug_all: log.info("influxdb_TCPseries:%s", influxdata )
  
  try:
    #if debug_all: log.info('Sync:  InfluxDB write points ')
    if debug_all: log.info('Sync:  InfluxDB write TCP points %s',deviceid)
    #if debug_all: log.info('Sync:  InfluxDB write %s:  ', mydata)
    #db.write_points_with_precision(influxdata, time_precision='ms')
    dbc.write_points(influxdata, time_precision='ms')
    
    log.info('Sync:  InfluxDB RAW TCP write points %s', len(influxdata))
    
  except InfluxDBClientError as e:
    if debug_all: log.info('Sync: inFlux error in influxdb_TCPseries write %s:  ' % str(e))
    
  except TypeError as e:
    if debug_all: log.info('Sync: TypeError in influxdb_TCPseries write %s:  ', influxdata)
    #e = sys.exc_info()[0]

    if debug_all: log.info('Sync: TypeError in influxdb_TCPseries write %s:  ' % str(e))
    
  except KeyError as e:
    if debug_all: log.info('Sync: KeyError in influxdb_TCPseries write %s:  ', influxdata)
    #e = sys.exc_info()[0]

    if debug_all: log.info('Sync: KeyError in influxdb_TCPseries write %s:  ' % str(e))   
    
  except:
    if debug_all: log.info('Sync: Error in influxdb_TCPseries write %s:  ', influxdata)
    e = sys.exc_info()[0]
    if debug_all: log.info("Error: %s" % e)
    
  if debug_all: log.info("inserted into influxdb_TCPseries!")    
      





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


        skupdates = []

        json_data = json.loads(data)
        
        for record in json_data:
          
          if debug_all: log.info('sync: dump_pcdinfirebase SignalK record %s:%s', device, record)
          
          json_record = {}
          if record != None:
            json_record = record
          
          if debug_all: log.info('sync: dump_pcdinfirebase SignalK record %s:%s', device, json_record)



          n2kpgn = int(json_record.get('pgn', 'NULL'), 16)
          if debug_all: log.info('sync: dump_pcdinfirebase SignalK n2kpgn %s:%s', device, n2kpgn)
          
          n2kdescription = json_record.get('description', 'NULL')
          if debug_all: log.info('sync: dump_pcdinfirebase SignalK n2kdescription %s:%s', device, n2kdescription)
          
          n2ksource = json_record.get('source', 'NULL')
          if debug_all: log.info('sync: dump_pcdinfirebase SignalK n2ksource %s:%s', device, n2ksource)
          
          n2ktimestamp = json_record.get('timestamp', 'NULL')
          if debug_all: log.info('sync: dump_pcdinfirebase SignalK n2ktimestamp %s:%s', device, n2ktimestamp)

          n2kpayload = json_record.get('payload', 'NULL')
          if debug_all: log.info('sync: dump_pcdinfirebase SignalK n2kpayload %s:%s', device, n2kpayload)

          n2kkeys = n2kpayload.keys()
          if debug_all: log.info('sync: dump_pcdinfirebase SignalK n2kkeys %s:%s', device, n2kkeys)

          for n2kkey in n2kkeys:
            n2kvalue = n2kpayload.get(n2kkey, 'NULL')

            if debug_all: log.info('sync: dump_pcdinfirebase SignalK n2kvalue %s:%s', n2kkey, n2kvalue)
            

            #skupdates = []
            skvalues= []

            skcontext = "vessels.urn:mrn:imo:mmsi:338184312"
          

            #sksource = {"label":"antisense","type":"NMEA2000","pgn":127250,"src":"204"}
            #sktimestamp = "2019-07-12T18:32:54.134Z"

            sksource = {"label":"chetcodigital","type":"NMEA2000","pgn":n2kpgn,"src":n2ksource}
            #sktimestamp = "2019-07-12T18:32:54.134Z"
            sktimestamp = n2ktimestamp

            #skvalues.append({"path":"navigation.headingMagnetic","value":1.8979})
            #skpath =  n2kdescription + '.' + n2kkey
            #skvalues.append({"path":skpath,"value":n2kvalue})
            
            skpathjson =  createSIGKpath(n2kpgn, n2kkey, n2kpayload)
            #skpathjson =  ""
            
            if debug_all: log.info('sync: dump_pcdinfirebase SignalK skpathjson %s:%s', device, skpathjson)
    
            if skpathjson != {}:
              skvalues.append(skpathjson)

              skupdate_source = {'source': sksource, "timestamp":sktimestamp,"values":skvalues}
              skupdates.append( skupdate_source)

        skdata = {"updates":skupdates, "context":skcontext}

        if debug_all: log.info('sync: dump_pcdinfirebase SignalK json %s:%s', device, skdata)
        
        #ref.set(json.loads(skdata))
        ref.set(skdata)



 
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


  

 
#081316 JLB added influxdb_cloud insert 
def insert_influxdb_cloud(fact_info, device, records):
  if debug_all: log.info("start of influxdb_cloud insert %s...%s records", device, len(records))
  #if debug_all: log.info("start of influxdb_cloud insert %s...%s records", device, len(records))
  #if debug_all: log.info("start of influxdb_cloud insert %s...%s records", partition, records)
  try:
    mydata = []
    mydataIDBC = []


    ts = int(time.time())
    #if debug_all: log.info('insert_influxdb_cloud: convert_influxdbcloud_json ts %s:  ', ts)
  
    myjsonkeys = { 'deviceid': device}
    #if debug_all: log.info('freeboard: convert_influxdbcloud_json myjsonkeys %s:  ', myjsonkeys)
    
      
    values = {'records': len(records)}

    measurement = 'HS_' + str(device)
    #if debug_all: log.info('insert_influxdb_cloud: convert_influxdbcloud_json values %s:  ', values)
    
    ifluxjson ={"measurement":measurement, "time": ts, "tags":myjsonkeys, "fields": values}
    mydataIDBC.append(ifluxjson)

    
    measurement = 'HelmSmartDB'
    #if debug_all: log.info('insert_influxdb_cloud: convert_influxdbcloud_json values %s:  ', values)
    
    ifluxjson ={"measurement":measurement, "time": ts, "tags":myjsonkeys, "fields": values}
    mydataIDBC.append(ifluxjson)
    #if debug_all: log.info('insert_influxdb_cloud: convert_influxdbcloud_json tagpairs %s:  ', mydataIDBC)
    
    
    for record in records:
      for i, fact_field in fact_info:
        
        fact = record[i]
        if fact != None:
          if record[PGN] == '01F200':

            try:
              #if debug_all: log.info("insert_influxdb_cloud 01F200 device %s -> %s ", record[DEVICE], fact)
              if debug_all: log.info("insert_influxdb_cloud 01F200 device %s : %s -> %s ", record[DEVICE], record[TIMESTAMP], fact)
              instance = fact.get('engine_id', 0)
              if int(instance) > 2:
                if debug_all: log.info("insert_influxdb_cloud bad instance %s -> %s:%s:%s ",instance, record[PGN], device, fact.get('raw', ''))
                
              valuetype = fact.get('type', 'NULL')
              value = fact.get('speed', 'NULL')
              if isinstance(value, (int, float, complex)):          
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.25,   'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_rapid_update'  + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:speed' +  '.HelmSmart' ) )
              value = fact.get('boost_presure', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.1 ,   'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_rapid_update'  + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:boost_pressure' +  '.HelmSmart'))
              value = fact.get('tilt_or_trim', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value),  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_rapid_update'  + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:tilt_or_trim' +  '.HelmSmart' ) )
              #if debug_all: log.info(mydata)

            except AttributeError as e:
                if debug_all: log.info('Sync: AttributeError in InfluxDBC.append mydataIDBC append PGN 01F200: %s:  ', fact)
                if debug_all: log.info('Sync: AttributeError in InfluxDBC.append mydataIDBC append PGN 01F200:%s:  ' % str(e))


            except NameError as e:
                if debug_all: log.info('Sync: NameError in InfluxDBC.append mydataIDBC append PGN 01F200: %s:  ', fact)
                if debug_all: log.info('Sync: NameError in InfluxDBC.append mydataIDBC append PGN 01F200: %s:  ' % str(e))


                
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01F200: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass



          # PGN127489 - engine_parameters_dynamic  
          elif record[PGN] == '01F201':

            try:
              
              #if debug_all: log.info('PGN127489:  engine_parameters_dynamic ')
              #if debug_all: log.info("PGN127489:  engine_parameters_dynamic  device %s fact %s", record[DEVICE], fact)      
              instance = fact.get('engine_id', 0)
              if int(instance) > 2:
                if debug_all: log.info("insert_influxdb_cloud bad instance %s -> %s:%s:%s ",instance, record[PGN], device, fact.get('raw', ''))
                
              valuetype = fact.get('type', 'NULL')
              value = fact.get('oil_pressure', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.1 ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:oil_pressure' +  '.HelmSmart'  ) )         
              value = fact.get('oil_temp', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],float(value) * 0.1,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:oil_temp' +  '.HelmSmart'    ) )         
              value = fact.get('engine_temp', 'NULL')
              if isinstance(value, (int, float, complex)): 
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.01,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:engine_temp' +  '.HelmSmart'    ) )         

              value = fact.get('total_engine_hours', 'NULL')  
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.1 ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:total_engine_hours' +  '.HelmSmart'   ) )         

              value = fact.get('alternator_potential', 'NULL')  
              if isinstance(value, (int, float, complex)):
                # changed voltage scale from 0.1 to 0.01 because NMEA 2000 volts resolution is 0.01
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.01 ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:alternator_potential' +  '.HelmSmart'   ) )         

              #fuel rate is in liters/hour       
              value = fact.get('fuel_rate', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],   float(value) * 0.1 ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:fuel_rate' +  '.HelmSmart' ) )         
              value = fact.get('coolant_pressure', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.1 ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:coolant_pressure' +  '.HelmSmart'   ) )         
              value = fact.get('fuel_pressure', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:fuel_pressure' +  '.HelmSmart'    ) )         
   
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydata mydataIDBC PGN PGN127489: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass
            

   
          #PGN127493: Transmission Parameters, Dynamic
          elif record[PGN] == '01F205':


            try:
            
              instance = fact.get('instance', 0)
              if int(instance) > 2:
                if debug_all: log.info("insert_influxdb_cloud bad instance %s -> %s:%s:%s ",instance, record[PGN], device, fact.get('raw', ''))
                
              valuetype = fact.get('type', 'NULL')
              value = fact.get('oil_pressure', 'NULL')
              if isinstance(value, (int, float, complex)):         
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 0.1 ,  'deviceid:' + record[DEVICE] + '.sensor:transmission_parameters_dynamic'   + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:oil_pressure' +  '.HelmSmart' ) )         
              value = fact.get('oil_temp', 'NULL')
              if isinstance(value, (int, float, complex)):         
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.1,  'deviceid:' + record[DEVICE] + '.sensor:transmission_parameters_dynamic'   + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:oil_temp' +  '.HelmSmart'   ) )         

 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01F205: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass


          #PGN127497: // Trip Parameters, Engine
          elif record[PGN] == '01F209':

            try:
                          
              instance = fact.get('instance', 0)
              valuetype = fact.get('type', 'NULL')
                          
              value = fact.get('trip_fuel_used', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:trip_parameters_engine'  + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:trip_fuel_used' +  '.HelmSmart'   ) )         

              value = fact.get('fuel_rate_average', 'NULL')
              if isinstance(value, (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 0.1 ,  'deviceid:' + record[DEVICE] + '.sensor:trip_parameters_engine' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:fuel_rate_average' +  '.HelmSmart'  ) )         

              value = fact.get('fuel_rate_economy', 'NULL')
              if isinstance(value, (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],   float(value) * 0.1,  'deviceid:' + record[DEVICE] + '.sensor:trip_parameters_engine' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:fuel_rate_economy' +  '.HelmSmart'  ) )         
                
              value = fact.get('instantaneous_fuel_economy', 'NULL')
              if isinstance(value, (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],   float(value) * 0.1,  'deviceid:' + record[DEVICE] + '.sensor:trip_parameters_engine' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:instantaneous_fuel_economy' +  '.HelmSmart'  ) )         
              
 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01F209: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass




          #PGN127505:  Fluid Level
          elif record[PGN] == '01F211':


            try:
              instance = fact.get('instance', 0)
              if int(instance) > 2:
                if debug_all: log.info("insert_influxdb_cloud bad instance %s -> %s:%s:%s ",instance, record[PGN], device, fact.get('raw', ''))
                
              valuetype = fact.get('type', 'NULL')
              value = fact.get('level', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 0.004,  'deviceid:' + record[DEVICE] + '.sensor:fluid_level' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:level' +  '.HelmSmart'  ) )         
              value = fact.get('tank_capacity', 'NULL')
              if isinstance(value, (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.1,  'deviceid:' + record[DEVICE] + '.sensor:fluid_level' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:tank_capacity' +  '.HelmSmart'   ) )         

            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01F211: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass

          #PGN127506: // Battery Status Detail
          elif record[PGN] == '01F212':

            try:
               
              instance = fact.get('instance', 0)
              if int(instance) > 2:
                if debug_all: log.info("insert_influxdb_cloud bad instance %s -> %s:%s:%s ",instance, record[PGN], device, fact.get('raw', ''))
                
              valuetype = fact.get('type', 'NULL')
              value = fact.get('voltage', 'NULL')
              
              if isinstance(value, (int, float, complex)):
                # JLB 080914 changed voltage scale from .01 to .1  = don't know why I had to?
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 0.01,  'deviceid:' + record[DEVICE] + '.sensor:battery_status'  + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:voltage' +  '.HelmSmart'   ) )         
              value = fact.get('current', 'NULL')
              if isinstance(value, (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 0.1 ,  'deviceid:' + record[DEVICE] + '.sensor:battery_status' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:current' +  '.HelmSmart'  ) )         
              value = fact.get('temperature', 'NULL')
              if isinstance(value, (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],   float(value) * 0.01,  'deviceid:' + record[DEVICE] + '.sensor:battery_status' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:temperature' +  '.HelmSmart'  ) )         

              value = fact.get('stateofcharge', 'NULL')
              if isinstance(value, (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],   float(value) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:battery_status' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:stateofcharge' +  '.HelmSmart'  ) )         
 
              value = fact.get('stateofhealth', 'NULL')
              if isinstance(value, (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],   float(value) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:battery_status' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:stateofhealth' +  '.HelmSmart'  ) )         
 
              value = fact.get('timeremaining', 'NULL')
              if isinstance(value, (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],   float(value) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:battery_status' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:timeremaining' +  '.HelmSmart'  ) )         
 

              value = fact.get('ripplevoltage', 'NULL')
              if isinstance(value, (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],   float(value) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:battery_status' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ripplevoltage' +  '.HelmSmart'  ) )         
 





 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01F214: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass


          #PGN127508: // Battery Status
          elif record[PGN] == '01F214':

            try:
               
              instance = fact.get('instance', 0)
              if int(instance) > 2:
                if debug_all: log.info("insert_influxdb_cloud bad instance %s -> %s:%s:%s ",instance, record[PGN], device, fact.get('raw', ''))
                
              valuetype = fact.get('type', 'NULL')
              value = fact.get('voltage', 'NULL')
              
              if isinstance(value, (int, float, complex)):
                # JLB 080914 changed voltage scale from .01 to .1  = don't know why I had to?
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 0.01,  'deviceid:' + record[DEVICE] + '.sensor:battery_status'  + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:voltage' +  '.HelmSmart'   ) )         
              value = fact.get('current', 'NULL')
              if isinstance(value, (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 0.1 ,  'deviceid:' + record[DEVICE] + '.sensor:battery_status' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:current' +  '.HelmSmart'  ) )         
              value = fact.get('temperature', 'NULL')
              if isinstance(value, (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],   float(value) * 0.01,  'deviceid:' + record[DEVICE] + '.sensor:battery_status' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:temperature' +  '.HelmSmart'  ) )         
 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01F214: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass

            

          #PGN130306:  Wind Data
          elif record[PGN] == '01FD02':

            try:
              
              if debug_all: log.info('PGN130306:  Wind Data')
              instance = fact.get('instance', 0)
              valuetype = fact.get('wind_reference', 'NULL')
              value = fact.get('wind_speed', 'NULL')
              if isinstance(value, (int, float, complex)):            

                if valuetype == "Gust":
                  mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.01,  'deviceid:' + record[DEVICE] + '.sensor:wind_data' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:wind_gusts' +  '.HelmSmart'  ) )

                else:
                  mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.01,  'deviceid:' + record[DEVICE] + '.sensor:wind_data' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:wind_speed' +  '.HelmSmart'  ) )


                 
              value = fact.get('wind_direction', 'NULL')
              if isinstance(value, (int, float, complex)):   
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:wind_data' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:wind_direction' +  '.HelmSmart'  ) )
 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01FD02: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass
               


          #PGN130323:  Meteorological Station Data
          elif record[PGN] == '01FD13':

            try:
              
              instance = fact.get('instance', 0)
              valuetype = fact.get('wind_reference', 'NULL')
              value = fact.get('wind_gusts', 'NULL')
              if isinstance(value, (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.01,  'deviceid:' + record[DEVICE] + '.sensor:wind_data' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:wind_gusts' +  '.HelmSmart'  ) )
 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01FD13: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass


          #PGN127250:  Heading
          elif record[PGN] == '01F112':

            try:
              #if debug_all: log.info('PGN127250:  Heading')
              instance = fact.get('instance', 0)
              valuetype = fact.get('heading_reference', 'NULL')
              value = fact.get('heading', 'NULL')
              #if debug_all: log.info('Heading = ' + str(value))
      
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:heading' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:heading' +  '.HelmSmart'   ) )
   
                
              value = fact.get('deviation', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:heading' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:deviation' +  '.HelmSmart'   ) )
                
              value = fact.get('variation', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:heading' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:variation' +  '.HelmSmart'   ) )
                 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01F112: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass


            

          #PGN127257:  Attitude
          elif record[PGN] == '01F119':

            try:

              
              instance = fact.get('instance', 0)
              valuetype = fact.get('type', 'NULL')
              value = fact.get('yaw', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:attitude'  + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:yaw' +  '.HelmSmart'   ) )         
              value = fact.get('pitch', 'NULL')
              if isinstance(value, (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] +  '.sensor:attitude'  + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:pitch' +  '.HelmSmart'   ) )         
              value = fact.get('roll', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] +  '.sensor:attitude'  + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:roll' +  '.HelmSmart'  ) )         

 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01F119: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass

          #PGN127245: Rudder
          elif record[PGN] == '01F10D':

            try:

              #if debug_all: log.info('PGN127245:  Rudder '+ record[DEVICE])
              instance = fact.get('instance', 0)
              valuetype = fact.get('direction_order', 'NULL')
              value = fact.get('angle_order', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:rudder' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:angle_order' +  '.HelmSmart'   ) )         
              value = fact.get('position', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:rudder' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:position' +  '.HelmSmart'   ) )         
                #if debug_all: log.info(value)
                #if debug_all: log.info( 'deviceid:' + record[DEVICE] + '.sensor:rudder' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:position' +  '.HelmSmart'  )
 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01F10D: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass


          #PGN127251: RateOfTurn
          elif record[PGN] == '01F113':

            try:
              
              #if debug_all: log.info('PGN127251:  rot '+ record[DEVICE])
              instance = fact.get('instance', 0)
              valuetype = fact.get('type', 'NULL')
              value = fact.get('rate_of_turn', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:rot' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:rateofturn' +  '.HelmSmart'   ) )         
     
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01F113: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass



          #PGN130310:  Temperature Data
          elif record[PGN] == '01FD06':


            try:
              
              instance = fact.get('instance', 0)
              valuetype = fact.get('type', 'NULL')
              value = fact.get('water_temperature', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 1.0,  'deviceid:' + record[DEVICE] +  '.sensor:temperature_data' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:water_temperature' +  '.HelmSmart'   ) )

                
              value = fact.get('air_temperature', 'NULL')
              if isinstance(value, (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 1.0,  'deviceid:' + record[DEVICE] +  '.sensor:temperature_data' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:air_temperature' +  '.HelmSmart'   ) )
   
                
              value = fact.get('baro_pressure', 'NULL')
              if isinstance(value, (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 1.0,  'deviceid:' + record[DEVICE] +  '.sensor:temperature_data' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:baro_pressure' +  '.HelmSmart'   ) )         
 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01FD06: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass

         

          #PGN130311:  ENviron Data
          elif record[PGN] == '01FD07':
            #if debug_all: log.info('PGN130311:  ENviron Data ')
            try:
              
              if debug_all: log.info("PGN130311:  ENviron Data  device %s fact %s", record[DEVICE], fact)      
              
              instance = fact.get('instance', 0)
              valuetype = fact.get('temperature_instance', 'NULL')
              humtype = fact.get('humidity_instance', 'NULL')
              value = fact.get('temperature', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 1.0, 'deviceid:' + record[DEVICE] + '.sensor:environmental_data' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:temperature' +  '.HelmSmart'   ) )         

              value = fact.get('humidity', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:environmental_data' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(humtype) + '.parameter:humidity' +  '.HelmSmart'   ) )
                
              value = fact.get('atmospheric_pressure', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:environmental_data' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:atmospheric_pressure' +  '.HelmSmart'   ) )         
 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01FD07: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass

          
          #PGN130312:  Temperature Data
          elif record[PGN] == '01FD08':
            try:
              instance = fact.get('temperature_instance', 0)
              if int(instance) > 3:
                if debug_all: log.info("insert_influxdb_cloud bad instance %s -> %s:%s:%s ",instance, record[PGN], device, fact.get('raw', ''))
                
              valuetype = fact.get('temperature_source', 'NULL')
              value = fact.get('actual_temperature', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:temperature' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:actual_temperature' +  '.HelmSmart'   ) )
                
              value = fact.get('set_temperature', 'NULL')
              if isinstance(value, (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:temperature' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:set_temperature' +  '.HelmSmart'   ) )         

            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydata append PGN 01FD08: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass

          
          #PGN130316:  Temperature Extended Data
          elif record[PGN] == '01FD0C':
            try:
              instance = fact.get('temperature_instance', 0)
              #if int(instance) > 3:
              #  if debug_all: log.info("insert_influxdb_cloud bad instance %s -> %s:%s:%s ",instance, record[PGN], device, fact.get('raw', ''))
                
              valuetype = fact.get('temperature_source', 'NULL')
              value = fact.get('actual_temperature', 'NULL') 
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:temperature' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:actual_temperature' +  '.HelmSmart'   ) )


              if valuetype == 'EGT':
                if isinstance(value, (int, float, complex)): 
                  mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:NULL' + '.parameter:egt_temp' +  '.HelmSmart'    ) ) 

                
              value = fact.get('set_temperature', 'NULL')
              if isinstance(value, (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:temperature' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:set_temperature' +  '.HelmSmart'   ) )         

            except: 
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydata append PGN 01FD0C: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass  




              
         #PGN129026:  COG and SOG
          elif record[PGN] == '01F802':


            try:
              
              instance = fact.get('instance', 0)
              valuetype = fact.get('cog_reference', 'NULL')
              value = fact.get('course_over_ground', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:cogsog'  + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:course_over_ground' +  '.HelmSmart'   ) )
                
              value = fact.get('speed_over_ground', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:cogsog'  + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:speed_over_ground' +  '.HelmSmart'   ) )         

 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01F802: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass


          #PGN129025:  Position Rapid
          elif record[PGN] == '01F801':


            try:
              
              instance = fact.get('instance', 0)
              valuetype = fact.get('type', 'NULL')
              valuelat = fact.get('lat', 'NULL')
              if isinstance(valuelat, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(valuelat) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:position_rapid' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:lat' +  '.HelmSmart'   ) )
   
                
              valuelng = fact.get('lng', 'NULL')
              if isinstance(valuelng, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(valuelng) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:position_rapid' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:lng' +  '.HelmSmart'   ) )
                
              if isinstance(valuelng, (int, float, complex)) and isinstance(valuelat, (int, float, complex)):  
                mydataIDBC.append(convert_influxdbcloud_gpsjson(record[TIMESTAMP], float(valuelat) * 1.0,  float(valuelng) * 1.0, 'deviceid:' + record[DEVICE] + '.sensor:position_rapid' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:latlng' +  '.HelmSmart'   ) )         

 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01F801: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass




          #PGN129029:  GNSS Position Data
          elif record[PGN] == '01F805':

            try:
              
              instance = fact.get('instance', 0)
              valuetype = fact.get('method', 'NULL')

              
              valuelat = fact.get('lat', 'NULL')
              if isinstance(valuelat, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(valuelat) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:position_rapid' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:lat' +  '.HelmSmart'   ) )
   
                
              valuelng = fact.get('lng', 'NULL')
              if isinstance(valuelng, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(valuelng) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:position_rapid' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:lng' +  '.HelmSmart'   ) )

              valuealt = fact.get('altitude', 'NULL')
              if isinstance(valuealt, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(valuealt) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:position_rapid' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:altitude' +  '.HelmSmart'   ) )


              valuealt = fact.get('altitude', 'NULL')
              if isinstance(valuealt, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(valuealt) * 1.0,  'deviceid:' + record[DEVICE] + '.sensor:environmental_data' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  'Outside Temperature'  + '.parameter:altitude' +  '.HelmSmart'   ) )         

              
              valuesiv = fact.get('siv', 'NULL')
              if isinstance(valuesiv, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(valuesiv) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:position_rapid' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:siv' +  '.HelmSmart'   ) )
                          

                
              if isinstance(valuelng, (int, float, complex)) and isinstance(valuelat, (int, float, complex)):  
                mydataIDBC.append(convert_influxdbcloud_gpsjson(record[TIMESTAMP], float(valuelat) * 1.0,  float(valuelng) * 1.0, 'deviceid:' + record[DEVICE] + '.sensor:position_rapid' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:latlng' +  '.HelmSmart'   ) )         

 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01F805: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass






          #PGN28267: Water Depth Data
          elif record[PGN] == '01F50B':

            try:

              
              instance = fact.get('instance', 0)
              valuetype = fact.get('type', 'NULL')
              value = fact.get('depth', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:water_depth'  + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:depth' +  '.HelmSmart'   ) )         
              value = fact.get('transducer_offset', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:water_depth' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:transducer_offset' +  '.HelmSmart'   ) )         
 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01F50B: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass



          #PGN128259:  Water Speed
          elif record[PGN] == '01F503':


            try:
              
              instance = fact.get('instance', 0)
              valuetype = fact.get('type_reference', 'NULL')
              value = fact.get('waterspeed', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:water_speed' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:waterspeed' +  '.HelmSmart'   ) )         
              value = fact.get('groundspeed', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:water_speed' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:groundspeed' +  '.HelmSmart'   ) )         
 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01F503: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass


          #PGN126992:  system Time
          elif record[PGN] == '01F010':


            try:
              
              instance = fact.get('instance', 0)
              valuetype = fact.get('time_source', 'NULL')
              value = fact.get('days', 'NULL')
              if isinstance(value, (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:sytem_time' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:days' +  '.HelmSmart'   ) )

                
              value = fact.get('ms', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:sytem_time' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ms' +  '.HelmSmart'   ) )         
 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01F010: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass



          #PGN130944:  SeaSmart Heartbeat message
          elif record[PGN] == '01FF80':

            try:
              
              #dtvalue = record[TIMESTAMP]
              dtvalue = datetime.now()
              mvalue = time.mktime(dtvalue.timetuple())
              value = record[TIMESTAMP]
              #if debug_all: log.info('heartbeat =  %s ', int(mvalue))
              #if debug_all: log.info('sync:heartbeat =  %s : %s : %s ', record[DEVICE], dtvalue, record[TIMESTAMP] )
              #if debug_all: log.info('sync:heartbeat =  %s : %s : %s ', record[DEVICE], dtvalue, record[TIMESTAMP] )

              if isinstance(int(mvalue), (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(mvalue) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:heartbeat' + '.source:' + record[SOURCE] + '.instance:0'  + '.type:NULL'  + '.parameter:timestamp' +  '.HelmSmart'   ) )         

              value = fact.get('session_id', 'NULL')
              if isinstance(int(mvalue), (int, float, complex)):            
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:heartbeat' + '.source:' + record[SOURCE] + '.instance:0'  + '.type:NULL'  + '.parameter:sessionid' +  '.HelmSmart'   ) )         


 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01FF80: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass




          #PGN130945 Custom Cellular status
          elif record[PGN] == '01FF7E':

            try:

               
              #instance = fact.get('instance', 0)
              #valuetype = fact.get('type', 'NULL')
              value = fact.get('ai_status', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:cellular_status'  + '.source:' + record[SOURCE] + '.instance:0'  + '.type:NULL' + '.parameter:ai_status' +  '.HelmSmart'   ) )         
              value = fact.get('db_status', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:cellular_status' + '.source:' + record[SOURCE] + '.instance:0'  + '.type:NULL'+ '.parameter:db_status' +  '.HelmSmart'   ) )         
 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01FF7E: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass


          #PGN130946:  Rain Data
          elif record[PGN] == '01FF82':


            try:
              
              instance = fact.get('instance', 0)
              valuetype = fact.get('type_reference', 'NULL')
              
              value = fact.get('rainaccum', 'NULL')
              if isinstance(value, (int, float, complex)):
                #convert 0.01 mm to meters to standardize 
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.00001,   'deviceid:' + record[DEVICE] + '.sensor:rain_gauge' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:accumulation' +  '.HelmSmart'   ) )         

              value = fact.get('rainduration', 'NULL')
              if isinstance(value, (int, float, complex)):
                #convert minutes to hours
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.0166,   'deviceid:' + record[DEVICE] + '.sensor:rain_gauge' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:rainduration' +  '.HelmSmart'   ) )         

              value = fact.get('rainrate', 'NULL')
              if isinstance(value, (int, float, complex)):
                # convert tenths of 0.01 mm/hr to meters/hr
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.00001,   'deviceid:' + record[DEVICE] + '.sensor:rain_gauge' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:rate' +  '.HelmSmart'   ) )         

              value = fact.get('rainpeak', 'NULL')
              if isinstance(value, (int, float, complex)):
                # convert tenths of 0.01 mm/hr to meters/hr
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.00001,   'deviceid:' + record[DEVICE] + '.sensor:rain_gauge' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:peak' +  '.HelmSmart'   ) )         


 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01FF82: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass




           
          #PGN65286: SeaSmart Dimmer
          elif record[PGN] == '00FF06':

            try:

              
              if debug_all: log.info("Dimmer insert %s ", record[DEVICE])
              pgntype = fact.get('pgntype',0)
              if debug_all: log.info("Dimmer insert PGNTYPE %s ", pgntype)

              # checkt if type is 0xE199 which belongs to SeaSmart
              if pgntype == 57753 or pgntype == 39393:
              
                instance = fact.get('instance', 0)
                if int(instance) > 16:
                  if debug_all: log.info("insert_influxdb_cloud bad instance %s:%s ", device, fact)
                  
                valuetype = fact.get('dimmertype', 'NULL')
                if debug_all: log.info("Dimmer dimmertype %s ", valuetype)

                value = fact.get('dimmer0', 'NULL')
                if debug_all: log.info("Dimmer insert value0 %s ", value)
                if isinstance(value, (int, float, complex)):             
                  mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartdimmer' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value0' +  '.HelmSmart'   ) )         

                value = fact.get('dimmer1', 'NULL')
                if isinstance(value, (int, float, complex)):             
                  mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartdimmer' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value1' +  '.HelmSmart'   ) )         

                value = fact.get('dimmer2', 'NULL')
                if isinstance(value, (int, float, complex)):             
                  mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartdimmer' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value2' +  '.HelmSmart'   ) )         

                value = fact.get('dimmer3', 'NULL')
                if isinstance(value, (int, float, complex)):
                  #netDimmer Modules return amps * 10
                  if valuetype.find('LED 1 Channel') != -1:
                    mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.1,   'deviceid:' + record[DEVICE] + '.sensor:seasmartdimmer' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value3' +  '.HelmSmart'   ) )         
                  #netDimmer HUBS return as dimmer value channel 3
                  else:
                    mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartdimmer' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value3' +  '.HelmSmart'   ) )         

                value = fact.get('control', 'NULL')
                if isinstance(value, (int, float, complex)):             
                  mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartdimmer' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value4' +  '.HelmSmart'   ) )         
                if debug_all: log.info("Dimmer data %s ", mydataIDBC)

 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FF06: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass

          #PGN65292: SeaSmart Indicator Runtime
          elif record[PGN] == '00FF0C':

            try:

              
              if debug_all: log.info("Indicator Runtime insert %s ", record[DEVICE])
              pgntype = fact.get('pgntype',0)
              if debug_all: log.info("Indicator Runtime insert PGNTYPE %s ", pgntype)

              # checkt if type is 0xE199 which belongs to SeaSmart
              if pgntype == 57753:
              
                instance = fact.get('instance', 0)
                if int(instance) > 16:
                  if debug_all: log.info("insert_influxdb_cloud bad instance %s:%s ", device, fact)
                  
                valuetype = fact.get('channel', 'NULL')
                #if debug_all: log.info("Dimmer dimmertype %s ", valuetype)

                value = fact.get('runtime_sec', 'NULL')
                if debug_all: log.info("Indicator Runtime insert value0 %s ", value)
                if isinstance(value, (int, float, complex)):             
                  mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartindicator' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:runtime_sec' +  '.HelmSmart'   ) )         

                value = fact.get('cycles', 'NULL')
                if isinstance(value, (int, float, complex)):             
                  mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartindicator' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:cycles' +  '.HelmSmart'   ) )         

 
 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FF0C: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass


          
          #PGN127501: SeaSmart Switch
          elif record[PGN] == '01F20D':

            try:
              
              if debug_all: log.info("Switch insert %s ", record[DEVICE])

              instance = fact.get('instance', 0)
              if int(instance) > 16:
                if debug_all: log.info("insert_influxdb_cloud bad instance %s -> %s:%s:%s ",instance, record[PGN], device, fact.get('raw', ''))

              
              valuetype = fact.get('type_reference', 'NULL')

              value = fact.get('indic01', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartswitch' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value0' +  '.HelmSmart'   ) )         
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartindicator' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:0' + '.parameter:value' +  '.HelmSmart'   ) )         



              value = fact.get('indic02', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartswitch' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value1' +  '.HelmSmart'   ) )
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartindicator' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:1' + '.parameter:value' +  '.HelmSmart'   ) )                    

              value = fact.get('indic03', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartswitch' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value2' +  '.HelmSmart'   ) )         
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartindicator' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:2' + '.parameter:value' +  '.HelmSmart'   ) )                    


              value = fact.get('indic04', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartswitch' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value3' +  '.HelmSmart'   ) )         
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartindicator' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:3' + '.parameter:value' +  '.HelmSmart'   ) )                    


              value = fact.get('indic05', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartswitch' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value4' +  '.HelmSmart'   ) )         
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartindicator' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:4' + '.parameter:value' +  '.HelmSmart'   ) )                    


              value = fact.get('indic06', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartswitch' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value5' +  '.HelmSmart'   ) )         
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartindicator' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:5' + '.parameter:value' +  '.HelmSmart'   ) )                    


              value = fact.get('indic07', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartswitch' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value6' +  '.HelmSmart'   ) )         
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartindicator' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:6' + '.parameter:value' +  '.HelmSmart'   ) )                    


              value = fact.get('indic08', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartswitch' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value7' +  '.HelmSmart'   ) )         
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartindicator' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:7' + '.parameter:value' +  '.HelmSmart'   ) )                    


              value = fact.get('indic09', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartswitch' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value8' +  '.HelmSmart'   ) )         

              value = fact.get('indic10', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartswitch' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value9' +  '.HelmSmart'   ) )         

              value = fact.get('indic11', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartswitch' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value10' +  '.HelmSmart'   ) )         


              value = fact.get('indic12', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartswitch' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value11' +  '.HelmSmart'   ) )         


              value = fact.get('indic13', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartswitch' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value12' +  '.HelmSmart'   ) )         

              value = fact.get('indic14', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartswitch' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value13' +  '.HelmSmart'   ) )         

              value = fact.get('indic15', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartswitch' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value14' +  '.HelmSmart'   ) )         


              value = fact.get('indic16', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartswitch' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:value15' +  '.HelmSmart'   ) )         








              value = fact.get('bank0', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartswitch' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:bank0' +  '.HelmSmart'   ) )         


              value = fact.get('bank1', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartswitch' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:bank1' +  '.HelmSmart'   ) )         


              value = fact.get('bank2', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:seasmartswitch' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:bank2' +  '.HelmSmart'   ) )         


 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 01F20D: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass




          #HALTEC PGN 65376 (0x0FF60) Electronic Engine Controller 1
          elif record[PGN] == '00FF60':


            try:
              #if debug_all: log.info("insert_influxdb_cloud 00FF60 -> %s ",fact)
              instance = fact.get('engine_id', 0)
                
              valuetype = fact.get('type', 'HALTECH')

              value = fact.get('engine_speed', 'NULL')
              if isinstance(value, (int, float, complex)):          
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_rapid_update'  + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:speed' +  '.HelmSmart' ) )

              value = fact.get('manifold_pressure', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP] ,(float(value) * 0.1 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_rapid_update' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:boost_pressure' +  '.HelmSmart'    ) )

              value = fact.get('throttle_position', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.1) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_rapid_update' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:throttle_position' +  '.HelmSmart'    ) )         


              value = fact.get('coolant_pressure', 'NULL')  
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.1) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:coolant_pressure' +  '.HelmSmart'   ) )         


            except TypeError as e:
              if debug_all: log.info('Sync: Type Error in InfluxDBC.append mydataIDBC append PGN 00FF60 %s:  ', fact)
              if debug_all: log.info('Sync: Type Error in InfluxDBC.append mydataIDBC append PGN 00FF60 %s:  ' % str(e))

              
              
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FF60: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass


            



          #HALTEC PGN 65504 (0x0FFE0)  Engine Temps  
          elif record[PGN] == '00FFE0':


            try:
              
              #if debug_all: log.info("insert_influxdb_cloud 00FFE0 -> %s ",fact)        
              instance = fact.get('engine_id', 0)
              valuetype = fact.get('type', 'HALTECH')
              
              value = fact.get('engine_temp', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.1 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:engine_temp' +  '.HelmSmart'  ) )         

              value = fact.get('fuel_temp', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],(float(value)  * 0.1 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:fuel_temp' +  '.HelmSmart'    ) )         

              value = fact.get('oil_temp', 'NULL')
              if isinstance(value, (int, float, complex)): 
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.1 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:oil_temp' +  '.HelmSmart'    ) )         

              value = fact.get('intake_temp', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.1 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:intake_temp' +  '.HelmSmart'    ) )         

 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FFE0: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass




          #HALTEC PGN 65377 (0x0FF61)   Engine Pressures
          elif record[PGN] == '00FF61':


            try:
              #if debug_all: log.info("insert_influxdb_cloud 00FF61 -> %s ",fact)  
              instance = fact.get('engine_id', 0)
              valuetype = fact.get('type', 'HALTECH')
              
              value = fact.get('fuel_pressure', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.1 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:fuel_pressure' +  '.HelmSmart'  ) )         

              value = fact.get('wastegate_pressure', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],(float(value) * 0.1 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:wastegate_pressure' +  '.HelmSmart'    ) )         

              value = fact.get('oil_pressure', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP] ,(float(value) * 0.1 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:oil_pressure' +  '.HelmSmart'    ) )

              value = fact.get('engine_demand', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP] ,(float(value) * 0.1 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:engine_demand' +  '.HelmSmart'    ) )

 

 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FF61: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass

            


          #HALTEC PGN 65394 (0x0FF72)   Engine Volts
          elif record[PGN] == '00FF72':


            try:
              #if debug_all: log.info("insert_influxdb_cloud 00FF61 -> %s ",fact)  
              instance = fact.get('engine_id', 0)
              valuetype = fact.get('type', 'HALTECH')
              
              value = fact.get('battery_volts', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.1 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:alternator_potential' +  '.HelmSmart'  ) )         

  
              value = fact.get('target_boost', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.1 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:target_boost' +  '.HelmSmart'    ) )

              value = fact.get('baro_pressure', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.1 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:baro_pressure' +  '.HelmSmart'    ) )

 

 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FF72: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass

            

          #HALTEC PGN 65393 (0x0FF71)   Fuel Flow
          elif record[PGN] == '00FF71':


            try:
              #if debug_all: log.info("insert_influxdb_cloud 00FF71 -> %s ",fact)  
              instance = fact.get('engine_id', 0)
              valuetype = fact.get('type', 'HALTECH')

              # convert cc/min to liters/hr = 1/16.6666 =   0.06            
              value = fact.get('fuel_flow', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.06 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:fuel_rate' +  '.HelmSmart'  ) )         

              # convert cc/min to liters/hr = 1/16.6666 =   0.06        
              value = fact.get('fuel_return', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.06 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:fuel_return' +  '.HelmSmart'    ) )


            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FF71: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass

            
            

          #HALTEC PGN 65393 (0x0FFE2)   Fuel Level
          elif record[PGN] == '00FFE2':


            try:
              #if debug_all: log.info("insert_influxdb_cloud 00FFE2 -> %s ",fact)  
              instance = fact.get('engine_id', 0)
              valuetype = fact.get('type', 'HALTECH')

              # value in 0.1 %         
              value = fact.get('fuel_level', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 0.1,  'deviceid:' + record[DEVICE] + '.sensor:fluid_level' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:level' +  '.HelmSmart'  ) )          


            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FFE2: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass

            

            

          #HALTEC PGN 65392 (0x0FFE1)   Gearbox
          elif record[PGN] == '00FFE1':


            try:
              #if debug_all: log.info("insert_influxdb_cloud 00FFE1 -> %s ",fact)  
              instance = fact.get('engine_id', 0)
              valuetype = fact.get('type', 'HALTECH')

     
              value = fact.get('gearbox_temperature', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.1,  'deviceid:' + record[DEVICE] + '.sensor:transmission_parameters_dynamic'   + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:oil_temp' +  '.HelmSmart'   ) )         


            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FFE1: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass

            








          #J1939 PGN 61444 (0x0F004) Electronic Engine Controller 1
          elif record[PGN] == '00F004':


            try:
              #if debug_all: log.info("insert_influxdb_cloud 01F200 -> %s ",fact)
              instance = fact.get('engine_id', 0)
                
              valuetype = fact.get('type', 'J1939')
              value = fact.get('speed', 'NULL')
              if isinstance(value, (int, float, complex)):          
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.125,   'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_rapid_update'  + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:speed' +  '.HelmSmart' ) )
              value = fact.get('torque_demand', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0 - 125 ,   'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_rapid_update'  + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:torque_demand' +  '.HelmSmart'))
              value = fact.get('torque_actual', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) - 125,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_rapid_update'  + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:torque_actual' +  '.HelmSmart' ) )
              value = fact.get('torque_request', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) - 125 ,   'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_rapid_update'  + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:torque_request' +  '.HelmSmart'))
              value = fact.get('torque_mode', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value),  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_rapid_update'  + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:torque_mode' +  '.HelmSmart' ) )
 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00F004: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass


            



          # PGN65262 - J1939 Engine Temps  
          elif record[PGN] == '00FEEE':


            try:
              
              #if debug_all: log.info('PGN65262:  j1939_engine_temps '+ record[PGN])          
              instance = fact.get('engine_id', 0)
              valuetype = fact.get('type', 'J1939')
              
              value = fact.get('engine_temp', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) + 233.15 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:engine_temp' +  '.HelmSmart'  ) )         
              value = fact.get('fuel_temp', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],(float(value) + 233.15 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:fuel_temp' +  '.HelmSmart'    ) )         
              value = fact.get('oil_temp', 'NULL')
              if isinstance(value, (int, float, complex)): 
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.03125 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:oil_temp' +  '.HelmSmart'    ) )         

              value = fact.get('turbo_temp', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP] (float(value) * 0.03125 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:turbo_temp' +  '.HelmSmart'    ) )         
              value = fact.get('intercool_temp', 'NULL')
              if isinstance(value, (int, float, complex)): 
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) + 233.15 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:intercool_temp' +  '.HelmSmart'    ) )         

              value = fact.get('intercool_open', 'NULL')  
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.4 ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:intercool_open' +  '.HelmSmart'   ) )         

 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FEEE: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass




          # PGN65263 - J1939 Engine Pressures
          elif record[PGN] == '00FEEF':


            try:
              #if debug_all: log.info('PGN65263:  j1939_engine_temps '+ record[PGN])          
              instance = fact.get('engine_id', 0)
              valuetype = fact.get('type', 'J1939')
              
              value = fact.get('fuel_pressure', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 4.0 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:fuel_pressure' +  '.HelmSmart'  ) )         
              value = fact.get('blowby_pressure', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],(float(value) * 0.05 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:blowby_pressure' +  '.HelmSmart'    ) )         
              value = fact.get('oil_level', 'NULL')
              if isinstance(value, (int, float, complex)): 
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.4 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:oil_level' +  '.HelmSmart'    ) )         

              value = fact.get('oil_pressure', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP] ,(float(value) * 4.0 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:oil_pressure' +  '.HelmSmart'    ) )

                
              value = fact.get('crankcase_pressure', 'NULL')
              if isinstance(value, (int, float, complex)): 
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], ((float(value) * 0.0078) - 250 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:crankcase_pressure' +  '.HelmSmart'    ) )         

              value = fact.get('coolant_pressure', 'NULL')  
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 2.0) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:coolant_pressure' +  '.HelmSmart'   ) )         

              value = fact.get('coolant_level', 'NULL')  
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.4 ),  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:coolant_level' +  '.HelmSmart'   ) )         


 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FEEF: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass

            


   
          #PGN 65272 (0x0FEF8)Transmission Fluids
          elif record[PGN] == '00FEF8':

            try:
              
              instance = fact.get('instance', 0)
              #if int(instance) > 2:
              # if debug_all: log.info("insert_influxdb_cloud bad instance %s -> %s:%s:%s ",instance, record[PGN], device, fact.get('raw', ''))
                
              valuetype = fact.get('type', 'J1939')

              
              value = fact.get('tran_oil_pressure', 'NULL')
              if isinstance(value, (int, float, complex)):         
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 16.0 ,  'deviceid:' + record[DEVICE] + '.sensor:transmission_parameters_dynamic'   + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:oil_pressure' +  '.HelmSmart' ) )         
              value = fact.get('tran_oil_temp', 'NULL')
              if isinstance(value, (int, float, complex)):         
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.03125,  'deviceid:' + record[DEVICE] + '.sensor:transmission_parameters_dynamic'   + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:oil_temp' +  '.HelmSmart'   ) )         
              
              value = fact.get('clutch_pressure', 'NULL')
              if isinstance(value, (int, float, complex)):         
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 16.0 ,  'deviceid:' + record[DEVICE] + '.sensor:transmission_parameters_dynamic'   + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:clutch_pressure' +  '.HelmSmart' ) )         
              value = fact.get('tran_oil_level', 'NULL')
              if isinstance(value, (int, float, complex)):         
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.4,  'deviceid:' + record[DEVICE] + '.sensor:transmission_parameters_dynamic'   + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:tran_oil_level' +  '.HelmSmart'   ) )         
              value = fact.get('tran_diff_pressure', 'NULL')
              if isinstance(value, (int, float, complex)):         
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 2.0,  'deviceid:' + record[DEVICE] + '.sensor:transmission_parameters_dynamic'   + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:tran_diff_pressure' +  '.HelmSmart'   ) )         


              
              value = fact.get('tran_oil_warn', 'NULL')
              if isinstance(value, (int, float, complex)):         
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],  float(value) * 0.5 ,  'deviceid:' + record[DEVICE] + '.sensor:transmission_parameters_dynamic'   + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:tran_oil_warn' +  '.HelmSmart' ) )         
              value = fact.get('tran_oil_status', 'NULL')
              if isinstance(value, (int, float, complex)):         
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) ,  'deviceid:' + record[DEVICE] + '.sensor:transmission_parameters_dynamic'   + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:tran_oil_status' +  '.HelmSmart'   ) )         

 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FEF8: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass



          # J1939 PGN 65271 (0x0FEF7) Vehicle Electrical Power
          elif record[PGN] == '00FEF7':


            try:
              
              #if debug_all: log.info('PGN65262:  j1939_engine_temps '+ record[PGN])          
              instance = fact.get('engine_id', 0)
              valuetype = fact.get('type', 'J1939')
              
              value = fact.get('charging_voltage', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.05 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:alternator_potential' +  '.HelmSmart'  ) )         
              value = fact.get('alternator_current', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],(float(value) *1.0 - 125 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:alternator_current' +  '.HelmSmart'    ) )         
              value = fact.get('battery_voltage', 'NULL')
              if isinstance(value, (int, float, complex)): 
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.05 ) ,  'deviceid:' + record[DEVICE] + '.sensor:battery_status' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:voltage' +  '.HelmSmart'    ) )         

              value = fact.get('battery_current', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP] (float(value) * 1.0 - 125) ,  'deviceid:' + record[DEVICE] + '.sensor:battery_status' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:current' +  '.HelmSmart'    ) )         
              value = fact.get('keyswitch_voltage', 'NULL')
              if isinstance(value, (int, float, complex)): 
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], ((float(value) * 0.05) ) ,  'deviceid:' + record[DEVICE] + '.sensor:battery_status' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:keyswitch_voltage' +  '.HelmSmart'    ) )         

 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FEF7: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass




          # J1939 PGN 65266 (0x0FEF2) Fuel Economy
          elif record[PGN] == '00FEF2':


            try:
              #if debug_all: log.info('PGN65262:  j1939_engine_temps '+ record[PGN])          
              instance = fact.get('engine_id', 0)
              valuetype = fact.get('type', 'J1939')
              
              value = fact.get('fuel_rate', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.05 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:fuel_rate' +  '.HelmSmart'  ) )         
              value = fact.get('instantaneous_fuel_economy', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],(float(value) * 0.001953125 ) ,  'deviceid:' + record[DEVICE] + '.sensor:trip_parameters_engine' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:instantaneous_fuel_economy' +  '.HelmSmart'    ) )         
              value = fact.get('fuel_rate', 'NULL')
              if isinstance(value, (int, float, complex)): 
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.05 ) ,  'deviceid:' + record[DEVICE] + '.sensor:trip_parameters_engine' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:fuel_rate_economy' +  '.HelmSmart'    ) )         

              value = fact.get('average_fuel_economy', 'NULL')
              if isinstance(value, (int, float, complex)): 
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.001953125 ) ,  'deviceid:' + record[DEVICE] + '.sensor:trip_parameters_engine' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:fuel_rate_average' +  '.HelmSmart'    ) )         
 

              value = fact.get('throttle_position', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP] (float(value) * 0.4) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_rapid_update' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:throttle_position' +  '.HelmSmart'    ) )         

              value = fact.get('demand_torque', 'NULL')
              if isinstance(value, (int, float, complex)): 
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], ((float(value) * 0.4) ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_rapid_update' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:demand_torque' +  '.HelmSmart'    ) )         


            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FEF2: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass

            




          #  J1939 PGN 65276 (0x0FEFC) Dash Display
          elif record[PGN] == '00FEFC':

            try:

              
              #if debug_all: log.info('PGN65262:  j1939_engine_temps '+ record[PGN])          
              instance = fact.get('engine_id', 0)
              valuetype = fact.get('type', 'J1939')
              
              value = fact.get('fuel1_level', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.4 ) ,  'deviceid:' + record[DEVICE] + '.sensor:fluid_level' + '.source:' + record[SOURCE] + '.instance:' +  str(0) + '.type:' +  str(8) + '.parameter:level' +  '.HelmSmart'  ) )         
              value = fact.get('fuel2_level', 'NULL')
              if isinstance(value, (int, float, complex)):
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP],(float(value) * 0.4 ) ,  'deviceid:' + record[DEVICE] + '.sensor:fluid_level' + '.source:' + record[SOURCE] + '.instance:' +  str(0) + '.type:' +  str(9) + '.parameter:level' +  '.HelmSmart'    ) )         
              value = fact.get('washer_level', 'NULL')
              if isinstance(value, (int, float, complex)): 
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.4 ) ,  'deviceid:' + record[DEVICE] + '.sensor:fluid_level' + '.source:' + record[SOURCE] + '.instance:' +  str(0) + '.type:' +  str(10) + '.parameter:level' +  '.HelmSmart'    ) )         

              value = fact.get('fuel_filter_differential_pressure', 'NULL')
              if isinstance(value, (int, float, complex)): 
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 2.0 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:fuel_filter_differential_pressure' +  '.HelmSmart'    ) )         

              value = fact.get('oil_filter_differential_pressure', 'NULL')
              if isinstance(value, (int, float, complex)): 
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.5 ) ,  'deviceid:' + record[DEVICE] + '.sensor:engine_parameters_dynamic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:oil_filter_differential_pressure' +  '.HelmSmart'    ) )         

              value = fact.get('cargo_temperature', 'NULL')
              if isinstance(value, (int, float, complex)): 
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], (float(value) * 0.03125 ) ,  'deviceid:' + record[DEVICE] + '.sensor:trip_parameters_engine' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  'Main Cabin Temperature' + '.parameter:fuel_rate_average' +  '.HelmSmart'    ) )         


 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FEFC: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass




          #PGN65287: SeaSmart ac watt hours 0x0FF07
          elif record[PGN] == '00FF07':


            try:

              pgntype = fact.get('pgntype',0)
              # checkt if type is 0xE199 which belongs to SeaSmart
              if pgntype == 57753:
                
                instance = fact.get('instance', 0)
                valuetype = fact.get('ac_type', 'NULL')
              
                value = fact.get('ac_kwatt_hours', 'NULL')
                if isinstance(value, (int, float, complex)):             
                  mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_watthours' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_kwatthours' +  '.HelmSmart'   ) )         

 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FF07: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass


          #PGN65288: SeaSmart ac detail 0x0FF08
          elif record[PGN] == '00FF08':


            try:

              pgntype = fact.get('pgntype',0)
              # checkt if type is 0xE199 which belongs to SeaSmart
              if pgntype == 57753:
                
                instance = fact.get('instance', 0)
                valuetype = fact.get('ac_type', 'UTIL')


                volts = fact.get('ac_volts_detail', 'NULL')
                if isinstance(volts, (int, float, complex)):             
                  mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(volts) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_line_neutral_volts' +  '.HelmSmart'   ) )         
                    
   
                amps = fact.get('ac_amps_detail', 'NULL')
                if isinstance(amps, (int, float, complex)):             
                  mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(amps) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_amps' +  '.HelmSmart'   ) )         

                if amps != 'NULL' and volts != 'NULL' :
                  watts = volts * amps
                  if isinstance(watts, (int, float, complex)):             
                    mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(watts) * 0.001,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_watts' +  '.HelmSmart'   ) )         

   
                status = fact.get('status', 'NULL')
                if isinstance(amps, (int, float, complex)):             
                  mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(status) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:status' +  '.HelmSmart'   ) )         
                  
 
 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FF08: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass

            
            


          #PGN65005: J1939 PGN 65005 - (0x00FDED) Utility Total Energy
          elif record[PGN] == '00FDED':

            try:

              instance = fact.get('instance', 0)
              valuetype = fact.get('type_reference', 'UTIL')

              value = fact.get('export_kwatt_hours', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_total_energy' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:export_kwatt_hours' +  '.HelmSmart'   ) )         

              value = fact.get('import_kwatt_hours', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_total_energy' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:import_kwatt_hours' +  '.HelmSmart'   ) )         

 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FDED: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass

      
          #PGN65014: J1939 PGN 65014 - (0x00FDF6) Utility Phase A Basic AC Quantities
          elif record[PGN] == '00FDF6':

            try:
              instance = fact.get('instance', 0)
              valuetype = fact.get('type_reference', 'UTIL')

              value = fact.get('ac_line_line_volts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_line_line_volts' +  '.HelmSmart'   ) )         

              value = fact.get('ac_line_neutral_volts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_line_neutral_volts' +  '.HelmSmart'   ) )         
                  
              value = fact.get('ac_frequency', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.0078125,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_frequency' +  '.HelmSmart'   ) )         

              value = fact.get('ac_amps', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_amps' +  '.HelmSmart'   ) )         
                  
              value = fact.get('ac_watts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_watts' +  '.HelmSmart'   ) )         

              #if debug_all: log.info('PGN65014:  j1939_engine_temps %s', mydataIDBC)
 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FDF6: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass




            
          #PGN65011: J1939 PGN 65011 - (0x00FDF3) Utility Phase B Basic AC Quantities
          elif record[PGN] == '00FDF3':

            try:

              instance = fact.get('instance', 1)
              valuetype = fact.get('type_reference', 'UTIL')

              value = fact.get('ac_line_line_volts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_line_line_volts' +  '.HelmSmart'   ) )         

              value = fact.get('ac_line_neutral_volts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_line_neutral_volts' +  '.HelmSmart'   ) )         
                  
              value = fact.get('ac_frequency', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.0078125,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_frequency' +  '.HelmSmart'   ) )         

              value = fact.get('ac_amps', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_amps' +  '.HelmSmart'   ) )         
                   
              value = fact.get('ac_watts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_watts' +  '.HelmSmart'   ) )         

                 
 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FDF3: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass


      
          #PGN65008: J1939 PGN 65008 - (0x00FDF0) Utility Phase C Basic AC Quantities
          elif record[PGN] == '00FDF0':

            try:

              instance = fact.get('instance', 2)
              valuetype = fact.get('type_reference', 'UTIL')

              value = fact.get('ac_line_line_volts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_line_line_volts' +  '.HelmSmart'   ) )         

              value = fact.get('ac_line_neutral_volts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_line_neutral_volts' +  '.HelmSmart'   ) )         
                  
              value = fact.get('ac_frequency', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.0078125,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_frequency' +  '.HelmSmart'   ) )         

              value = fact.get('ac_amps', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_amps' +  '.HelmSmart'   ) )         
                  
                  
              value = fact.get('ac_watts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_watts' +  '.HelmSmart'   ) )         
 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FDF0: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass



      
          #PGN65017: J1939 65017 - (0x0FDF9) Utility Average Basic AC Quantities
          elif record[PGN] == '00FDF9':

            try:

              instance = fact.get('instance', 3)
              valuetype = fact.get('type_reference', 'UTIL')

              value = fact.get('ac_line_line_volts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_line_line_volts' +  '.HelmSmart'   ) )         

              value = fact.get('ac_line_neutral_volts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_line_neutral_volts' +  '.HelmSmart'   ) )         
                  
              value = fact.get('ac_frequency', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.0078125,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_frequency' +  '.HelmSmart'   ) )         

              value = fact.get('ac_amps', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_amps' +  '.HelmSmart'   ) )         
                  
                  
              value = fact.get('ac_watts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_watts' +  '.HelmSmart'   ) )         
 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FDF9: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass




          #PGN65018: J1939 PGN 65018 - (0x00FDFA) Generator Total Energy
          elif record[PGN] == '00FDFA':

            try:

              instance = fact.get('instance', 0)
              valuetype = fact.get('type_reference', 'GEN')

              value = fact.get('export_kwatt_hours', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_total_energy' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:export_kwatt_hours' +  '.HelmSmart'   ) )         

              value = fact.get('import_kwatt_hours', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_total_energy' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:import_kwatt_hours' +  '.HelmSmart'   ) )         

 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FDFA: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass

      
          #PGN65027: J1939 PGN 65027 - (0x00FE03) Generator Phase A Basic AC Quantities
          elif record[PGN] == '00FE03':

            try:

              instance = fact.get('instance', 0)
              valuetype = fact.get('type_reference', 'GEN')

              value = fact.get('ac_line_line_volts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_line_line_volts' +  '.HelmSmart'   ) )         

              value = fact.get('ac_line_neutral_volts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_line_neutral_volts' +  '.HelmSmart'   ) )         
                  
              value = fact.get('ac_frequency', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.0078125,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_frequency' +  '.HelmSmart'   ) )         

              value = fact.get('ac_amps', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_amps' +  '.HelmSmart'   ) )         
                  
              value = fact.get('ac_watts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_watts' +  '.HelmSmart'   ) )         

              #if debug_all: log.info('PGN65014:  j1939_engine_temps %s', mydataIDBC)
 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FE03: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass



            
          #PGN65024: J1939 PGN 65024 - (0x00FE00) Generator Phase B Basic AC Quantities
          elif record[PGN] == '00FE00':

            try:

              instance = fact.get('instance', 1)
              valuetype = fact.get('type_reference', 'GEN')

              value = fact.get('ac_line_line_volts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_line_line_volts' +  '.HelmSmart'   ) )         

              value = fact.get('ac_line_neutral_volts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_line_neutral_volts' +  '.HelmSmart'   ) )         
                  
              value = fact.get('ac_frequency', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.0078125,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_frequency' +  '.HelmSmart'   ) )         

              value = fact.get('ac_amps', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_amps' +  '.HelmSmart'   ) )         
                   
              value = fact.get('ac_watts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_watts' +  '.HelmSmart'   ) )         

                 

 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FE00: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass

      
          #PGN65021: J1939 PGN 65021 - (0x00FDFD) Generator Phase C Basic AC Quantities
          elif record[PGN] == '00FDFD':

            try:

              instance = fact.get('instance', 2)
              valuetype = fact.get('type_reference', 'GEN')

              value = fact.get('ac_line_line_volts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_line_line_volts' +  '.HelmSmart'   ) )         

              value = fact.get('ac_line_neutral_volts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_line_neutral_volts' +  '.HelmSmart'   ) )         
                  
              value = fact.get('ac_frequency', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.0078125,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_frequency' +  '.HelmSmart'   ) )         

              value = fact.get('ac_amps', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_amps' +  '.HelmSmart'   ) )         
                  
                  
              value = fact.get('ac_watts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_watts' +  '.HelmSmart'   ) )         

 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FDFD: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass


      
          #PGN65030: J1939 65030 - (0x0FE06) Generator Average Basic AC Quantities
          elif record[PGN] == '00FE06':

            try:

              instance = fact.get('instance', 3)
              valuetype = fact.get('type_reference', 'GEN')

              value = fact.get('ac_line_line_volts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_line_line_volts' +  '.HelmSmart'   ) )         

              value = fact.get('ac_line_neutral_volts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_line_neutral_volts' +  '.HelmSmart'   ) )         
                  
              value = fact.get('ac_frequency', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 0.0078125,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_frequency' +  '.HelmSmart'   ) )         

              value = fact.get('ac_amps', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_amps' +  '.HelmSmart'   ) )         
                  
                  
              value = fact.get('ac_watts', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_basic' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:ac_watts' +  '.HelmSmart'   ) )         

 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FE06: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass





          #PGN65005: J1939 PGN 65018 - (0x00FDFA) GEN Total Energy
          elif record[PGN] == '00FDFA':

            try:

              instance = fact.get('instance', 0)
              valuetype = fact.get('type_reference', 'GEN')

              value = fact.get('export_kwatt_hours', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_total_energy' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:export_kwatt_hours' +  '.HelmSmart'   ) )         

              value = fact.get('import_kwatt_hours', 'NULL')
              if isinstance(value, (int, float, complex)):             
                mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], float(value) * 1.0,   'deviceid:' + record[DEVICE] + '.sensor:ac_total_energy' + '.source:' + record[SOURCE] + '.instance:' +  str(instance) + '.type:' +  str(valuetype) + '.parameter:import_kwatt_hours' +  '.HelmSmart'   ) )         

 
            except:
              e = sys.exc_info()[0] 
              if debug_all: log.info('Sync: Error in InfluxDBC.append mydataIDBC append PGN 00FDFA: %s',fact)
              if debug_all: log.info("Error: %s" % e)
              pass



  except TypeError as e:
    #if debug_all: log.info('Sync: TypeError in InfluxDBC mydata append %s:  ',  mydataIDBC)
    if debug_all: log.info('Sync: TypeError in InfluxDBC mydata append %s:%s:%s  ', record[DEVICE] , record[PGN] , fact)
    #e = sys.exc_info()[0]

    if debug_all: log.info('Sync: TypeError in InfluxDBC mydata append %s:  ' % str(e))
    
  except KeyError as e:
    if debug_all: log.info('Sync: KeyError in InfluxDBC mydata append %s:  ', mydataIDBC)
    #e = sys.exc_info()[0]

    if debug_all: log.info('Sync: KeyError in InfluxDBC mydata append %s:  ' % str(e))

  except NameError as e:
    if debug_all: log.info('Sync: Namerror in InfluxDBC mydata append %s: %s: %s: ', record[PGN], value, mydataIDBC)
    #e = sys.exc_info()[0]

    if debug_all: log.info('Sync: NameError in InfluxDBC mydata append %s:  ' % str(e))     
  except:
    #if debug_all: log.info('Sync: Error in InfluxDB mydata append %s. %s, %s, %s:  ', mydata, record[TIMESTAMP], value,'deviceid:001EC010AD69.sensor:environmental_data.instance:0.type:Outside_Temperature.parameter:temperature'  )
    if debug_all: log.info('Sync: Error in InfluxDBC mydata append %s:', mydataIDBC)

    e = sys.exc_info()[0]
    if debug_all: log.info("Error: %s" % e)
    #pass

  #if debug_all: log.info('Sync:  InfluxDB write mydata %s:  ', mydata)
 


  try:

    IFDBhost = os.environ.get('IFDBhost')
    IFDBport = os.environ.get('IFDBport')
    IFDBusername = os.environ.get('IFDBusername')
    IFDBpassword = os.environ.get('IFDBpassword')
    IFDBdatabase = os.environ.get('IFDBdatabase')
    
    
    #shim = Shim(host, port, username, password, database)
    #db = influxdb.InfluxDBClient(host, port, username, password, database)
    dbc = InfluxDBCloud(IFDBhost, IFDBport, IFDBusername, IFDBpassword, IFDBdatabase,  ssl=True)
    #dbc = InfluxDBCloud(IFDBhost, IFDBport, IFDBusername, IFDBpassword, IFDBdatabase,  ssl=False)

    #if debug_all: log.info('Sync:  InfluxDB write %s:  ', mydata)
    #if debug_all: log.info('Sync:  InfluxDB-Cloud write %s points', len(mydataIDBC))
    if debug_all: log.info('Sync:  InfluxDB-Cloud write device=%s  points = %s', record[DEVICE], len(mydataIDBC))
    #db.write_points_with_precision(mydata, time_precision='ms')


    #Add count of number of records written to local status
    mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], int(len(mydataIDBC)),   'deviceid:' + record[DEVICE] + '.sensor:helmsmartstat.source:FF.instance:0.type:NULL.parameter:write_records.HelmSmart'   ) )         

    #Add count of number of records written to global status
    ts = int(time.time()) * 1000
    #if debug_all: log.info('insert_influxdb_cloud: convert_influxdbcloud_json ts %s:  ', ts)
  
    myjsonkeys = { 'deviceid': device}
    #if debug_all: log.info('freeboard: convert_influxdbcloud_json myjsonkeys %s:  ', myjsonkeys)
    
      
    values = {'records':len(mydataIDBC)}
    measurement = 'HelmSmartDB'
    #if debug_all: log.info('insert_influxdb_cloud: convert_influxdbcloud_json values %s:  ', values)
    
    ifluxjson ={"measurement":measurement, "time": ts, "tags":myjsonkeys, "fields": values}
    mydataIDBC.append(ifluxjson)
    #if debug_all: log.info('insert_influxdb_cloud: convert_influxdbcloud_json tagpairs %s:  ', mydataIDBC)




    
    dbc.write_points(mydataIDBC, time_precision='ms')
    #shim.write_multi(mydata)
    if debug_all: log.info("Sync: write_points influxDB-Cloud! %s", record[DEVICE])

    
  #except influxdb.InfluxDBClientError as e:   
  except InfluxDBClientError as e:

    if debug_all: log.error('Sync: InfluxDBServerError error in InfluxDB-Cloud write %s:  ' % str(e))

  except InfluxDBServerError as e:
    if debug_all: log.info('Sync:  InfluxDB-Cloud write device=%s  points = %s', record[DEVICE], len(mydataIDBC))
    if debug_all: log.info('Sync: inFlux error in InfluxDBServer-Cloud write %s:  ' % str(e))    
    if debug_all: log.error('Sync: inFlux error in InfluxDBServer-Cloud write %s:  ' % str(e))
    pass
    
  except TypeError as e:
    if debug_all: log.error('Sync: TypeError in InfluxDB-Cloud write %s:  ', mydataIDBC)
    #e = sys.exc_info()[0]

    if debug_all: log.error('Sync: TypeError in InfluxDB-Cloud write %s:  ' % str(e))
    
  except KeyError as e:
    if debug_all: log.error('Sync: KeyError in InfluxDB-Cloud write %s:  ', mydataIDBC)
    #e = sys.exc_info()[0]

    if debug_all: log.error('Sync: KeyError in InfluxDB-Cloud write %s:  ' % str(e))

  except NameError as e:
    if debug_all: log.error('Sync: NameError in InfluxDB-Cloud write %s:  ', mydataIDBC)
    #e = sys.exc_info()[0]

    if debug_all: log.error('Sync: NameError in InfluxDB-Cloud write %s:  ' % str(e))   
    
    
  except:
    if debug_all: log.error('Sync: Error in InfluxDB-Cloud write %s:  ', mydataIDBC)
    e = sys.exc_info()[0]
    if debug_all: log.error("Error: %s" % e)
    
  if debug_all: log.info("inserted into influxDB-Cloud! %s", device)            
