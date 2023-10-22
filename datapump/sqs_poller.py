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


import gevent, gevent.monkey
import requests


import logging
# *******************************************************************
# Debug Output defines
# Comment to enable/disable
# ********************************************************************
#debug_all = False
debug_all = True


import botocore
import boto3
# Get the service resource
#sqs = boto3.resource('sqs')
#s3 = boto3.resource(service_name='sqs', region_name='REGION_NAME')

sqs_queue = boto3.client('sqs', region_name='us-east-1', aws_access_key_id=environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY'))

#queue_url = 'SQS_QUEUE_URL'
queue_url = 'https://sqs.us-east-1.amazonaws.com/291312677175/helmsmart-cloud'
#queue_url = 'https://sqs.us-east-1.amazonaws.com/291312677175/SeaSmart'




def process_queue(config):

  try:
    
    # read message from SQS queue
    response = sqs_queue.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        MessageAttributeNames=[  'All'  ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    

    #print(response['Messages'][0])

    log.info("Read SQS:device_id %s:  response %s: ", device_id,response['Messages'][0])

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

  

if __name__ == "__main__":
  #num_requests = int(os.environ.get('NUM_REQUESTS',1))
  num_requests =1
  

  db_pool = ConnectionPool(os.environ.get('DATABASE_URL'))
  
  conn = db_pool.getconn()
  fact_info = ensure_database(conn, SCHEMA)
  db_pool.putconn(conn, close=True)  

  config = dict(
    device_group = os.environ['DEVICE_GROUP'],
    db_pool = db_pool ,
    s3_bucket = bucket(),
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
