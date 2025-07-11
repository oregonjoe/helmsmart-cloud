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
#debug_all = True

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
queue_url= os.environ.get('SQS_POSTS_URL')

queue_url= "https://sqs.us-west-2.amazonaws.com/291312677175/helmsmart-cloud"



import nmea
from splicer import Schema
SCHEMA=Schema([
  dict(name="device",type='STRING'),
  dict(name="partition",type='STRING'),
  dict(name="url",type='STRING'),
]+nmea.SCHEMA.fields)

from sync import (
  dump_pcdinfirebase, dump_json, insert_influxdb_cloud,  ensure_database,PARTITION, URL
)


from helmsmart_influxdb import insert_influxdbCloud_TCPseries

env = xlocal()


# JLB 022025  - added seperate influxdb record insert
#@instrument
def dump_TCPserver(message):
  
  insert_influxdbCloud_TCPseries( message['device_id'], message['payload'] )


# JLB 081316  - added seperate influxdb-cloud record insert
#@instrument
def dump_influxdb_cloud(device, partition, records):

  try:
    
    #if debug_all: log.info('sqs_post_poller: fact_info in dump_influxdb_cloud  %s:  ', fact_info)
    
    insert_influxdb_cloud(
          #env.fact_info,
          fact_info,
          device,
          [
            [device, partition, "url"] + record
            for record in records
          ] 
        )
    
  except TypeError as e:
    if debug_all: log.info('sqs_post_poller TypeError in dump_influxdb_cloud  %s:  ' % str(e))
    
  except AttributeError as e:
    if debug_all: log.info('sqs_post_poller AttributeError in dump_influxdb_cloud  %s:  ' % str(e))
    
  except NameError as e:
    if debug_all: log.info('sqs_post_poller: NameError in dump_influxdb_cloud  %s:  ' % str(e))

  except:
    e = sys.exc_info()[0]
    if debug_all: log.info("sqs_post_poller: in dump_influxdb_cloud SSA300 Error: %s" % str(e))

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
    if debug_all: log.info('sqs_post_poller Got SQS message %s: device %s ', mpartition,device_id)
    #partition = message['partition'][:-4]
    #if debug_all: log.info('sqs_post_poller Got SQS message %s: ', partition)
    #if debug_all: log.info('sqs_post_poller Got SQS message %s: device %s ', partition, message['device_id'])
    
    #if debug_all: log.info('sqs_post_poller proc Got SQS message_body %s:  ', message_body)

    partition = mpartition[:-4]
    if debug_all: log.info('sqs_post_poller Got SQS message partition %s: ', partition)
    

      
    if "TESTSSEA00" in partition:
      try:
        if debug_all: log.info('Got Alert message %s: %s ', device_id, partition)


        try:
          records = message['payload']
          device = message['device_id']
          partition = message['partition'][:-4]
          switchdata = message.get('switchdata', {})
          if debug_all: log.info('sqs_post_poller:SSEA00 switch %s: %s ', device, switchdata)

          dimmerdata = message.get('dimmerdata', {})
          if debug_all: log.info('sqs_post_poller:SSEA00 dimmerdata %s: %s ', device, dimmerdata)

          timmerdata = message.get('timmerdata', {})
          if debug_all: log.info('sqs_post_poller:SSEA00 timmerdata %s: %s ', device, timmerdata)       
          
    
          if debug_all: log.info('sqs_post_poller got EmailAlert %s: %s', device, records)
          #dump_firebase(device,  "Alert", partition, json.dumps(records))
          dump_pcdinfirebase(device,  "Alert", partition, json.dumps(records))
          
          
          #if debug_all: log.info('sqs_post_poller: Alert message update_firebase_index %s: %s ', device, partition)
          #update_firebase_index(device, "Alert", partition)
          
          if debug_all: log.info('Inserted Alert message %s: %s ', device, partition)
          
        except:
          if debug_all: log.info('sqs_post_poller:: Error in proc SSEA00 %s:', partition)

          e = sys.exc_info()[0]
          if debug_all: log.info("sqs_post_poller::  in proc SSEA00 Error: %s" % e)
          pass


        #if timmerdata or (timmerdata != ""  and timmerdata != None and timmerdata is not None):
        #if timmerdata  is not {}:
        if timmerdata :
          #url = "https://api.telemetryapp.com/data"
          if debug_all: log.info('sqs_post_poller:SSEA00 timmerdata  %s ', timmerdata)
          timmerInstance  =timmerdata.get('instance',0)
          timmerType  =timmerdata.get('type','LED Dimmer 4 Channel')
          timmerParameter  =timmerdata.get('parameter','value0')
          timmerArray =timmerdata.get('timmer_array',"")
          
          devicedataurl = "http://helmsmart-cloud.herokuapp.com/settimmerapi?deviceid=" + str(device)
          devicedataurl = devicedataurl + "&instance=" + str(timmerInstance)
          devicedataurl = devicedataurl + "&type=" + str(timmerType)
          devicedataurl = devicedataurl + "&parameter=" + str(timmerParameter)
          devicedataurl = devicedataurl + "&array=" + str(timmerArray)

          if debug_all: log.info("sqs_post_poller:  in proc SSEA00 timmer: %s", devicedataurl)

          
          headers = {'content-type': 'application/json'}
          response = requests.get(devicedataurl)

        #if switchdata or (switchdata != ""  and switchdata != None and switchdata is not None):
        #if switchdata  is not {}:
        if switchdata :          
          #url = "https://api.telemetryapp.com/data"
          if debug_all: log.info('sqs_post_poller:SSEA00 switchdata  %s ', switchdata)
          switchInstance  =switchdata.get('instance',15)
          switchid  =switchdata.get('index',15)
          switchvalue =switchdata.get('value',3)

          devicedataurl = "http://helmsmart-cloud.herokuapp.com/setswitchapi?deviceid=" + str(device)
          devicedataurl = devicedataurl + "&instance=" + str(switchInstance)
          devicedataurl = devicedataurl + "&switchid=" + str(switchid)
          devicedataurl = devicedataurl + "&switchvalue=" + str(switchvalue)

          if debug_all: log.info("sqs_post_poller:  in proc SSEA00 switch: %s", devicedataurl)

          
          headers = {'content-type': 'application/json'}
          response = requests.get(devicedataurl)


        #if dimmerdata or (dimmerdata != ""  and dimmerdata != None and dimmerdata is not None):
        #if dimmerdata  is not {}:
        if dimmerdata  :                
          if debug_all: log.info('sqs_post_poller:SSEA00 dimmer  %s ', dimmerdata)
          dimmerInstance  =dimmerdata.get('instance',15)
          dimmerid  =dimmerdata.get('index',15)
          dimmervalue =dimmerdata.get('value',255)
          dimmeroverride =dimmerdata.get('override',0)
          
          devicedataurl = "http://helmsmart-cloud.herokuapp.com/setdimmerapi?deviceid=" + str(device)
          devicedataurl = devicedataurl + "&instance=" + str(dimmerInstance)
          devicedataurl = devicedataurl + "&dimmerid=" + str(dimmerid)
          devicedataurl = devicedataurl + "&dimmervalue=" + str(dimmervalue)
          devicedataurl = devicedataurl + "&dimmeroverride=" + str(dimmeroverride)
          
          if debug_all: log.info("sqs_post_poller:  in proc SSEA00 dimmer: %s", devicedataurl)

          
          headers = {'content-type': 'application/json'}
          response = requests.get(devicedataurl)






        
      except:
        if debug_all: log.info('sqs_post_poller:: Error in proc SSEA00 %s:', partition)

        e = sys.exc_info()[0]
        if debug_all: log.info("sqs_post_poller::  in proc SSEA00 Error: %s" % str(e))
        pass


    # ##########################################################
    # Got a message from a seasmart gateway via HTTP POST
    # ##########################################################
    elif "SSA300" in partition:  
      try:
        #if debug_all: log.info('sqs_post_poller Got PushSmart SQS message %s: ', partition)
        if debug_all: log.info('sqs_post_poller Got PushSmart SQS message %s: %s ', partition, device_id)

        schema = SCHEMA
        #device = message['device_id']
        #partition = message['partition'][:-4]

        message_payload = message_body.get('payload')
        #if debug_all: log.info('sqs_post_poller Got SQS message_payload %s: ', message_payload)

        # added 022025 to put raw pushsmart data into inFluxDB for TCPserver
        #dump_TCPserver(message_body)
        
        #records = nmea.loads(json.dumps(message_payload))
        #records = nmea.loads((message_payload))
        records = nmea.loads((json.dumps(message_payload)))
        #records = nmea.loads((json.dumps(message_payload).decode("utf-8")))
        #records = nmea.loads(message_payload.decode("utf-8"))
        #records = nmea.loads(json.loads(message_payload))
        #records = nmea.loads(message_payload)
        #if debug_all: log.info('sqs_post_poller Got SQS records %s: ', records) 

        mysortedrecords = sorted(records, key=lambda t:t[1])
        if debug_all: log.info('sqs_post_poller: PS message sorted device %s: %s ', device_id, mysortedrecords)


        if debug_all: log.info('sqs_post_poller dump_pcdinfirebase message_payload %s: ', partition)
        #print(message_payload)
        if debug_all: log.info('sqs_post_poller dump_pcdinfirebase %s: ', partition)
        #print(message_payload.replace('\\n', '\n').replace('\\r', '\r'))

        
        dump_pcdinfirebase(device_id, "PCDIN", partition, json.dumps(message_payload.replace('\\n', '\n').replace('\\r', '\r')))
        #dump_pcdinfirebase(device_id, "PCDIN", partition, message_payload)
        dump_pcdinfirebase(device_id, "JSON", partition, dump_json(schema, mysortedrecords))
        dump_pcdinfirebase(device_id, "SIGNALK", partition, dump_json(schema, mysortedrecords))

        if debug_all: log.info('sqs_post_poller: PS message dump_influxdb_cloud %s: %s ', device_id, partition)
        #if debug_all: log.info('sqs_post_poller: PS message dump_influxdb_cloud %s: %s ', device, partition)
        #081316 JLB - added influxdb-cloud update
        # write parsed nmea data to database
        dump_influxdb_cloud(device_id, partition, records)

      except TypeError as e:
        if debug_all: log.info('sqs_post_poller:proc: TypeError in proc  %s:  ', partition)
        if debug_all: log.info('sqs_post_poller:proc: TypeError in proc  %s:  ' % str(e))
        
      except AttributeError as e:
        if debug_all: log.info('sqs_post_poller:proc: AttributeError in proc  %s:  ', partition)
        if debug_all: log.info('sqs_post_poller:proc: AttributeError in proc  %s:  ' % str(e))
        
      except NameError as e:
        if debug_all: log.info('sqs_post_poller:proc: NameError in proc  %s:  ', partition)
        if debug_all: log.info('sqs_post_poller:proc: NameError in proc  %s:  ' % str(e))

      except:
        if debug_all: log.info('sqs_post_poller:proc: Error in proc SSA300 %s:', partition)
        e = sys.exc_info()[0]
        if debug_all: log.info("sqs_post_poller:proc:  in proc SSA300 Error: %s" % str(e))
        pass

    elif "SSLOG00" in partition:
      try:
        # JLB 063014 - test of not posting to S3
        #dump_s3(message)
        if debug_all: log.info('sqs_post_poller Got Log file message  %s: %s ', partition, device_id) 


        schema = SCHEMA
        #device = message['device_id']
        #partition = message['partition'][:-4]

        message_payload = message_body.get('payload')
        #if debug_all: log.info('sqs_post_poller Got SQS message_payload %s: ', message_payload)

        # added 022025 to put raw pushsmart data into inFluxDB for TCPserver
        #dump_TCPserver(message_body)
        
        #records = nmea.loads(json.dumps(message_payload))
        #records = nmea.loads((message_payload))
        records = nmea.loads((json.dumps(message_payload)))
        #records = nmea.loads((json.dumps(message_payload).decode("utf-8")))
        #records = nmea.loads(message_payload.decode("utf-8"))
        #records = nmea.loads(json.loads(message_payload))
        #records = nmea.loads(message_payload)
        #if debug_all: log.info('sqs_post_poller Got SQS records %s: ', records) 

        mysortedrecords = sorted(records, key=lambda t:t[1])
        if debug_all: log.info('sqs_post_poller: PS message sorted device %s: %s ', device_id, mysortedrecords)


        if debug_all: log.info('sqs_post_poller dump_pcdinfirebase message_payload %s: ', partition)
        #print(message_payload)
        if debug_all: log.info('sqs_post_poller dump_pcdinfirebase %s: ', partition)
        #print(message_payload.replace('\\n', '\n').replace('\\r', '\r'))

        
        dump_pcdinfirebase(device_id, "PCDIN", partition, json.dumps(message_payload.replace('\\n', '\n').replace('\\r', '\r')))
        #dump_pcdinfirebase(device_id, "PCDIN", partition, message_payload)
        dump_pcdinfirebase(device_id, "JSON", partition, dump_json(schema, mysortedrecords))
        dump_pcdinfirebase(device_id, "SIGNALK", partition, dump_json(schema, mysortedrecords))

        if debug_all: log.info('sqs_post_poller: PS message dump_influxdb_cloud %s: %s ', device_id, partition)
        #if debug_all: log.info('sqs_post_poller: PS message dump_influxdb_cloud %s: %s ', device, partition)
        #081316 JLB - added influxdb-cloud update
        # write parsed nmea data to database
        dump_influxdb_cloud(device_id, partition, records)

      except TypeError as e:
        if debug_all: log.info('sqs_post_poller:proc: TypeError in proc SSLOG00  %s:  ', partition)
        if debug_all: log.info('sqs_post_poller:proc: TypeError in proc SSLOG00  %s:  ' % str(e))
        
      except AttributeError as e:
        if debug_all: log.info('sqs_post_poller:proc: AttributeError in proc SSLOG00  %s:  ', partition)
        if debug_all: log.info('sqs_post_poller:proc: AttributeError in proc SSLOG00  %s:  ' % str(e))
        
      except NameError as e:
        if debug_all: log.info('sqs_post_poller:proc: NameError in proc SSLOG00  %s:  ', partition)
        if debug_all: log.info('sqs_post_poller:proc: NameError in proc SSLOG00  %s:  ' % str(e))

        
      except:
        if debug_all: log.info('sqs_post_poller:: Error in proc SSLOG00 %s:', partition)

        e = sys.exc_info()[0]
        if debug_all: log.info("sqs_post_poller::  in proc SSLOG00 Error: %s" % str(e))
        pass 
      

  except AttributeError as e:
    #if debug_all: log.info('sqs_post_poller:: TypeError in proc  %s:  ', partition)

    if debug_all: log.info('sqs_post_poller:: TypeError in proc  %s:  ' % str(e))
    
  except TypeError as e:
    #if debug_all: log.info('sqs_post_poller:: TypeError in proc  %s:  ', partition)

    if debug_all: log.info('sqs_post_poller:: TypeError in proc  %s:  ' % str(e))
      
  except KeyError as e:
    #if debug_all: log.info('sqs_post_poller:: KeyError in proc %s:  ', partition)

    if debug_all: log.info('sqs_post_poller:: KeyError in proc  %s:  ' % str(e))

  except NameError as e:
    #if debug_all: log.info('sqs_post_poller:: NameError in proc  %s:  ', partition)

    if debug_all: log.info('sqs_post_poller:: NameError in proc  %s:  ' % str(e))
      
  except:
    #if debug_all: log.info('sqs_post_poller:: Error in proc  %s:', partition)

    e = sys.exc_info()[0]
    if debug_all: log.info("sqs_post_poller::  in proc Error: %s" % e)
    pass     

#reads num_receive messeges from SQS que
def get_messages(queue_url, num_receive):
  if debug_all: log.info('sqs_post_poller:get_messages %s', num_receive)
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
      if debug_all: log.info('sqs_post_poller:no messages left')
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
  
  if debug_all: log.info('sqs_post_poller start process_queue %s: ', num_receive)
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

      if debug_all: log.info('sqs_post_poller process_queue %s: ', count)

      if debug_all: log.info("process_queue:  message %s: ", message)
      #if debug_all: log.info("process_queue:  message_MessageId %s: ", message['MessageId'])
      
      #try to get messages from the SQS queue and parse them
      if message != []:
        transaction(handle,  message)
        count += 1

      if count == 0:
        # if we had messages process right away, else
        if debug_all: log.info('sqs_post_poller process_queue sleeping: ')
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
      if debug_all: log.info('sqs_post_poller: process_queue errror  %s' % str(e))

    #end of while loop
        
  if debug_all: log.info('sqs_post_poller: exiting process_queue')


def interval(delay, method, *args, **kw):
  """
  Repeatedly call the same function.
  """

  while True:
    try:
      method(*args, **kw)
    except:
      log.exception("Error invoking %s", method)
      if debug_all: log.info('sqs_post_poller: Error invoking method%s', method)
      
    gevent.sleep(delay)


# trys to get a pushsmart message from the SQS que
def transaction(func, sqs_message):
  """Delete message if no errors."""
  #if debug_all: log.info('sqs_post_poller: transaction %s', sqs_message.get_body())
  try:
    
    if debug_all: log.info('sqs_post_poller:transaction message %s', sqs_message['Body'])
    #queue_url = environ.get('SQS_QUEUE_URL')
    #func(sqs_message.get_body())
    #func(sqs_message['Body'])
    func(sqs_message)

    #proc(sqs_message)
    #sqs_message.delete()

    #receipt_handle = sqs_message['ReceiptHandle']
    receipt_handle = sqs_message['ReceiptHandle']
    if debug_all: log.info('sqs_post_poller: transaction ReceiptHandle  %s', receipt_handle)

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
  if debug_all: log.info('sqs_post_poller:best_effort message %s', message)

  
  try:
    func(message)
  except  Exception as e:
    if debug_all: log.info('sqs_post_poller:best_effort error %s' % str(e))
    
    retry_count = message.get('retries', 0) + 1
    if retry_count > env.max_retries:
      log.exception('Discarding due to errors: %s', pushsmart_message)
      if debug_all: log.info('sqs_post_poller:best_effort Discarding')
      
    else:
      log.exception('Retrying')
      if debug_all: log.info('sqs_post_poller:best_effort retrying')
      
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

      if debug_all: log.info("sqs_post_poller Send SQS:device_id %s:  response %s: ", device_id,response['MessageId'])

      
  

if __name__ == "__main__":
  #num_requests = int(os.environ.get('NUM_REQUESTS',1))
  num_requests =1
  

  db_pool = ConnectionPool(os.environ.get('DATABASE_URL'))
  #db_pool = ConnectionPool(os.environ.get('HEROKU_POSTGRESQL_MAUVE_URL'))
  
  
  conn = db_pool.getconn()
  fact_info = ensure_database(conn, SCHEMA)
  #db_pool.putconn(conn, close=True)  
  #if debug_all: log.info('sqs_post_poller: fact_info in main  %s:  ', fact_info)
  
  config = dict(
    device_group = os.environ['DEVICE_GROUP'],
    db_pool = db_pool ,
    #s3_bucket = bucket(),
    fact_info = fact_info,
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
