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

from influxdb import InfluxDBClient as InfluxDBCloud
from influxdb.client import InfluxDBClientError
from influxdb.client import InfluxDBServerError


from influxdb_client_3 import InfluxDBClient3, Point, WriteOptions

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

    

#022225 JLB added to convert PushSmart record to influxdb-cloud JSON
def convert_influxdb_cloud_tcpjson(psvalue,  deviceid):
  ifluxjson ={}
  
  try:

    PGN = "000000"
    #mydtt = datetime.strptime(mytime, "%Y-%m-%d %H:%M:%S")

    #dtt = mytime.timetuple()
    #ts = int(mktime(dtt) * 1000)
    ps_tms = int(time.time() * 1000)
 
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
    value = psvalue.strip("b\'")
    valuepairs = value.split(",")
    # check if we have proper formatted pushsmart string
    if len(valuepairs) != 5:
      return {}
    
    elif valuepairs[0] != '$PCDIN':
      return {}

    #Check PGN length is correct
    elif len(valuepairs[1]) != 6:
      return {}

    #check if timestamp length is correct
    elif len(valuepairs[2]) != 8:
      return {}

    #check if source length is correct
    elif len(valuepairs[3]) != 2:
      return {}
    
    #check if payload is terminated with * checksum
    elif len(valuepairs[4]) < 8:    
      return {}

    #check if payload is terminated with * checksum
    elif (valuepairs[4][len(valuepairs[4])-3] != '*') and (valuepairs[4][len(valuepairs[4])-4] != '*'):
      return {}
      
    # all good fields so go ahead and set values and timestamp
    else:
      ps_tms = seasmart_timestamp(valuepairs[2])


    """  
    #Example KEY
    #key = 'deviceid:{}.sensor:tcp.source:0.instance:0.type:pushsmart.parameter:raw.HelmSmart'.format(deviceid)
    tagpairs = key.split(".")
    if debug_all: log.info('freeboard: convert_influxdbcloud_json tagpairs %s:  ', tagpairs)

    myjsonkeys={}

    tag0 = tagpairs[0].split(":")
    tag1 = tagpairs[1].split(":")
    tag2 = tagpairs[2].split(":")
    tag3 = tagpairs[3].split(":")
    tag4 = tagpairs[4].split(":")
    tag5 = tagpairs[5].split(":")
    
    """
    #"deviceid:001EC010AD69.sensor:environmental_data.source:0.instance:0.type:Outside_Temperature.parameter:temperature.HelmSmart"
    #myjsonkeys = { 'deviceid':tag0[1], 'sensor':tag1[1], 'source':tag2[1], 'instance':tag3[1], 'type':tag4[1], 'parameter':tag5[1]}
    #myjsonkeys = { 'deviceid':tag0[1], 'sensor':tag1[1], 'source':tag2[1], 'instance':tag3[1], 'type':PGN, 'parameter':'raw'}
    #if debug_all: log.info('freeboard: convert_influxdbcloud_json myjsonkeys %s:  ', myjsonkeys)

    #values = {'value':value}
    #values = {tag5[1]:value}
    measurement = 'HS_'+str(deviceid)+'_psraw'
    #ifluxjson ={"measurement":tagpairs[6], "time": ts, "tags":myjsonkeys, "fields": values}
    #ifluxjson ={"measurement":measurement, "time": ts, "tags":myjsonkeys, "fields": values}
    ifluxjson ={"measurement":measurement, "time":ps_tms*1000000,  'deviceid':deviceid, 'source':valuepairs[3], "raw": value}
    if debug_all: log.info('freeboard: convert_influxdbcloud_json %s:  ', ifluxjson)


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
  if debug_all_influxdb: log.info("start of insert_influxdbCloud_TCPseries insert...")

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

    #write_api = client.write_api(write_options=SYNCHRONOUS)
    #write_options=SYNCHRONOUS
    #tcpmessages = message.split("\r\n")
    tcpmessages = message.split("\\r\\n")

    if debug_all: log.info("insert_influxdbCloud_TCPseries tcpmessages %s : %s", len(tcpmessages), tcpmessages)


    key = 'deviceid:{}.sensor:tcp.source:0.instance:0.type:pushsmart.parameter:raw.HelmSmart'.format(deviceid)
    
    influxdata = []
    for record in tcpmessages:
      
      #influxdata_record = convert_influxdb_cloud_tcpjson(record,  key)
      influxdata_record = convert_influxdb_cloud_tcpjson(record,  deviceid)
       
      if influxdata_record != {}:
        influxdata.append(influxdata_record)

    if debug_all: log.info("insert_influxdbCloud_TCPseries influxdata %s:", influxdata)

    """
    data = {
      "point1": {
        "deviceid": "001EC010AD69",
        "source": "82",
        "raw": "$PCDIN,01FD09,E7K6OT0A,82,FF410001A555FFFF*45",
        "time": 1740099837
      },
      "point2": {
        "deviceid": "001EC010AD69",
        "source": "82",
        "raw": "$PCDIN,01FD07,E7K6OT05,82,FF41A76CA5550504*3C",
        "time": 1740099838
      },
      "point3": {
        "deviceid": "001EC010AD69",
        "source": "82",
        "raw": "$PCDIN,01FD06,E7K6OT04,82,FFFFFFA76C0504FF*4D",
        "time": 1740099839
      },
      "point4": {
        "deviceid": "001EC010AD69",
        "source": "82",
        "raw": "$PCDIN,01FD02,E7K6OT03,82,FF240051B2F8FFFF*40",
        "time": 1740099840
      },
    }
    """


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
        "deviceid": "001EC010AD69",
        "source": "82",
        "raw": "$PCDIN,01FD02,E7K6OT03,82,FF240051B2F8FFFF*40",
      },
    }

    """
    for key in data:
      point = (
        Point("HS_001EC010AD69_raw")
        .tag("deviceid", data[key]["deviceid"])
        .tag("source", data[key]["source"])
        .field(data[key]["source"], data[key]["raw"])
      )
    """
    """    
    for key in data:
      point = (
        Point("HS_001EC010AD69_psraw")
        .tag("deviceid", data[key]["deviceid"])
        .tag("source", data[key]["source"])
        .field("psraw", data[key]["raw"])
        .time(data[key]["time"])
      )
    """
    #if debug_all_influxdb: log.info("insert_influxdbCloud_TCPseries data %s:", data)
    """        
    for key in data:
      point = (
        Point("HS_001EC010AD69_psraw")
        .tag("deviceid", data[key]["deviceid"])
        .tag("source", data[key]["source"])
        .field("psraw", data[key]["raw"])
      )
    """
 
    for key in influxdata:
      point = (
        Point(key['measurement'])
        .tag("deviceid", key["deviceid"])
        .tag("source", key["source"])
        .field("psraw", key["raw"])
        .time(key["time"])
      )

      if debug_all_influxdb: log.info("insert_influxdbCloud_TCPseries point %s", point)    
      #client.write(database=database, write_precision="s", record=point)
      #client.write(database=database, record=point, write_precision="s")
      #client.write(database=database, record=point, write_precision='ms')
      # seems to be a big problem in specifiying a time percision other then nsec
      #client.write(database=database, record=point, write_precision="ms")     
      #client.write(database=database, record=point) 

    #client.write(database=database, record=point)

    #client = InfluxDBClient(url=IFDBCURL, token=IFDBCToken)  

    client.close()
    
#  except influxdb_client_3.InfluxDBError as e:
#    if debug_all_influxdb: log.info('Sync: inFlux error in insert_influxdbCloud_TCPseries write %s:  ' % str(e))
    
  except TypeError as e:
    if debug_all_influxdb: log.info('Sync: TypeError in insert_influxdbCloud_TCPseries write %s:  ', deviceid)
    #e = sys.exc_info()[0]

    if debug_all_influxdb: log.info('Sync: TypeError in insert_influxdbCloud_TCPseries write %s:  ' % str(e))
    
  except KeyError as e:
    if debug_all_influxdb: log.info('Sync: KeyError in insert_influxdbCloud_TCPseries write %s:  ', deviceid)
    #e = sys.exc_info()[0]

    if debug_all_influxdb: log.info('Sync: KeyError in insert_influxdbCloud_TCPseries write %s:  ' % str(e))   

  except NameError as e:
    if debug_all_influxdb: log.info('Sync: NameError in insert_influxdbCloud_TCPseries write %s:  ', deviceid)
    #e = sys.exc_info()[0]

    if debug_all_influxdb: log.info('Sync: NameError in insert_influxdbCloud_TCPseries write %s:  ' % str(e))   

  except ValueError as e:
    if debug_all_influxdb: log.info('Sync: ValueError in insert_influxdbCloud_TCPseries write %s:  ', deviceid)
    #e = sys.exc_info()[0]

    if debug_all_influxdb: log.info('Sync: ValueError in insert_influxdbCloud_TCPseries write %s:  ' % str(e))



  except:
    if debug_all_influxdb: log.info('Sync: Error in insert_influxdbCloud_TCPseries write %s:  ', deviceid)
    e = sys.exc_info()[0]
    if debug_all_influxdb: log.info("Error: %s" % e)
    
  if debug_all_influxdb: log.info("inserted into insert_influxdbCloud_TCPseries!")



  
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
    #dbc.write_points(influxdata, time_precision='ms')
    
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
      








#legacy influxdb long term insert
def insert_influxdb(deviceid, mydataIDBC):

  try:

    IFDBhost = os.environ.get('IFDBhost')
    IFDBport = os.environ.get('IFDBport')
    IFDBusername = os.environ.get('IFDBusername')
    IFDBpassword = os.environ.get('IFDBpassword')
    IFDBdatabase = os.environ.get('IFDBdatabase')
    

    dbc = InfluxDBCloud(IFDBhost, IFDBport, IFDBusername, IFDBpassword, IFDBdatabase,  ssl=True)
    if debug_all: log.info('Sync:  InfluxDB write device=%s  points = %s', deviceid, len(mydataIDBC))
    #db.write_points_with_precision(mydata, time_precision='ms')


    #Add count of number of records written to local status
    #mydataIDBC.append(convert_influxdbcloud_json(record[TIMESTAMP], int(len(mydataIDBC)),   'deviceid:' + deviceid + '.sensor:helmsmartstat.source:FF.instance:0.type:NULL.parameter:write_records.HelmSmart'   ) )         

    """
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
    """

    
    if debug_all: log.info('insert_influxdb_cloud: convert_influxdbcloud_json tagpairs length %s:  ', len(mydataIDBC))

    
    client.write_points(mydataIDBC, time_precision='ms')

    if debug_all: log.info("Sync: write_points influxDB! %s", deviceid)

    
  #except influxdb.InfluxDBClientError as e:   
  except InfluxDBClientError as e:

    if debug_all: log.error('Sync: InfluxDBServerError error in InfluxDB-Cloud write %s:  ' % str(e))

  except InfluxDBServerError as e:
    if debug_all: log.info('Sync:  InfluxDB write device=%s  points = %s', deviceid, len(mydataIDBC))
    if debug_all: log.info('Sync: inFlux error in InfluxDBServer write %s:  ' % str(e))    
    if debug_all: log.error('Sync: inFlux error in InfluxDBServer write %s:  ' % str(e))
    pass
    
  except TypeError as e:
    if debug_all: log.error('Sync: TypeError in InfluxDB write %s:  ', deviceid)
    #e = sys.exc_info()[0]

    if debug_all: log.error('Sync: TypeError in InfluxDB write %s:  ' % str(e))
    
  except KeyError as e:
    if debug_all: log.error('Sync: KeyError in InfluxDB write %s:  ', deviceid)
    #e = sys.exc_info()[0]

    if debug_all: log.error('Sync: KeyError in InfluxDB write %s:  ' % str(e))

  except NameError as e:
    if debug_all: log.error('Sync: NameError in InfluxDB write %s:  ', deviceid)
    #e = sys.exc_info()[0]

    if debug_all: log.error('Sync: NameError in InfluxDB write %s:  ' % str(e))   
    
  except AttributeError as e:
    if debug_all: log.error('Sync: AttributeError in InfluxDB write %s:  ', deviceid)
    #e = sys.exc_info()[0]

    if debug_all: log.error('Sync: AttributeError in InfluxDB write %s:  ' % str(e))
    
  except:
    if debug_all: log.error('Sync: Error in InfluxDB write %s:  ', deviceid)
    e = sys.exc_info()[0]
    if debug_all: log.error("Error: %s" % e)
    
  if debug_all: log.info("inserted into influxDB! %s", deviceid)            



# short term influxdb insert 
def insert_influxdb3_cloud(deviceid, mydataIDBC):
  
  if debug_all: log.info("start of insert_influxdb3_cloud insert %s records", len(mydataIDBC))


  try:
	
    IFDBCToken = os.environ.get('InfluxDBCloudToken')
    IFDBCOrg = os.environ.get('InfluxDBCloudOrg')
    IFDBCBucket = os.environ.get('InfluxDBCloudBucket')
    IFDBCURL = os.environ.get('InfluxDBCloudURL')

    database=os.environ.get('IFDBDatabase')	
	
	
    client = InfluxDBClient3(host=IFDBCURL, token=IFDBCToken, org=IFDBCOrg)

    points = []
    
    for key in mydataIDBC:

      """      
      point = (
        Point(key['measurement'])
        .tag( key["tags"])
        .field(key["fields"])
        .time(key["time"])
      )
      """
      tags = key.get("tags", "")
      fields = key.get("fields", "")

      if debug_all: log.info('insert_influxdb3_cloud: convert_influxdbcloud_json tags %s:  ', tags)
      if debug_all: log.info('insert_influxdb3_cloud: convert_influxdbcloud_json fields %s:  ', fields)

      try:

        ps_tms = int(time.time() * 1000)
        #"time":ps_tms*1000000

        
        point = (
          Point(key['measurement'])
          .tag("deviceid", tags.get('deviceid','000000000000'))
          .tag("sensor", tags.get('sensor', 'unknown'))
          .tag("source", tags.get('source', '0'))
          .tag("instance", tags.get('instance', 'FF'))
          .tag("type", tags.get('type', 'unknown'))
          .tag("parameter", tags.get('parameter', 'records'))
          .field( tags.get('parameter', 'records'), fields[tags.get('parameter','records')])
          .time( ps_tms*1000000)
        )
        if debug_all: log.info('insert_influxdb3_cloud: convert_influxdbcloud_json point %s:  ', point)
        #client.write(database=database, record=point)
        
        points.append(point)
        
      except InfluxDBClient3.InfluxDBError as e:

        if debug_all: log.error('Sync: InfluxDBServerError error in InfluxDB3-Cloud write %s:  ' % str(e))
        
      except:
        
        if debug_all: log.error('Sync: Error in InfluxDB3-Cloud create point %s:  ', key)
        e = sys.exc_info()[0]
        if debug_all: log.error("Error: %s" % e)
        

    if debug_all: log.info('insert_influxdb_cloud: convert_influxdbcloud_json points %s:  ', len(points))
    
    #client.write_points(mydataIDBC, time_precision='ms')
    client.write(database=database, record=points) 
    #shim.write_multi(mydata)
    if debug_all: log.info("Sync: write_points influxDB3-Cloud! %s", deviceid)

    
  #except influxdb.InfluxDBClientError as e:   
  except InfluxDBClient3.InfluxDBError as e:

    if debug_all: log.error('Sync: InfluxDBServerError error in InfluxDB3-Cloud write %s:  ' % str(e))


  except TypeError as e:
    if debug_all: log.error('Sync: TypeError in InfluxDB3-Cloud write %s:  ', deviceid)
    #e = sys.exc_info()[0]

    if debug_all: log.error('Sync: TypeError in InfluxDB3-Cloud write %s:  ' % str(e))
    
  except KeyError as e:
    if debug_all: log.error('Sync: KeyError in InfluxDB3-Cloud write %s:  ', deviceid)
    #e = sys.exc_info()[0]

    if debug_all: log.error('Sync: KeyError in InfluxDB3-Cloud write %s:  ' % str(e))

  except NameError as e:
    if debug_all: log.error('Sync: NameError in InfluxDB3-Cloud write %s:  ', deviceid)
    #e = sys.exc_info()[0]

    if debug_all: log.error('Sync: NameError in InfluxDB3-Cloud write %s:  ' % str(e))   
    
  except AttributeError as e:
    if debug_all: log.error('Sync: AttributeError in InfluxDB3-Cloud write %s:  ', deviceid)
    #e = sys.exc_info()[0]

    if debug_all: log.error('Sync: AttributeError in InfluxDB3-Cloud write %s:  ' % str(e))
    
  except:
    if debug_all: log.error('Sync: Error in InfluxDB3-Cloud write %s:  ', deviceid)
    e = sys.exc_info()[0]
    if debug_all: log.error("Error: %s" % e)
    
  if debug_all: log.info("inserted into influxDB3-Cloud! %s", deviceid)            


    
	
