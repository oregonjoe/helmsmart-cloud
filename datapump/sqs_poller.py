import os
from os import environ
from os import environ as env, path
import pylibmc  
import sys

from psycopg_pool import ConnectionPool

import json


from calendar import timegm
import datetime
from datetime import timezone
import time
from time import mktime
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
#debug_all = False
debug_all = True

logging.basicConfig(level=logging.DEBUG)
log = logging



from gevent.pool import Pool, Group

import botocore
import boto3
# Get the service resource
#sqs = boto3.resource('sqs')
#s3 = boto3.resource(service_name='sqs', region_name='REGION_NAME')

sqs_queue = boto3.client('sqs', region_name='us-east-1', aws_access_key_id=environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY'))

#queue_url = 'SQS_QUEUE_URL'
queue_url = 'https://sqs.us-east-1.amazonaws.com/291312677175/helmsmart-cloud'
#queue_url = 'https://sqs.us-east-1.amazonaws.com/291312677175/SeaSmart'


def proc(message):

  #062914 JLB
  # test to read custom message from SQS que
  try:
    partition = message['partition'][:-4]
    #if debug_all: log.info('s3_poller Got SQS message %s: ', partition)
    log.info('sqs_poller Got SQS message %s: device %s ', partition, message['device_id'])


  except TypeError as e:
    if debug_all: log.info('sqs_poller:: TypeError in proc  %s:  ', partition)

    if debug_all: log.info('sqs_poller:: TypeError in proc  %s:  ' % str(e))
      
  except KeyError as e:
    if debug_all: log.info('sqs_poller:: KeyError in proc %s:  ', partition)

    if debug_all: log.info('sqs_poller:: KeyError in proc  %s:  ' % str(e))

  except NameError as e:
    if debug_all: log.info('sqs_poller:: NameError in proc  %s:  ', partition)

    if debug_all: log.info('sqs_poller:: NameError in proc  %s:  ' % str(e))
      
  except:
    if debug_all: log.info('sqs_poller:: Error in proc  %s:', partition)

    e = sys.exc_info()[0]
    if debug_all: log.info("sqs_poller::  in proc Error: %s" % e)
    pass     

#reads num_receive messeges from SQS que
def get_messages(queue_url, num_receive):
  if debug_all: log.info('sqs_poller:get_messages %s', num_receive)
  try:
    
    # read message from SQS queue
    rs = sqs_queue.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        MessageAttributeNames=[  'All'  ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    

    #print(response['Messages'][0])

    log.info("Read SQS:device_id %s:  response %s: ", device_id,response['Messages'][0])

    if debug_all: log.info('sqs_poller:get_messages read %s', len(rs))

    return rs
  

  except botocore.exceptions.ClientError as e:
    log.info("Read SQS:ClientError device_id %s:  ", device_id)
    log.info('Read SQS:ClientError  Error in que SQS %s:  ' % e)

  except botocore.exceptions.ParamValidationError as e:
    log.info("Read SQS:ParamValidationError device_id %s:  ", device_id)
    log.info('Read SQS:ParamValidationError  Error in que SQS %s:  ' % e)

  except NameError as e:
    log.info("Read SQS:NameError device_id %s:  ", device_id)
    log.info('Read SQS:NameError  Error in que SQS %s:  ' % e)    
    
  except:
    e = sys.exc_info()[0]
    log.info("Send SQS:device_id %s:  ", device_id)
    log.info('Send SQS: Error in que SQS %s:  ' % e)

    log.warn(e)
    return []



def process_queue(config):  
  #queue = boto.connect_sqs().lookup(os.environ['SQS_QUEUE'])
  queue_url = environ.get('SQS_QUEUE_URL'),
  num_receive = int(os.environ.get('NUM_MESSAGES', 10))
  
  if debug_all: log.info('sqs_poller start process_queue %s: ', num_receive)
  # get redis que info
  #if debug_all: log.info('s3_poller jobs in queue %s: ', len(q))

  # create the partial that parses messages using proc function
  # and if it can't  - returns them to the SQS queue or deletes them if we tried
  # too many times
  handle = partial(best_effort, proc)
  with env(**dict(queue=queue_url, **config)):

    #infinate loop
    while True:
      count = 0

      try:

        #get messages from SQS queue and try to process them with the PROC function
        for message in get_messages(queue_url, num_receive):
          if debug_all: log.info('sqs_poller process_queue %s: ', num_receive)
          #try to get messages from the SQS queue and parse them
          transaction(handle,  message)
          count += 1

        if count == 0:
          # if we had messages process right away, else
          if debug_all: log.info('sqs_poller process_queue sleeping: ')
          sleep(1)
          
      except Exception as e:
        #if debug_all: log.info('s3_poller: process_queue errror' % e)
        log.info('sqs_poller: process_queue errror' % e)

      #end of while loop
        
  if debug_all: log.info('sqs_poller: exiting process_queue')


def interval(delay, method, *args, **kw):
  """
  Repeatedly call the same function.
  """

  while True:
    try:
      method(*args, **kw)
    except:
      log.exception("Error invoking %s", method)
      if debug_all: log.info('sqs_poller: Error invoking method%s', method)
      
    gevent.sleep(delay)


# trys to get a pushsmart message from the SQS que
def transaction(func, sqs_message):
  """Delete message if no errors."""
  #if debug_all: log.info('s3_poller: transaction %s', sqs_message.get_body())
  try:
    func(sqs_message.get_body())
    sqs_message.delete()
               
  except Exception as e:
    if debug_all: log.info('sqs_poller: transaction errror' % e)

# tries to get pushsmart messages
# and if there is a problem will retry several times (3)?
# times before deleting them from the queue
def best_effort(func, pushsmart_message):
  #if debug_all: log.info('s3_poller:best_effort starting')
  message = json.loads(pushsmart_message)
  try:
    func(message)
  except  Exception as e:
    if debug_all: log.info('sqs_poller:best_effort error ' % e)
    
    retry_count = message.get('retries', 0) + 1
    if retry_count > env.max_retries:
      log.exception('Discarding due to errors: %s', pushsmart_message)
      if debug_all: log.info('sqs_poller:best_effort Discarding')
      
    else:
      log.exception('Retrying')
      if debug_all: log.info('sqs_poller:best_effort retrying')
      
      retry = message.copy()
      retry['retries'] = retry_count
      
      retry['errors'] = retry.get('errors', [])
      retry['errors'].append(str(e))

      env.queue.write(
        env.queue.new_message(json.dumps(retry))
      )
  

if __name__ == "__main__":
  #num_requests = int(os.environ.get('NUM_REQUESTS',1))
  num_requests =1
  

  db_pool = ConnectionPool(os.environ.get('DATABASE_URL'))
  
  """
  conn = db_pool.getconn()
  fact_info = ensure_database(conn, SCHEMA)
  db_pool.putconn(conn, close=True)  
  """
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