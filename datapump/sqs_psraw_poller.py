import os
from os import environ
from os import environ as env, path
#import pylibmc  
import sys

from psycopg_pool import ConnectionPool
from xlocal import xlocal
import json


from calendar import timegm
import datetime
from datetime import timezone
import time
from time import mktime
from time import sleep
from zoneinfo import ZoneInfo



#import md5
import hashlib
import base64
from operator import itemgetter
from itertools import groupby
from functools import partial

import gevent, gevent.monkey
import requests


import logging
# *******************************************************************
# Debug Output defines
# Comment to enable/disable
# ********************************************************************
debug_all = False
debug_all = True

logging.basicConfig(level=logging.DEBUG)
log = logging



from gevent.pool import Pool, Group

import botocore
import boto3
# Get the service resource
#sqs = boto3.resource('sqs')
#s3 = boto3.resource(service_name='sqs', region_name='REGION_NAME')
aws_region = os.environ.get('AWS_REGION')
#sqs_queue = boto3.client('sqs', region_name='us-west-2', aws_access_key_id=environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY'))
sqs_queue = boto3.client('sqs', region_name=os.environ.get('AWS_REGION'), aws_access_key_id=environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY'))
#queue_url = 'SQS_QUEUE_URL'
#queue_url = 'https://sqs.us-east-1.amazonaws.com/291312677175/helmsmart-cloud'
#queue_url = 'https://sqs.us-east-1.amazonaws.com/291312677175/SeaSmart'
queue_url= os.environ.get('SQS_PSRAW_URL')

from influxdb_client_3 import InfluxDBClient3, Point, WriteOptions


import nmea
from splicer import Schema
SCHEMA=Schema([
  dict(name="device",type='STRING'),
  dict(name="partition",type='STRING'),
  dict(name="url",type='STRING'),
]+nmea.SCHEMA.fields)


env = xlocal()


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
def seasmart_timestamp(timestamp, EPOCH=1262304000000):
  """
  char(6), char(2) -> datetime
  """
  #Get TimeStamp from PushSmart record
  #$PCDIN,01F010,6DOB8463,A7,0007040040AE3E0A*22
  #$PCDIN,01F010,[TIMESTAMP],A7,0007040040AE3E0A*22
  #Timestamp is Hex32 from 1/1/2010 (EPOCH 1262304000)

  #initialize pushsmart timestamp to 0
  ps_tms = int(time.time()) * 1000
  #ps_ts = int(timestamp[:6], 32) + EPOCH
  #return datetime.fromtimestamp(ps_ts)

  #But lets trap for a Hex32 format error just to be sure
  try:
    #ts = int(timestamp[:6], 32) + EPOCH
    # get seconds
    ts = int(timestamp[:6], 32) * 1000
    # get ms
    tms = int(timestamp[6:8], 32)
    tms = ts + tms
  except:
    if debug_all: log.info("NMEA get timestamp format error - timestamp %s ", timestamp)
    return ps_tms

  #return datetime.fromtimestamp(ts +  EPOCH)

  # and check that we have a date between now and 1/1/2010
  if tms <= 0:
    if debug_all: log.info("NMEA get timestamp error - negitive timestamp %s ", timestamp)
    return ps_tms

  #return datetime.fromtimestamp(ts +  EPOCH)  
  # Get current time in mseconds
  current_tms = int(time.time()) * 1000
  #return datetime.fromtimestamp(ts +  EPOCH)
  # and be sure ts is not greater then current time as check
  if tms + int(EPOCH) <= current_tms:
    ps_tms = tms + EPOCH
    return ps_tms
  
  else:
    if debug_all: log.info("NMEA get timestamp error -  timestamp greater then current %s ", timestamp)
    return ps_tms
    
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
      client.write(database=database, record=point) 

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





# JLB 022025  - added seperate influxdb record insert
#@instrument
def dump_TCPserver(message):
  
  insert_influxdbCloud_TCPseries( message['device_id'], message['payload'] )
  #if debug_all: log.info('sqs_psraw_poller dump_TCPserver %s:  ', message['device_id'])


def proc(message):

  #062914 JLB
  # test to read custom message from SQS que
  try:
    #message_body = json.loads(message['Body'])
    message_body =message
    #partition = message_body['partition'][:-4]


    #if debug_all: log.info('sqs_post_poller proc Got SQS message_body %s:  ', message_body)

    mpartition = message_body.get('partition')
    device_id = message_body.get('device_id')

    #if debug_all: log.info('sqs_post_poller Got SQS message %s: ', partition)
    if debug_all: log.info('sqs_psraw_poller Got SQS message %s: device %s ', mpartition,device_id)
    #partition = message['partition'][:-4]
    #if debug_all: log.info('sqs_post_poller Got SQS message %s: ', partition)
    #if debug_all: log.info('sqs_post_poller Got SQS message %s: device %s ', partition, message['device_id'])
    
    #if debug_all: log.info('sqs_post_poller proc Got SQS message_body %s:  ', message_body)

    partition = mpartition[:-4]
    if debug_all: log.info('sqs_psraw_poller Got SQS message partition %s: ', partition)
    



    # ##########################################################
    # Got a message from a seasmart gateway via HTTP POST
    # ##########################################################
    if "SSA300" in partition:  
      try:
        #if debug_all: log.info('sqs_post_poller Got PushSmart SQS message %s: ', partition)
        if debug_all: log.info('sqs_psraw_poller Got PushSmart RAW SQS message %s: %s ', partition, device_id)

        schema = SCHEMA
        #device = message['device_id']
        #partition = message['partition'][:-4]

        message_payload = message_body.get('payload')
        #if debug_all: log.info('sqs_post_poller Got SQS message_payload %s: ', message_payload)

        # added 022025 to put raw pushsmart data into inFluxDB for TCPserver
        dump_TCPserver(message_body)
        


      except TypeError as e:
        if debug_all: log.info('sqs_psraw_poller:proc: TypeError in proc  %s:  ', partition)
        if debug_all: log.info('sqs_psraw_poller:proc: TypeError in proc  %s:  ' % str(e))
        
      except AttributeError as e:
        if debug_all: log.info('sqs_psraw_poller:proc: AttributeError in proc  %s:  ', partition)
        if debug_all: log.info('sqs_psraw_poller:proc: AttributeError in proc  %s:  ' % str(e))
        
      except NameError as e:
        if debug_all: log.info('sqs_psraw_poller:proc: NameError in proc  %s:  ', partition)
        if debug_all: log.info('sqs_psraw_poller:proc: NameError in proc  %s:  ' % str(e))

      except:
        if debug_all: log.info('sqs_psraw_poller:proc: Error in proc SSA300 %s:', partition)
        e = sys.exc_info()[0]
        if debug_all: log.info("sqs_psraw_poller:proc:  in proc SSA300 Error: %s" % str(e))
        pass


  except AttributeError as e:
    #if debug_all: log.info('sqs_post_poller:: TypeError in proc  %s:  ', partition)

    if debug_all: log.info('sqs_psraw_poller:: TypeError in proc  %s:  ' % str(e))
    
  except TypeError as e:
    #if debug_all: log.info('sqs_post_poller:: TypeError in proc  %s:  ', partition)

    if debug_all: log.info('sqs_psraw_poller:: TypeError in proc  %s:  ' % str(e))
      
  except KeyError as e:
    #if debug_all: log.info('sqs_post_poller:: KeyError in proc %s:  ', partition)

    if debug_all: log.info('sqs_psraw_poller:: KeyError in proc  %s:  ' % str(e))

  except NameError as e:
    #if debug_all: log.info('sqs_post_poller:: NameError in proc  %s:  ', partition)

    if debug_all: log.info('sqs_psraw_poller:: NameError in proc  %s:  ' % str(e))
      
  except:
    #if debug_all: log.info('sqs_post_poller:: Error in proc  %s:', partition)

    e = sys.exc_info()[0]
    if debug_all: log.info("sqs_psraw_poller::  in proc Error: %s" % e)
    pass     

#reads num_receive messeges from SQS que
def get_messages(queue_url, num_receive):
  if debug_all: log.info('sqs_psraw_poller:get_messages %s', num_receive)
  try:
    
    # read message from SQS queue
    response = sqs_queue.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        MessageAttributeNames=[  'All'  ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    if "Messages" not in response:
      if debug_all: log.info('sqs_psraw_poller:no messages left')
      return []

    #print(response['Messages'][0])
    print(f"Number of messages received: {len(response.get('Messages', []))}")

    message = response.get("Messages", [])[0]
    # print(message)
    #if debug_all: log.info("Read SQS:  message %s: ", message)
    
    message_body = message['Body']
    receipt_handle = message['ReceiptHandle']

    #if debug_all: log.info("Read SQS:  message_body %s: ", message_body)

    if debug_all: log.info("Read SQS:  receipt_handle %s: ", receipt_handle)

    #if debug_all: log.info("get_messages:  response %s: ", rs['Messages'][0])

    #if debug_all: log.info('sqs_post_poller:get_messages read %s', len(rs))

    #return rs
    return message
  

  except botocore.exceptions.ClientError as e:
    #if debug_all: log.info("Read SQS:ClientError device_id %s:  ", device_id)
    if debug_all: log.info('Read SQS:ClientError  Error in que SQS %s:  ' % str(e))

  except botocore.exceptions.ParamValidationError as e:
   # if debug_all: log.info("Read SQS:ParamValidationError device_id %s:  ", device_id)
    if debug_all: log.info('Read SQS:ParamValidationError  Error in que SQS %s:  ' % str(e))

  except NameError as e:
    #if debug_all: log.info("Read SQS:NameError device_id %s:  ", device_id)
    if debug_all: log.info('Read SQS:NameError  Error in que SQS %s:  ' % str(e))
    
  except:
    e = sys.exc_info()[0]
    #if debug_all: log.info("Send SQS:device_id %s:  ", device_id)
    if debug_all: log.info('Send SQS: Error in que SQS %s:  ' % str(e))

    log.warn(e)
    return []



def process_queue(config):  
  #queue = boto.connect_sqs().lookup(os.environ['SQS_QUEUE'])
  #queue_url = environ.get('SQS_QUEUE_URL')
  num_receive = int(os.environ.get('NUM_MESSAGES', 10))
  
  if debug_all: log.info('sqs_psraw_poller start process_queue %s: ', num_receive)
  # get redis que info
  #if debug_all: log.info('sqs_post_poller jobs in queue %s: ', len(q))

  # create the partial that parses messages using proc function
  # and if it can't  - returns them to the SQS queue or deletes them if we tried
  # too many times
  handle = partial(best_effort, proc)
  #with env(**dict(queue=queue_url, **config)):

  #infinate loop
  while True:
    count = 0

    try:

      #get messages from SQS queue and try to process them with the PROC function
      #for message in get_messages(queue_url, num_receive):
      message=get_messages(queue_url, num_receive)

      if debug_all: log.info('sqs_psraw_poller process_queue %s: ', count)

      if debug_all: log.info("process_queue:  message %s: ", message)
      #if debug_all: log.info("process_queue:  message_MessageId %s: ", message['MessageId'])
      
      #try to get messages from the SQS queue and parse them
      if message != []:
        transaction(handle,  message)
        count += 1

      if count == 0:
        # if we had messages process right away, else
        if debug_all: log.info('sqs_psraw_poller process_queue sleeping: ')
        sleep(1)

    except NameError as e:
      #if debug_all: log.info("Read SQS:NameError device_id %s:  ", device_id)
      if debug_all: log.info('process_queue SQS:NameError  Error in que SQS %s:  ' % str(e))
      
    except TypeError as e:
      #if debug_all: log.info("Read SQS:NameError device_id %s:  ", device_id)
      if debug_all: log.info('process_queue SQS:TypeError  Error in que SQS %s:  ' % str(e))
      
    except:
      e = sys.exc_info()[0]
      #if debug_all: log.info('sqs_post_poller: process_queue errror' % e)
      if debug_all: log.info('sqs_psraw_poller: process_queue errror  %s' % str(e))

    #end of while loop
        
  if debug_all: log.info('sqs_psraw_poller: exiting process_queue')


def interval(delay, method, *args, **kw):
  """
  Repeatedly call the same function.
  """

  while True:
    try:
      method(*args, **kw)
    except:
      log.exception("Error invoking %s", method)
      if debug_all: log.info('sqs_psraw_poller: Error invoking method%s', method)
      
    gevent.sleep(delay)


# trys to get a pushsmart message from the SQS que
def transaction(func, sqs_message):
  """Delete message if no errors."""
  #if debug_all: log.info('sqs_post_poller: transaction %s', sqs_message.get_body())
  try:
    
    if debug_all: log.info('sqs_psraw_poller:transaction message %s', sqs_message['Body'])
    #queue_url = environ.get('SQS_QUEUE_URL')
    #func(sqs_message.get_body())
    #func(sqs_message['Body'])
    func(sqs_message)

    #proc(sqs_message)
    #sqs_message.delete()

    #receipt_handle = sqs_message['ReceiptHandle']
    receipt_handle = sqs_message['ReceiptHandle']
    if debug_all: log.info('sqs_psraw_poller: transaction ReceiptHandle  %s', receipt_handle)

    # Delete received message from queue
    sqs_queue.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    print('Received and deleted message: %s' % sqs_message)

  except AttributeError as e:
    #if debug_all: log.info("Read SQS:NameError device_id %s:  ", device_id)
    if debug_all: log.info('transaction SQS:AttributeError  Error in que SQS %s:  ' % str(e))
    
  except NameError as e:
    #if debug_all: log.info("Read SQS:NameError device_id %s:  ", device_id)
    if debug_all: log.info('transaction SQS:NameError  Error in que SQS %s:  ' % str(e))
    
  except TypeError as e:
    #if debug_all: log.info("Read SQS:NameError device_id %s:  ", device_id)
    if debug_all: log.info('transaction SQS:TypeError  Error in que SQS %s:  ' % str(e))

  except:
    e = sys.exc_info()[0]
    if debug_all: log.info('sqs_post_poller: transaction errror  %s' % str(e))

# tries to get pushsmart messages
# and if there is a problem will retry several times (3)?
# times before deleting them from the queue
def best_effort(func, pushsmart_message):
  #if debug_all: log.info('sqs_post_poller:best_effort starting')
  message = json.loads(pushsmart_message['Body'])

  #if debug_all: log.info('sqs_post_poller:best_effort message %s', pushsmart_message['Body'])
  if debug_all: log.info('sqs_psraw_poller:best_effort message %s', message)

  
  try:
    func(message)
  except  Exception as e:
    if debug_all: log.info('sqs_psraw_poller:best_effort error %s' % str(e))
    
    retry_count = message.get('retries', 0) + 1
    if retry_count > env.max_retries:
      log.exception('Discarding due to errors: %s', pushsmart_message)
      if debug_all: log.info('sqs_post_poller:best_effort Discarding')
      
    else:
      log.exception('Retrying')
      if debug_all: log.info('sqs_psraw_poller:best_effort retrying')
      
      retry = message.copy()
      retry['retries'] = retry_count
      
      retry['errors'] = retry.get('errors', [])
      retry['errors'].append(str(e))

      #env.queue.write( env.queue.new_message(json.dumps(retry)) )


      # Send message to SQS queue
      response = sqs_queue.send_message(
          QueueUrl=queue_url,
          DelaySeconds=10,
          #MessageAttributes={ 'Device': {  'deviceid':device_id} },
          MessageBody=(json.dumps(retry))
      )

      #print(response['MessageId'])

      if debug_all: log.info("sqs_psraw_poller Send SQS:device_id %s:  response %s: ", device_id,response['MessageId'])

      
  

if __name__ == "__main__":
  #num_requests = int(os.environ.get('NUM_REQUESTS',1))
  num_requests =1
  

  db_pool = ConnectionPool(os.environ.get('DATABASE_URL'))
  #db_pool = ConnectionPool(os.environ.get('HEROKU_POSTGRESQL_MAUVE_URL'))
  
  
  conn = db_pool.getconn()
  #fact_info = ensure_database(conn, SCHEMA)
  #db_pool.putconn(conn, close=True)  
  #if debug_all: log.info('sqs_post_poller: fact_info in main  %s:  ', fact_info)
  
  config = dict(
    device_group = os.environ['DEVICE_GROUP'],
    db_pool = db_pool ,
    #s3_bucket = bucket(),
    #fact_info = fact_info,
    max_retries = os.environ.get('MAX_RETRIES',3)
  )



  
  group = Group()
  for x in range(num_requests):
    group.add(gevent.spawn(process_queue, config))
  
  #group.add(gevent.spawn(interval, 60, purge_firebase, TARGET_FIREBASE_ENTRIES))
  group.join()

    # todo: 
    # update date_dim
    # scale process based on queue length
