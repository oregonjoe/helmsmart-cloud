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

from messagepost import process_message

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

sqs_queue = boto3.client('sqs', region_name=os.environ.get('AWS_REGION'), aws_access_key_id=environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY'))

#queue_url = 'SQS_QUEUE_URL'
#queue_url = 'https://sqs.us-east-1.amazonaws.com/291312677175/helmsmart-cloud'
#queue_url = 'https://sqs.us-east-1.amazonaws.com/291312677175/SeaSmart'
#queue_url = os.environ.get('SQS_QUEUE_URL')
queue_url = os.environ.get('SQS_ALERTS_URL')

import nmea
from splicer import Schema
SCHEMA=Schema([
  dict(name="device",type='STRING'),
  dict(name="partition",type='STRING'),
  dict(name="url",type='STRING'),
]+nmea.SCHEMA.fields)

from sync import (
  dump_pcdinfirebase, dump_json, insert_influxdb_cloud, ensure_database,PARTITION, URL
)

env = xlocal()

# JLB 081316  - added seperate influxdb-cloud record insert
#@instrument
def dump_influxdb_cloud(device, partition, records):

  try:
    
    #if debug_all: log.info('sqs_poller: fact_info in dump_influxdb_cloud  %s:  ', fact_info)
    
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
    if debug_all: log.info('sqs_alerts_poller TypeError in dump_influxdb_cloud  %s:  ' % str(e))
    
  except AttributeError as e:
    if debug_all: log.info('sqs_alerts_poller AttributeError in dump_influxdb_cloud  %s:  ' % str(e))
    
  except NameError as e:
    if debug_all: log.info('sqs_alerts_poller: NameError in dump_influxdb_cloud  %s:  ' % str(e))

  except:
    e = sys.exc_info()[0]
    if debug_all: log.info("sqs_alerts_poller: in dump_influxdb_cloud SSA300 Error: %s" % str(e))


def proc(alert_message):

  if debug_all: log.info("sqs_alerts_poller:alert_message %s", alert_message)
  
  alertKey = alert_message.get('key', 0) 
  alert_StartTime = alert_message.get('starttime',0) 
  alert_StartTime = alert_message.get('endtime',0)
  alert_payload = alert_message.get('payload', "") 
  alert_Parameters = alert_payload.get('parameters', "") 

  if debug_all: log.info("sqs_alerts_poller:alert_Parameters %s", alert_Parameters)    

  #looks up any alert actions and sends out SMS/Email/Switch/Dimmer/Timmer events
  #from messagepost import process_message
  process_message(alert_payload)



#reads num_receive messeges from SQS que
def get_messages(queue_url, num_receive):
  if debug_all: log.info('sqs_alerts_poller:get_messages %s', num_receive)
  try:
    #queue_url = environ.get('SQS_QUEUE_ALERTS_URL')  
    # read message from SQS queue
    response = sqs_queue.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        MessageAttributeNames=[  'All'  ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    if "Messages" not in response:
      if debug_all: log.info('sqs_alerts_poller:no messages left')
      return []

    #print(response['Messages'][0])
    print(f"Number of messages received: {len(response.get('Messages', []))}")

    message = response.get("Messages", [])[0]
    # print(message)
    #if debug_all: log.info("Read SQS:  message %s: ", message)
    
    message_body = message['Body']
    receipt_handle = message['ReceiptHandle']

    if debug_all: log.info("sqs_alerts_poller:Read SQS:  message_body %s: ", message_body)

    if debug_all: log.info("sqs_alerts_poller:Read SQS:  receipt_handle %s: ", receipt_handle)

    #if debug_all: log.info("get_messages:  response %s: ", rs['Messages'][0])

    #if debug_all: log.info('sqs_poller:get_messages read %s', len(rs))

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
  #queue_url = environ.get('SQS_QUEUE_ALERTS_URL')
  num_receive = int(os.environ.get('NUM_MESSAGES', 10))
  
  if debug_all: log.info('sqs_alerts_poller start process_queue %s: ', num_receive)
  # get redis que info
  #if debug_all: log.info('s3_poller jobs in queue %s: ', len(q))

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

      if debug_all: log.info('sqs_alerts_poller: process_queue %s: ', count)

      if debug_all: log.info("process_queue:  message %s: ", message)
      #if debug_all: log.info("process_queue:  message_MessageId %s: ", message['MessageId'])
      
      #try to get messages from the SQS queue and parse them
      if message != []:
        transaction(handle,  message)
        count += 1

      if count == 0:
        # if we had messages process right away, else
        if debug_all: log.info('sqs_alerts_poller process_queue sleeping: ')
        sleep(1)

    except NameError as e:
      #if debug_all: log.info("Read SQS:NameError device_id %s:  ", device_id)
      if debug_all: log.info('process_queue SQS:NameError  Error in que SQS %s:  ' % str(e))
      
    except TypeError as e:
      #if debug_all: log.info("Read SQS:NameError device_id %s:  ", device_id)
      if debug_all: log.info('process_queue SQS:TypeError  Error in que SQS %s:  ' % str(e))
      
    except:
      e = sys.exc_info()[0]
      #if debug_all: log.info('s3_poller: process_queue errror' % e)
      if debug_all: log.info('sqs_alerts_poller: process_queue errror  %s' % str(e))

    #end of while loop
        
  if debug_all: log.info('sqs_alerts_poller: exiting process_queue')


def interval(delay, method, *args, **kw):
  """
  Repeatedly call the same function.
  """

  while True:
    try:
      method(*args, **kw)
    except:
      log.exception("Error invoking %s", method)
      if debug_all: log.info('sqs_alerts_poller: Error invoking method%s', method)
      
    gevent.sleep(delay)


# trys to get a pushsmart message from the SQS que
def transaction(func, sqs_message):
  """Delete message if no errors."""
  #if debug_all: log.info('s3_poller: transaction %s', sqs_message.get_body())
  try:
    
    if debug_all: log.info('sqs_alerts_poller:transaction message %s', sqs_message['Body'])
    #queue_url = environ.get('SQS_QUEUE_ALERTS_URL')
    #func(sqs_message.get_body())
    #func(sqs_message['Body'])
    func(sqs_message)

    #proc(sqs_message)
    #sqs_message.delete()

    #receipt_handle = sqs_message['ReceiptHandle']
    receipt_handle = sqs_message['ReceiptHandle']
    if debug_all: log.info('sqs_alerts_poller: transaction ReceiptHandle  %s', receipt_handle)

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
    if debug_all: log.info('sqs_alerts_poller: transaction errror  %s' % str(e))

# tries to get pushsmart messages
# and if there is a problem will retry several times (3)?
# times before deleting them from the queue
def best_effort(func, pushsmart_message):
  #if debug_all: log.info('s3_poller:best_effort starting')
  message = json.loads(pushsmart_message['Body'])

  #if debug_all: log.info('sqs_poller:best_effort message %s', pushsmart_message['Body'])
  if debug_all: log.info('sqs_alerts_poller:best_effort message %s', message)

  
  try:
    func(message)
  except  Exception as e:
    if debug_all: log.info('sqs_alerts_poller:best_effort error %s' % str(e))
    
    retry_count = message.get('retries', 0) + 1
    if retry_count > env.max_retries:
      log.exception('Discarding due to errors: %s', pushsmart_message)
      if debug_all: log.info('sqs_alerts_poller:best_effort Discarding')
      
    else:
      log.exception('Retrying')
      if debug_all: log.info('sqs_alerts_poller:best_effort retrying')
      
      retry = message.copy()
      retry['retries'] = retry_count
      
      retry['errors'] = retry.get('errors', [])
      retry['errors'].append(str(e))

      #env.queue.write( env.queue.new_message(json.dumps(retry)) )
      #queue_url = environ.get('SQS_QUEUE_ALERTS_URL')

      # Send message to SQS queue
      response = sqs_queue.send_message(
          QueueUrl=queue_url,
          DelaySeconds=10,
          #MessageAttributes={ 'Device': {  'deviceid':device_id} },
          MessageBody=(json.dumps(retry))
      )

      #print(response['MessageId'])

      if debug_all: log.info("sqs_alerts_poller Send SQS:device_id %s:  response %s: ", device_id,response['MessageId'])

      
  

if __name__ == "__main__":
  #num_requests = int(os.environ.get('NUM_REQUESTS',1))
  num_requests =1
  

  db_pool = ConnectionPool(os.environ.get('DATABASE_URL'))
  #db_pool = ConnectionPool(os.environ.get('HEROKU_POSTGRESQL_MAUVE_URL'))
  
  
  conn = db_pool.getconn()
  fact_info = ensure_database(conn, SCHEMA)
  #db_pool.putconn(conn, close=True)  
  #if debug_all: log.info('sqs_poller: fact_info in main  %s:  ', fact_info)
  
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
