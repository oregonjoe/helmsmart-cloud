import os
from os import environ
from os import environ as env, path
#import pylibmc  
import sys
import re
import requests
from requests.exceptions import HTTPError
import json
import logging
import datetime
import time
import pytz
from time import mktime
from operator import itemgetter
from itertools import groupby
#from m2x.client import M2XClient
#from geopy.distance import vincenty
from array import *
from astral import *

from alert_processor import process_emailalert

# *******************************************************************
# Debug Output defines
# Comment to enable/disable
# ********************************************************************
debug_all = False
debug_info = True
debug_all = True


requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.INFO)

logging.basicConfig(level=logging.INFO)
log = logging


#import sendgrid
#from sendgrid.helpers.mail import *
#from sendgrid.helpers.mail import Mail, Email, Content

import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# read MailerToGo env vars
mailertogo_host     = os.environ.get('MAILERTOGO_SMTP_HOST')
mailertogo_port     = os.environ.get('MAILERTOGO_SMTP_PORT', 587)
mailertogo_user     = os.environ.get('MAILERTOGO_SMTP_USER')
mailertogo_password = os.environ.get('MAILERTOGO_SMTP_PASSWORD')
mailertogo_domain   = os.environ.get('MAILERTOGO_DOMAIN', "mydomain.com")


from twilio.rest import Client as smsClient


from sync import (
  dump_pcdinfirebase, dump_json, insert_influxdb_cloud, ensure_database,PARTITION, URL
)


from influxdb.influxdb08 import InfluxDBClient

from influxdb import InfluxDBClient as InfluxDBCloud
from influxdb.client import InfluxDBClientError

import psycopg
from psycopg_pool import ConnectionPool
#db_pool = ThreadedConnectionPool( 1,  **connection_from(os.environ['DATABASE_URL']))
#db_pool = ConnectionPool( 1,  **connection_from(os.environ['DATABASE_URL']))
db_pool = ConnectionPool(os.environ.get('DATABASE_URL'))
#db_pool = ConnectionPool(os.environ.get('HEROKU_POSTGRESQL_MAUVE_URL'))

#import botocore
#import boto3
# Get the service resource
#sqs = boto3.resource('sqs')
#s3 = boto3.resource(service_name='sqs', region_name='REGION_NAME')

#sqs_queue = boto3.client('sqs', region_name='us-east-1', aws_access_key_id=environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY'))

#queue_url = 'SQS_QUEUE_URL'
#queue_url = 'https://sqs.us-east-1.amazonaws.com/291312677175/helmsmart-cloud'
#queue_url = os.environ.get('SQS_QUEUE_ALERTS_URL')


class DateEncoder(json.JSONEncoder):
  def default(self, obj):
    if hasattr(obj, 'isoformat'):
      return obj.isoformat()
    else:
      return str(obj)



# ****************************************************************
# converts database standard sensor units to specified units
# *************************************************************************
def convertunits(value, units):
  units = int(units)

  # opps.. problem here as the value=0 also means its not=true so we cant dot this bucause 0 would return "---"
  #if not value:
  # return "---"
  if not isinstance(value, (int, float)):  # it is an integer or a float
    return "---"
  
  if value is None:
    return "---"

  if value == 'None':
    return "---"

  if units == 0: #//="0">Fahrenheit</option>
      return float("{0:.2f}".format((value * 1.8) - 459) )


  elif units ==  1: #//="1">Celsius</option>
      return float("{0:.2f}".format((value * 1.0) - 273) )


  elif units == 2: #//e="2">Kelvin</option>
      return value 


  #//  case 3: //="3">- - -</option> 


  elif units == 4: #//="4">Knots</option>
      return float("{0:.2f}".format(value * 1.94384449))


  elif units == 5: #//="5">MPH</option>
      return float("{0:.2f}".format(value * 2.23694) )


  elif units == 6: #//e="6">KPH</option>
      return float("{0:.2f}".format(value * 1.0) )



  #// case 7: //="7">- - -</option>
  elif units == 8: #//="8">PSI</option>
      return float("{0:.2f}".format(value * 0.145037738007) )



  elif units == 9: #//e="9">KPASCAL</option>
      return float("{0:.2f}".format(value * 1.0))



  elif units == 10: #//="10">INHG</option>
      return float("{0:.2f}".format(value * 0.295229) )


  #//  case 11: //="11">- - -</option>
  # //  case 12: //="12">TRUE</option>
  #//   case 13: //="13">MAGNETIC</option>
  #//   case 14: //="14">- - -</option>
  #//   case 15: //="15">- - -</option>
  elif units == 16:            #//   case 16: //="16">DEGREES</option>
    return float("{0:.6f}".format(value * 1.0 ) )
  
  elif units == 17:            #//   case 17: //="17">Radians</option>
    return float("{0:.6f}".format(value * 0.0174533 ) )
  
  
  elif units == 18: #//="18">Gallons/hs</option>
      return float("{0:.2f}".format(value * 0.264172052 ) )


  elif units == 19: #//="19">Liters/hr</option>
      return float("{0:.2f}".format(value * 1.0 ) )


  elif units == 20:# //="20">Liters</option>
       return float("{0:.2f}".format(value * 0.1 ) )
      
  elif units == 21:# //="21">Gallons</option>
      return float("{0:.2f}".format(value * 0.264172052 ) )
    
  #case 22: //="22">CubicMeter</option>
  #case 23: //="23">- - -</option>
  #case 24: //="24">RPM</option>
  #case 25: //="25">RPS</option>   
  #case 26: //="26">%</option>
  elif units == 27: #//="27">Volts</option>
      return float("{0:.2f}".format(value *1.00))


  elif units == 31: #//="31">kWhrs</option>
      return float("{0:.2f}".format(value *1.00))
  # case 28: //="28">Amps</option>
  
  elif units == 32: #//="32">Feet</option>
      return float("{0:.2f}".format(value * 3.28084)) 

  elif units == 33: #//="33">Meters</option>
      return float("{0:.2f}".format(value * 1.0))


  elif units == 44: #//= RAIN IN mm
       return float("{0:.2f}".format(value * 1000.0))  

  elif units == 45: #//=RAIN in inches
      return float("{0:.2f}".format(value * 39.3))
    

  elif units == 34: #//="34">Miles</option>
      return float("{0:.2f}".format(value * 0.000621371))              

  elif units == 35: #//="35">Nautical Mile</option>
      return float("{0:.2f}".format(value * 0.0005399568))                
  
  elif units == 36: #//="36">Fathoms</option>
      return float("{0:.2f}".format(value * 0.546806649))


  elif units == 37: #//="37">Time</option>
      #if debug_all: log.info('HeartBeat time %s:', datetime.datetime.fromtimestamp(int(value)).strftime('%H:%M:%S'))
      return (datetime.datetime.fromtimestamp(int(value)).strftime('%H:%M:%S'))

  elif units == 38: #//="38">Date/time</option>
      #if debug_all: log.info('HeartBeat time %s:', datetime.datetime.fromtimestamp(int(value)).strftime('%m/%d/%Y %H:%M:%S'))
      return (datetime.datetime.fromtimestamp(int(value)).strftime('%m/%d/%Y %H:%M:%S'))
    
  elif units == 39: #//="39">Hours</option>
    #Engine Hours (value / (60*60))
    return float("{0:.2f}".format(value * 0.000277777))

  elif units == 43: #//="43">Volts 10</option>
    return float("{0:.2f}".format(value * 0.1))

  else:
      return float("{0:.2f}".format(value * 1.0))

    
# ****************************************************************
# Gets the start and end times based on the interval
# *************************************************************************
def getepochtimes(Interval):



    if debug_all: log.info('messagepost:  getepochtimes Interval %s:  ', Interval)

    epochtimes=[]
    starttime = 0

    
    try:
        # if 0 then use current time 
        if starttime == 0:
            nowtime = datetime.datetime.now()
            endepoch =  int(time.time())

            if Interval== "1min":
                resolution = 60
                startepoch = endepoch - (resolution * 2)
                oldtime = datetime.datetime.now() - datetime.timedelta(minutes=2)
            elif Interval == "2min":
                resolution = 60*2
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(minutes=3)                
            elif Interval == "5min":
                resolution = 60*5
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(minutes=5)
            elif Interval== "10min":
                resolution = 60*10
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(minutes=10)
            elif Interval == "15min":
                resolution = 60*15
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(minutes=15)
            elif Interval== "30min":
                resolution = 60*30
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(minutes=30)
            elif Interval== "1hour":
                resolution = 60*60
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(hours=1)
                
            elif Interval == "2hour":
                resolution = 60*60*2
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(hours=2)

                
            elif Interval == "3hour":
                resolution = 60*60*3
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(hours=3)                
                
            elif Interval == "4hour":
                resolution = 60*60*4
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(hours=4)

                
            elif Interval == "6hour":
                resolution = 60*60*6
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(hours=6)
            elif Interval == "8hour":
                resolution = 60*60*8
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(hours=8)
            elif Interval == "12hour":
                resolution = 60*60*12
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(hours=12)
            elif Interval == "1day":
                resolution = 60*60*24
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(days=1)
            elif Interval == "2day":
                resolution = 60*60*24*2
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(days=2)                
            elif Interval== "7day":
                resolution = 60*60*24*7
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(days=7)
            elif Interval == "1month":
                resolution = 60*60*24*30
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(months=1)
            else:
                resolution = 60
                startepoch = endepoch - (resolution * 1)
                oldtime = datetime.datetime.now() - datetime.timedelta(minutes=2)

                
        epochtimes.append(startepoch)
        epochtimes.append(endepoch)
        epochtimes.append(resolution)

    except TypeError as e:
        if debug_all: log.info('messagepost: TypeError in geting getepochtimes parameters %s:  ', Interval)
        if debug_all: log.info('messagepost: TypeError in geting getepochtimes parameters %s:  ' % str(e))
            
    except KeyError as e:
        if debug_all: log.info('messagepost: KeyError in geting getepochtimes parameters %s:  ', Interval)
        if debug_all: log.info('messagepost: KeyError in geting getepochtimes parameters %s:  ' % str(e))

    except NameError as e:
        if debug_all: log.info('messagepost: NameError in geting getepochtimes parameters %s:  ', Interval)
        if debug_all: log.info('messagepost: NameError in geting getepochtimes parameters %s:  ' % str(e))
            
    except IndexError as e:
        if debug_all: log.info('messagepost: IndexError in geting getepochtimes parameters %s:  ', Interval)
        if debug_all: log.info('messagepost: IndexError in geting getepochtimes parameters %s:  ' % str(e))  


    except:
        if debug_all: log.info('messagepost: Error in geting  getepochtimes %s:  ', Interval)
        e = sys.exc_info()[0]
        if debug_all: log.info('messagepost: Error in geting getepochtimes parameters %s:  ' % str(e))

    return(epochtimes)

def getSwitchIndex(eventtype):
    
    switchdata = {}
    if debug_all: log.info('getSwitchIndex: eventtype %s  ', eventtype)
    
    try:
        if eventtype == "/M2M/Switch/Value 0 Port":	
            switchInstance=0
            switchIndex=0
            

        elif eventtype == "/M2M/Switch/Value 1 Port":	
            switchInstance=0
            switchIndex=1


        elif eventtype == "/M2M/Switch/Value 2 Port":	
            switchInstance=0
            switchIndex=2


        elif eventtype == "/M2M/Switch/Value 3 Port":	
            switchInstance=0
            switchIndex=3


        elif eventtype == "/M2M/Switch/Value 4 Port":	
            switchInstance=0
            switchIndex=4


        elif eventtype == "/M2M/Switch/Value 5 Port":	
            switchInstance=0
            switchIndex=5


        elif eventtype == "/M2M/Switch/Value 6 Port":	
            switchInstance=0
            switchIndex=6


        elif eventtype == "/M2M/Switch/Value 7 Port":	
            switchInstance=0
            switchIndex=7


        elif eventtype == "/M2M/Switch/Value 8 Port":	
            switchInstance=0
            switchIndex=8



        elif eventtype == "/M2M/Switch/Value 9 Port":	
            switchInstance=0
            switchIndex=9


        elif eventtype == "/M2M/Switch/Value 10 Port":	
            switchInstance=0
            switchIndex=10


        elif eventtype == "/M2M/Switch/Value 11 Port":	
            switchInstance=0
            switchIndex=11


        elif eventtype == "/M2M/Switch/Value 12 Port":	
            switchInstance=0
            switchIndex=12


        elif eventtype == "/M2M/Switch/Value 13 Port":	
            switchInstance=0
            switchIndex=13


        elif eventtype == "/M2M/Switch/Value 14 Port":	
            switchInstance=0
            switchIndex=14


        elif eventtype == "/M2M/Switch/Value 15 Port":	
            switchInstance=0
            switchIndex=15


        elif eventtype == "/M2M/Switch/Value 0 Starboard":	
            switchInstance=1
            switchIndex=0
            

        elif eventtype == "/M2M/Switch/Value 1 Starboard":	
            switchInstance=1
            switchIndex=1


        elif eventtype == "/M2M/Switch/Value 2 Starboard":	
            switchInstance=1
            switchIndex=2


        elif eventtype == "/M2M/Switch/Value 3 Starboard":	
            switchInstance=1
            switchIndex=3


        elif eventtype == "/M2M/Switch/Value 4 Starboard":	
            switchInstance=1
            switchIndex=4


        elif eventtype == "/M2M/Switch/Value 5 Starboard":	
            switchInstance=1
            switchIndex=5


        elif eventtype == "/M2M/Switch/Value 6 Starboard":	
            switchInstance=1
            switchIndex=6


        elif eventtype == "/M2M/Switch/Value 7 Starboard":	
            switchInstance=1
            switchIndex=7


        elif eventtype == "/M2M/Switch/Value 8 Starboard":	
            switchInstance=1
            switchIndex=8



        elif eventtype == "/M2M/Switch/Value 9 Starboard":	
            switchInstance=1
            switchIndex=9


        elif eventtype == "/M2M/Switch/Value 10 Starboard":	
            switchInstance=1
            switchIndex=10


        elif eventtype == "/M2M/Switch/Value 11 Starboard":	
            switchInstance=1
            switchIndex=11


        elif eventtype == "/M2M/Switch/Value 12 Starboard":	
            switchInstance=1
            switchIndex=12


        elif eventtype == "/M2M/Switch/Value 13 Starboard":	
            switchInstance=1
            switchIndex=13


        elif eventtype == "/M2M/Switch/Value 14 Starboard":	
            switchInstance=1
            switchIndex=14


        elif eventtype == "/M2M/Switch/Value 15 Starboard":	
            switchInstance=1
            switchIndex=15
                    

        elif eventtype == "/M2M/Switch/Value 0 Center":	
            switchInstance=2
            switchIndex=0
            

        elif eventtype == "/M2M/Switch/Value 1 Center":	
            switchInstance=2
            switchIndex=1


        elif eventtype == "/M2M/Switch/Value 2 Center":	
            switchInstance=2
            switchIndex=2


        elif eventtype == "/M2M/Switch/Value 3 Center":	
            switchInstance=2
            switchIndex=3


        elif eventtype == "/M2M/Switch/Value 4 Center":	
            switchInstance=2
            switchIndex=4


        elif eventtype == "/M2M/Switch/Value 5 Center":	
            switchInstance=2
            switchIndex=5


        elif eventtype == "/M2M/Switch/Value 6 Center":	
            switchInstance=2
            switchIndex=6


        elif eventtype == "/M2M/Switch/Value 7 Center":	
            switchInstance=2
            switchIndex=7


        elif eventtype == "/M2M/Switch/Value 8 Center":	
            switchInstance=2
            switchIndex=8


        elif eventtype == "/M2M/Switch/Value 9 Center":	
            switchInstance=2
            switchIndex=9


        elif eventtype == "/M2M/Switch/Value 10 Center":	
            switchInstance=2
            switchIndex=10


        elif eventtype == "/M2M/Switch/Value 11 Center":	
            switchInstance=2
            switchIndex=11


        elif eventtype == "/M2M/Switch/Value 12 Center":	
            switchInstance=2
            switchIndex=12


        elif eventtype == "/M2M/Switch/Value 13 Center":	
            switchInstance=2
            switchIndex=13


        elif eventtype == "/M2M/Switch/Value 14 Center":	
            switchInstance=2
            switchIndex=14


        elif eventtype == "/M2M/Switch/Value 15 Center":	
            switchInstance=2
            switchIndex=15


        switchdata['instance']=switchInstance
        switchdata['index']=switchIndex
        
        return switchdata

    except TypeError as e:
        if debug_all: log.info('messagepost: TypeError in getSwitchIndex %s:%s  ', eventtype, switchdata)
        if debug_all: log.info('messagepost: TypeError in getSwitchIndex %s:  ' % str(e))

    except ValueError as e:
        if debug_all: log.info('messagepost: ValueError in getSwitchIndex %s:%s  ', eventtype, switchdata)
        if debug_all: log.info('messagepost: TypeError in getSwitchIndex %s:  ' % str(e))

    except AttributeError as e:
        if debug_all: log.info('messagepost: AttributeError in getSwitchIndex %s:%s  ', eventtype, switchdata)
        if debug_all: log.info('messagepost: AttributeError in getSwitchIndex %s:  ' % str(e))        
        
    except KeyError as e:
        if debug_all: log.info('messagepost: KeyError in getSwitchIndex %s:%s  ', eventtype, switchdata)
        if debug_all: log.info('messagepost: KeyError in getSwitchIndex %s:  ' % str(e))

    except NameError as e:
        if debug_all: log.info('messagepost: NameError in getSwitchIndex %s:%s  ', eventtype, switchdata)
        if debug_all: log.info('messagepost: NameError in getSwitchIndex %s:  ' % str(e))     

    except:
        if debug_all: log.info('messagepost: Error in getSwitchIndex %s:%s  ', eventtype, switchdata)
        e = sys.exc_info()[0]

def getDimmerIndex(eventtype):
    
    dimmerdata = {}
    if debug_all: log.info('getDimmerIndex: eventtype %s  ', eventtype)
    
    try:
        if eventtype == "/M2M/LED Dimmer/Value 0 Zone 0":	
            switchInstance=0
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 1 Zone 0":	
            switchInstance=0
            switchIndex=1


        elif eventtype == "/M2M/LED Dimmer/Value 2 Zone 0":	
            switchInstance=0
            switchIndex=2


        elif eventtype == "/M2M/LED Dimmer/Value 3 Zone 0":	
            switchInstance=0
            switchIndex=3


        elif eventtype == "/M2M/LED Dimmer/Value 4 Zone 0":	
            switchInstance=0
            switchIndex=4





        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 1":	
            switchInstance=1
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 1 Zone 1":	
            switchInstance=1
            switchIndex=1


        elif eventtype == "/M2M/LED Dimmer/Value 2 Zone 1":	
            switchInstance=1
            switchIndex=2


        elif eventtype == "/M2M/LED Dimmer/Value 3 Zone 1":	
            switchInstance=1
            switchIndex=3


        elif eventtype == "/M2M/LED Dimmer/Value 4 Zone 1":	
            switchInstance=1
            switchIndex=4


 
                    

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 2":	
            switchInstance=2
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 1 Zone 2":	
            switchInstance=2
            switchIndex=1


        elif eventtype == "/M2M/LED Dimmer/Value 2 Zone 2":	
            switchInstance=2
            switchIndex=2


        elif eventtype == "/M2M/LED Dimmer/Value 3 Zone 2":	
            switchInstance=2
            switchIndex=3


        elif eventtype == "/M2M/LED Dimmer/Value 4 Zone 2":	
            switchInstance=2
            switchIndex=4


        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 3":	
            switchInstance=3
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 4":	
            switchInstance=4
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 5":	
            switchInstance=5
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 6":	
            switchInstance=6
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 7":	
            switchInstance=7
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 8":	
            switchInstance=8
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 9":	
            switchInstance=9
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 10":	
            switchInstance=10
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 11":	
            switchInstance=11
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 12":	
            switchInstance=12
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 13":	
            switchInstance=13
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 14":	
            switchInstance=14
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 15":	
            switchInstance=15
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 16":	
            switchInstance=16
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 17":	
            switchInstance=17
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 18":	
            switchInstance=18
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 19":	
            switchInstance=19
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 20":	
            switchInstance=20
            switchIndex=0

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 21":	
            switchInstance=21
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 22":	
            switchInstance=22
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 23":	
            switchInstance=23
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 24":	
            switchInstance=24
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 25":	
            switchInstance=25
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 26":	
            switchInstance=26
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 27":	
            switchInstance=27
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 28":	
            switchInstance=28
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 29":	
            switchInstance=29
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 30":	
            switchInstance=30
            switchIndex=0


        elif eventtype == "/M2M/LED Dimmer/Value 0 Zone 31":	
            switchInstance=31
            switchIndex=0


        elif eventtype == "/M2M/RGB Dimmer/Value 0 Zone 0":	
            switchInstance=128
            switchIndex=0
            

        elif eventtype == "/M2M/RGB Dimmer/Value 1 Zone 0":	
            switchInstance=128
            switchIndex=1


        elif eventtype == "/M2M/RGB Dimmer/Value 2 Zone 0":	
            switchInstance=128
            switchIndex=2


        elif eventtype == "/M2M/RGB Dimmer/Value 3 Zone 0":	
            switchInstance=128
            switchIndex=3


        elif eventtype == "/M2M/RGB Dimmer/Value 4 Zone 0":	
            switchInstance=128
            switchIndex=4





        elif eventtype == "/M2M/RGB Dimmer/Value 0 Zone 1":	
            switchInstance=129
            switchIndex=0
            

        elif eventtype == "/M2M/RGB Dimmer/Value 1 Zone 1":	
            switchInstance=129
            switchIndex=1


        elif eventtype == "/M2M/RGB Dimmer/Value 2 Zone 1":	
            switchInstance=129
            switchIndex=2


        elif eventtype == "/M2M/RGB Dimmer/Value 3 Zone 1":	
            switchInstance=129
            switchIndex=3


        elif eventtype == "/M2M/RGB Dimmer/Value 4 Zone 1":	
            switchInstance=129
            switchIndex=4


 
                    

        elif eventtype == "/M2M/RGB Dimmer/Value 0 Zone 2":	
            switchInstance=130
            switchIndex=0
            

        elif eventtype == "/M2M/RGB Dimmer/Value 1 Zone 2":	
            switchInstance=130
            switchIndex=1


        elif eventtype == "/M2M/RGB Dimmer/Value 2 Zone 2":	
            switchInstance=130
            switchIndex=2


        elif eventtype == "/M2M/RGB Dimmer/Value 3 Zone 2":	
            switchInstance=130
            switchIndex=3


        elif eventtype == "/M2M/RGB Dimmer/Value 4 Zone 2":	
            switchInstance=130
            switchIndex=4

                    

        elif eventtype == "/M2M/RGB Dimmer/Value 0 Zone 3":	
            switchInstance=131
            switchIndex=0
            

        elif eventtype == "/M2M/RGB Dimmer/Value 1 Zone 3":	
            switchInstance=131
            switchIndex=1


        elif eventtype == "/M2M/RGB Dimmer/Value 2 Zone 3":	
            switchInstance=131
            switchIndex=2


        elif eventtype == "/M2M/RGB Dimmer/Value 3 Zone 3":	
            switchInstance=131
            switchIndex=3


        elif eventtype == "/M2M/RGB Dimmer/Value 4 Zone 3":	
            switchInstance=131
            switchIndex=4

                    

        elif eventtype == "/M2M/RGB Dimmer/Value 0 Zone 4":	
            switchInstance=132
            switchIndex=0
            

        elif eventtype == "/M2M/RGB Dimmer/Value 1 Zone 4":	
            switchInstance=132
            switchIndex=1


        elif eventtype == "/M2M/RGB Dimmer/Value 2 Zone 4":	
            switchInstance=132
            switchIndex=2


        elif eventtype == "/M2M/RGB Dimmer/Value 3 Zone 4":	
            switchInstance=132
            switchIndex=3


        elif eventtype == "/M2M/RGB Dimmer/Value 4 Zone 4":	
            switchInstance=132
            switchIndex=4

                    

        elif eventtype == "/M2M/RGB Dimmer/Value 0 Zone 5":	
            switchInstance=133
            switchIndex=0
            

        elif eventtype == "/M2M/RGB Dimmer/Value 1 Zone 5":	
            switchInstance=133
            switchIndex=1


        elif eventtype == "/M2M/RGB Dimmer/Value 2 Zone 5":	
            switchInstance=133
            switchIndex=2


        elif eventtype == "/M2M/RGB Dimmer/Value 3 Zone 5":	
            switchInstance=133
            switchIndex=3


        elif eventtype == "/M2M/RGB Dimmer/Value 4 Zone 5":	
            switchInstance=133
            switchIndex=4

                    

        elif eventtype == "/M2M/RGB Dimmer/Value 0 Zone 6":	
            switchInstance=134
            switchIndex=0
            

        elif eventtype == "/M2M/RGB Dimmer/Value 1 Zone 6":	
            switchInstance=134
            switchIndex=1


        elif eventtype == "/M2M/RGB Dimmer/Value 2 Zone 6":	
            switchInstance=134
            switchIndex=2


        elif eventtype == "/M2M/RGB Dimmer/Value 3 Zone 6":	
            switchInstance=134
            switchIndex=3


        elif eventtype == "/M2M/RGB Dimmer/Value 4 Zone 6":	
            switchInstance=134
            switchIndex=4

                    

        elif eventtype == "/M2M/RGB Dimmer/Value 0 Zone 7":	
            switchInstance=135
            switchIndex=0
            

        elif eventtype == "/M2M/RGB Dimmer/Value 1 Zone 7":	
            switchInstance=135
            switchIndex=1


        elif eventtype == "/M2M/RGB Dimmer/Value 2 Zone 7":	
            switchInstance=135
            switchIndex=2


        elif eventtype == "/M2M/RGB Dimmer/Value 3 Zone 7":	
            switchInstance=135
            switchIndex=3


        elif eventtype == "/M2M/RGB Dimmer/Value 4 Zone 7":	
            switchInstance=135
            switchIndex=4


                    

        elif eventtype == "/M2M/RGB Dimmer/Value 0 Zone 8":	
            switchInstance=136
            switchIndex=0
            

        elif eventtype == "/M2M/RGB Dimmer/Value 1 Zone 8":	
            switchInstance=136
            switchIndex=1


        elif eventtype == "/M2M/RGB Dimmer/Value 2 Zone 8":	
            switchInstance=136
            switchIndex=2


        elif eventtype == "/M2M/RGB Dimmer/Value 3 Zone 8":	
            switchInstance=136
            switchIndex=3


        elif eventtype == "/M2M/RGB Dimmer/Value 4 Zone 8":	
            switchInstance=136
            switchIndex=4

        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 0 Zone 0":	
            switchInstance=192
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 1 Zone 0":	
            switchInstance=192
            switchIndex=1


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 2 Zone 0":	
            switchInstance=192
            switchIndex=2


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 3 Zone 0":	
            switchInstance=192
            switchIndex=3


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 4 Zone 0":	
            switchInstance=192
            switchIndex=4





        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 0 Zone 1":	
            switchInstance=193
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 1 Zone 1":	
            switchInstance=193
            switchIndex=1


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 2 Zone 1":	
            switchInstance=193
            switchIndex=2


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 3 Zone 1":	
            switchInstance=193
            switchIndex=3


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 4 Zone 1":	
            switchInstance=193
            switchIndex=4





        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 0 Zone 2":	
            switchInstance=194
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 1 Zone 2":	
            switchInstance=194
            switchIndex=1


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 2 Zone 2":	
            switchInstance=194
            switchIndex=2


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 3 Zone 2":	
            switchInstance=194
            switchIndex=3


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 4 Zone 2":	
            switchInstance=194
            switchIndex=4




        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 0 Zone 3":	
            switchInstance=194
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 1 Zone 3":	
            switchInstance=194
            switchIndex=1


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 2 Zone 3":	
            switchInstance=194
            switchIndex=2


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 3 Zone 3":	
            switchInstance=194
            switchIndex=3


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 4 Zone 3":	
            switchInstance=194
            switchIndex=4




        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 0 Zone 4":	
            switchInstance=195
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 1 Zone 4":	
            switchInstance=195
            switchIndex=1


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 2 Zone 41":	
            switchInstance=195
            switchIndex=2


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 3 Zone 4":	
            switchInstance=195
            switchIndex=3


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 4 Zone 4":	
            switchInstance=195
            switchIndex=4




        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 0 Zone 15":	
            switchInstance=196
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 1 Zone 5":	
            switchInstance=1963
            switchIndex=1


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 2 Zone 5":	
            switchInstance=196
            switchIndex=2


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 3 Zone 5":	
            switchInstance=196
            switchIndex=3


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 4 Zone 5":	
            switchInstance=196
            switchIndex=4




        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 0 Zone 6":	
            switchInstance=197
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 1 Zone 6":	
            switchInstance=197
            switchIndex=1


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 2 Zone 6":	
            switchInstance=197
            switchIndex=2


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 3 Zone 6":	
            switchInstance=197
            switchIndex=3


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 4 Zone 6":	
            switchInstance=197
            switchIndex=4




        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 0 Zone 7":	
            switchInstance=198
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 1 Zone 7":	
            switchInstance=198
            switchIndex=1


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 2 Zone 7":	
            switchInstance=198
            switchIndex=2


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 3 Zone 7":	
            switchInstance=198
            switchIndex=3


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 4 Zone 7":	
            switchInstance=198
            switchIndex=4




        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 0 Zone 8":	
            switchInstance=199
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 1 Zone 8":	
            switchInstance=199
            switchIndex=1


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 2 Zone 8":	
            switchInstance=199
            switchIndex=2


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 3 Zone 8":	
            switchInstance=199
            switchIndex=3


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 4 Zone 8":	
            switchInstance=199
            switchIndex=4




        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 0 Zone 9":	
            switchInstance=200
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 1 Zone 9":	
            switchInstance=200
            switchIndex=1


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 2 Zone 9":	
            switchInstance=200
            switchIndex=2


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 3 Zone 9":	
            switchInstance=200
            switchIndex=3


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 4 Zone 9":	
            switchInstance=200
            switchIndex=4




        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 0 Zone 10":	
            switchInstance=201
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 1 Zone 10":	
            switchInstance=201
            switchIndex=1


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 2 Zone 10":	
            switchInstance=201
            switchIndex=2


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 3 Zone 10":	
            switchInstance=201
            switchIndex=3


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 4 Zone 10":	
            switchInstance=201
            switchIndex=4




        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 0 Zone 11":	
            switchInstance=202
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 1 Zone 11":	
            switchInstance=202
            switchIndex=1


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 2 Zone 11":	
            switchInstance=202
            switchIndex=2


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 3 Zone 11":	
            switchInstance=202
            switchIndex=3


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 4 Zone 11":	
            switchInstance=202
            switchIndex=4




        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 0 Zone 12":	
            switchInstance=203
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 1 Zone 12":	
            switchInstance=203
            switchIndex=1


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 2 Zone 12":	
            switchInstance=203
            switchIndex=2


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 3 Zone 12":	
            switchInstance=203
            switchIndex=3


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 4 Zone 12":	
            switchInstance=203
            switchIndex=4




        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 0 Zone 13":	
            switchInstance=204
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 1 Zone 13":	
            switchInstance=204
            switchIndex=1


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 2 Zone 13":	
            switchInstance=204
            switchIndex=2


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 3 Zone 13":	
            switchInstance=204
            switchIndex=3


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 4 Zone 13":	
            switchInstance=204
            switchIndex=4




        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 0 Zone 14":	
            switchInstance=205
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 1 Zone 14":	
            switchInstance=205
            switchIndex=1


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 2 Zone 14":	
            switchInstance=205
            switchIndex=2


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 3 Zone 14":	
            switchInstance=205
            switchIndex=3


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 4 Zone 14":	
            switchInstance=205
            switchIndex=4




        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 0 Zone 15":	
            switchInstance=206
            switchIndex=0
            

        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 1 Zone 15":	
            switchInstance=206
            switchIndex=1


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 2 Zone 15":	
            switchInstance=206
            switchIndex=2


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 3 Zone 15":	
            switchInstance=206
            switchIndex=3


        elif eventtype == "/M2M/LED Dimmer 4 Channel/Value 4 Zone 15":	
            switchInstance=206
            switchIndex=4

  

        dimmerdata['instance']=switchInstance
        dimmerdata['index']=switchIndex
        
        return dimmerdata

    except TypeError as e:
        if debug_all: log.info('messagepost: TypeError in getDimmerIndex %s:%s  ', eventtype, dimmerdata)
        if debug_all: log.info('messagepost: TypeError in getDimmerIndex %s:  ' % str(e))

    except ValueError as e:
        if debug_all: log.info('messagepost: ValueError in getDimmerIndex %s:%s  ', eventtype, dimmerdata)
        if debug_all: log.info('messagepost: TypeError in getDimmerIndex %s:  ' % str(e))

    except AttributeError as e:
        if debug_all: log.info('messagepost: AttributeError in getDimmerIndex %s:%s  ', eventtype, dimmerdata)
        if debug_all: log.info('messagepost: AttributeError in getDimmerIndex %s:  ' % str(e))        
        
    except KeyError as e:
        if debug_all: log.info('messagepost: KeyError in getDimmerIndex %s:%s  ', eventtype, dimmerdata)
        if debug_all: log.info('messagepost: KeyError in getDimmerIndex %s:  ' % str(e))

    except NameError as e:
        if debug_all: log.info('messagepost: NameError in getDimmerIndex %s:%s  ', eventtype, dimmerdata)
        if debug_all: log.info('messagepost: NameError in getDimmerIndex %s:  ' % str(e))     

    except:
        if debug_all: log.info('messagepost: Error in getDimmerIndex %s:%s  ', eventtype, dimmerdata)
        e = sys.exc_info()[0]


def make_HSAlert_json(series_number, parameters, distance, value, alarmstatus):

        series_parameters={}

        series_parameters = parameters.get('series_1',"")
        
        try:
            
            #if not value :
            #    print 'make_tempodb_json: no value to update'
            #    #if debug_all: log.info('Telemetry:make_HSAlert_json  : no value to update' )
            #    return series_parameters


            if value == "":
                series_parameters["title"]= series_parameters['title']
                series_parameters["interval"]= parameters['Interval']
                series_parameters["alarmtype"]= series_parameters['alarmtype']
                series_parameters["alarmmode"]= series_parameters['alarmmode']
                series_parameters["alarmlow"]= series_parameters['alarmlow']
                series_parameters["alarmhigh"]= series_parameters['alarmhigh']
                series_parameters["units"]= series_parameters['units']
                series_parameters["alarmstatus"]= alarmstatus
                series_parameters["value"]= "missing"
                


            else:
                series_parameters["title"]= series_parameters['title']
                series_parameters["interval"]= parameters['Interval']
                series_parameters["alarmtype"]= series_parameters['alarmtype']
                series_parameters["alarmmode"]= series_parameters['alarmmode']
                series_parameters["alarmlow"]= series_parameters['alarmlow']
                series_parameters["alarmhigh"]= series_parameters['alarmhigh']
                series_parameters["units"]= series_parameters['units']
                series_parameters["alarmstatus"]= alarmstatus
                series_parameters["distance"]= distance
                series_parameters["value"]= value


        except TypeError as e:
            if debug_all: log.info('make_HSAlert_json: TypeError in  %s:  ' % str(e))
            
        except KeyError as e:
            if debug_all: log.info('make_HSAlert_json: KeyError in  %s:  ' % str(e))

        except NameError as e:
            if debug_all: log.info('make_HSAlert_json: NameError in  %s:  ' % str(e))

        except IndexError as e:
            if debug_all: log.info('make_HSAlert_json: IndexError in  %s:  ' % str(e))          

        except:
            if debug_all: log.info("make_HSAlert_json: Error: %s" % e)
            
            
        #if debug_all: log.info('Telemetry:make_HSAlert_jsonseries_parameters %s',series_parameters )
        return series_parameters


# ****************************************************************
# InfluxDB Sensor key
# takes alert message sensor key and returns the sensor values
# *************************************************************************
def getSensorParameter(sensorKey):

    #select  median(temperature) AS temperature

        
    try:
        
        if sensorKey.find(".*.") > 0:  
            sensorKey = sensorKey.replace(".*.","*.")
        
        seriesname = sensorKey
        seriestags = seriesname.split(".")
        if debug_all: log.info('getSensorParameter: seriestags %s:  ', seriestags)

        seriesparametertag = seriestags[5]
        if debug_all: log.info('getSensorParameter: seriesparametertag %s:  ', seriesparametertag)
        
        seriesparameter = seriesparametertag.split(":")    
        parameter = seriesparameter[1]
        if debug_all: log.info('getSensorParameter: parameter %s:  ', parameter)
        
        parameterKey = ('median({}) AS {}').format( parameter,  parameter)
    
        return parameterKey

    except TypeError as e:
        if debug_all: log.info('getSensorParameter: TypeError in convertInfluxDBCloudKeys %s:  ', sensorKey)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getSensorParameter: TypeError in convertInfluxDBCloudKeys %s:  ' % str(e))
        
    except KeyError as e:
        if debug_all: log.info('getSensorParameter: KeyError in convertInfluxDBCloudKeys %s:  ', sensorKey)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getSensorParameter: KeyError in convertInfluxDBCloudKeys %s:  ' % str(e))

    except NameError as e:
        if debug_all: log.info('getSensorParameter: NameError in convertInfluxDBCloudKeys %s:  ', sensorKey)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getSensorParameter: NameError in convertInfluxDBCloudKeys %s:  ' % str(e))

    except IndexError as e:
        if debug_all: log.info('getSensorParameter: IndexError in convertInfluxDBCloudKeys %s:  ', sensorKey)
        #e = sys.exc_info()[0]

        if debug_all: log.info('getSensorParameter: IndexError in convertInfluxDBCloudKeys %s:  ' % str(e))          

    except:
        if debug_all: log.info('getSensorParameter: Error in convertInfluxDBCloudKeys %s:  ', sensorKey)
        e = sys.exc_info()[0]
        if debug_all: log.info("getSensorParameter: Error: %s" % e)

# ****************************************************************
# takes alert message sensor key and returns the selected value
# *************************************************************************
def getSensorTag(sensorKey, index):

    try:
        
        if sensorKey.find(".*.") > 0:  
            sensorKey = sensorKey.replace(".*.","*.")
        
        seriesname = sensorKey
        seriestags = seriesname.split(".")
        if debug_all: log.info('getSensorTag: seriestags %s:  ', seriestags)

        seriesparametertag = seriestags[index]
        if debug_all: log.info('getSensorTag: seriesparametertag %s:  ', seriesparametertag)
        
        seriesparameter = seriesparametertag.split(":")    
        sensorTag = seriesparameter[1]
        if debug_all: log.info('getSensorTag: sensorTag %s:  ', sensorTag)
    
        return sensorTag


    except:
        e = sys.exc_info()[0]
        if debug_all: log.info("getSensorTag: Error: %s" % e)
        return ""



# ****************************************************************
# InfluxDB Sensor key
# takes alert message sensor key and returns the sensor values
# *************************************************************************
def createInfluxDBCloudKeys(sensorKey):

    # example key 'key': 'deviceid:68271933E95E.sensor:seasmartdimmer.source:.*.instance:0.type:LED 1 Channel.parameter:value0.HelmSmart'

    if sensorKey.find(".*.") > 0:  
        sensorKey = sensorKey.replace(".*.","*.")
        #SERIES_KEY.replace("*.","??")
        #SERIES_KEY.replace(".",".")
        #if debug_all: log.info('convertInfluxDBCloudKeys: Error in convertInfluxDBCloudKeys %s:  ', SERIES_KEY)
                
    try:
        #if debug_all: log.info('convertInfluxDBCloudKeys: SERIES_KEY %s:  ', SERIES_KEY)
        seriesname = sensorKey
        seriestags = seriesname.split(".")

        #if debug_all: log.info('convertInfluxDBCloudKeys: seriestags %s:  ', seriestags)

        seriesdeviceidtag = seriestags[0]
        seriesdeviceid = seriesdeviceidtag.split(":")

        seriessensortag = seriestags[1]
        seriessensor = seriessensortag.split(":")

        seriessourcetag = seriestags[2]
        seriessource = seriessourcetag.split(":")

        seriesinstancetag = seriestags[3]
        seriesinstance = seriesinstancetag.split(":")

        seriestypetag = seriestags[4]
        seriestype = seriestypetag.split(":")

        seriesparametertag = seriestags[5]
        seriesparameter = seriesparametertag.split(":")    
        parameter = seriesparameter[1]

        
        if parameter == 'latlng':
            serieskeys="( deviceid='"
            serieskeys= serieskeys + seriesdeviceid[1] 
            serieskeys= serieskeys +  "' AND sensor='" +  seriessensor[1]
            if seriessource[1] != "*":
                serieskeys= serieskeys +  "' AND source='" +  seriessource[1] 
            serieskeys= serieskeys +  "' AND instance='" +  seriesinstance[1] 
            serieskeys= serieskeys +  "' AND type='" +  seriestype[1] 
            serieskeys= serieskeys +  "' AND parameter='lat') OR " 

            serieskeys=serieskeys + "( deviceid='"
            serieskeys= serieskeys + seriesdeviceid[1] 
            serieskeys= serieskeys +  "' AND sensor='" +  seriessensor[1]
            if seriessource[1] != "*":
                serieskeys= serieskeys +  "' AND source='" +  seriessource[1] 
            serieskeys= serieskeys +  "' AND instance='" +  seriesinstance[1] 
            serieskeys= serieskeys +  "' AND type='" +  seriestype[1] 
            serieskeys= serieskeys +  "' AND parameter='lng') "  

                
        else:
            serieskeys="( deviceid='"
            serieskeys= serieskeys + seriesdeviceid[1] 
            serieskeys= serieskeys +  "' AND sensor='" +  seriessensor[1]
            if seriessource[1] != "*":
                serieskeys= serieskeys +  "' AND source='" +  seriessource[1] 
            serieskeys= serieskeys +  "' AND instance='" +  seriesinstance[1] 
            serieskeys= serieskeys +  "' AND type='" +  seriestype[1] 
            serieskeys= serieskeys +  "' AND parameter='" +  seriesparameter[1] + "'   )"


        return serieskeys


    except TypeError as e:
        if debug_all: log.info('createInfluxDBCloudKeys: TypeError in convertInfluxDBCloudKeys %s:  ', sensorKey)
        #e = sys.exc_info()[0]

        if debug_all: log.info('createInfluxDBCloudKeys: TypeError in convertInfluxDBCloudKeys %s:  ' % str(e))
        
    except KeyError as e:
        if debug_all: log.info('createInfluxDBCloudKeys: KeyError in convertInfluxDBCloudKeys %s:  ', sensorKey)
        #e = sys.exc_info()[0]

        if debug_all: log.info('createInfluxDBCloudKeys: KeyError in convertInfluxDBCloudKeys %s:  ' % str(e))

    except NameError as e:
        if debug_all: log.info('createInfluxDBCloudKeys: NameError in convertInfluxDBCloudKeys %s:  ', sensorKey)
        #e = sys.exc_info()[0]

        if debug_all: log.info('createInfluxDBCloudKeys: NameError in convertInfluxDBCloudKeys %s:  ' % str(e))

    except IndexError as e:
        if debug_all: log.info('createInfluxDBCloudKeys: IndexError in convertInfluxDBCloudKeys %s:  ', sensorKey)
        #e = sys.exc_info()[0]

        if debug_all: log.info('createInfluxDBCloudKeys: IndexError in convertInfluxDBCloudKeys %s:  ' % str(e))          

    except:
        if debug_all: log.info('createInfluxDBCloudKeys: Error in convertInfluxDBCloudKeys %s:  ', sensorKey)
        e = sys.exc_info()[0]
        if debug_all: log.info("createInfluxDBCloudKeys: Error: %s" % e)




# ****************************************************************
# InfluxDB Sensor query
# takes alert message sensor key and returns the sensor values
# *************************************************************************
def getSensorValues(alertParameters):

    dchost = 'hilldale-670d9ee3.influxcloud.net' 
    dcport = 8086
    dcusername = 'helmsmart'
    dcpassword = 'Salm0n16'
    dcdatabase = 'pushsmart-cloud'

    sensorSeries = alertParameters.get('series_1',"")

    if sensorSeries == "":
        return None

    sensorValues=[]
    sensorKey = sensorSeries['key']
    sensorUnits = sensorSeries['units']
    sensorInterval = alertParameters['Interval']

    if debug_all: log.info('getSensorValues: sensor key %s: interval %s: units %s', sensorKey,sensorInterval , sensorUnits)


    try:


        #example queryQuery
        #select  median(temperature) AS temperature
        #from HS_68271935AFB5
        #where  deviceid='68271935AFB5'
        #AND  sensor='environmental_data'
        #AND instance='0'
        #AND (type='Outside Temperature' OR type='Outside Humidity')
        #AND time > 1698425630s and time < 1698426230s group by time(120s) 

        # get device to get sensor values from
        measurement = 'HS_' + str(alertParameters['deviceid'])


        #calculate start and end time from interval
        resolution = ""
        epochtimes = getepochtimes(sensorInterval)
        

        startepoch = epochtimes[0]
        endepoch = epochtimes[1]
        if resolution == "":
            resolution = epochtimes[2]

        # get sensor from key
        idbcseriesparameters = getSensorParameter(sensorKey)

        # get select from key
        idbcserieskeys = createInfluxDBCloudKeys(sensorKey)

        # setup query
        dbc = InfluxDBCloud(dchost, dcport, dcusername, dcpassword, dcdatabase,  ssl=True)


        dbcquery = ('select {} FROM {} '
                         'where {} AND time > {}s and time < {}s '
                         'group by *, time({}s) LIMIT 1') \
                    .format( idbcseriesparameters,  measurement, idbcserieskeys,
                            startepoch, endepoch,
                            resolution)
            
        if debug_all: log.info('getSensorValues: Influx Cloud Query String %s:  ', dbcquery)

        response= dbc.query(dbcquery)
        
        if debug_all: log.info('getSensorValues:  InfluxDB-Cloud response  %s:', response)
        #InfluxDB-Cloud response  ResultSet({'('HS_68271933E950',
        #{'deviceid': '68271933E950', 'instance': '0', 'parameter': 'engine_temp', 'sensor': 'engine_parameters_dynamic', 'type': 'NULL'})':
        #[{'time': '2023-10-27T19:30:00Z', 'engine_temp': 350.4}, {'time': '2023-10-27T19:35:00Z', 'engine_temp': 336.64}]}):

        if response is None:
            if debug_all: log.info('getSensorValues: InfluxDB Query has no data ')
            return None

        if not response:
            if debug_all: log.info('getSensorValues: InfluxDB Query has no data ')
            return None

        keys = response.raw.get('series',[])
        if debug_all: log.info("getSensorValues Get InfluxDB series keys %s", keys)

        for series in keys:
            if debug_all: log.info("getSensorValues Get InfluxDB series key %s", series)
            if debug_all: log.info("getSensorValues Get InfluxDB series tags %s ", series['tags'])
            if debug_all: log.info("getSensorValues Get InfluxDB series columns %s ", series['columns'])
            if debug_all: log.info("getSensorValues Get InfluxDB series values %s ", series['values'])

            for point in series['values']:
                # point[0] is time and point[1] is sensor value
                if point[0] is not None and  point[1] is not None:
                    if debug_all: log.info("getSensorValues Get InfluxDB sensor values %s ", point[1])
                    sensorValues.append(point[1])


        # return the sensor values
        return sensorValues
        
    except KeyError as e:
        if debug_all: log.info('getSensorValues: KeyError in EmailAlertPost-Cloud %s:  ' % str(e))

    except ValueError as e:
        if debug_all: log.info('getSensorValues: ValueError in EmailAlertPost-Cloud %s:  ' % str(e))

    except TypeError as e:
        if debug_all: log.info('getSensorValues: TypeError in EmailAlertPost-Cloud %s:  ' % str(e))

    except NameError as e:
        if debug_all: log.info('getSensorValues: NameError in EmailAlertPost-Cloud %s:  ' % str(e))
    
    except UnboundLocalError as e:
        if debug_all: log.info('getSensorValues: UnboundLocalError in EmailAlertPost-Cloud %s:  ' % str(e))

    except InfluxDBClientError as e:
      if debug_all: log.info('getSensorValues: Exception Error in InfluxDB  %s:  ' % str(e))
      
    except:
        e = sys.exc_info()[0]
        if debug_all: log.info("getSensorValues: Error: %s" % e)

# ****************************************************************
# 
# takes alert message sensor key and returns the switch values
# *************************************************************************
def getSwitchValues(parameters, alarmstatus):

  
  switchdata = {}

  # extract the series alarm paramterts
  series_parameters = parameters.get('series_1',"")
  if debug_all: log.info('getSwitchValues: alertParameters %s ',parameters)
  
  try:
    if series_parameters['alarmmode'] == 'alarmswitchon' or series_parameters['alarmmode'] == 'alarmswitchoff' or series_parameters['alarmmode'] == 'alarmswitchonoff' or series_parameters['alarmmode'] == 'alarmswitchoffon':
        #turn switch on if alarm is active and off if inactive
        if series_parameters['alarmmode'] == 'alarmswitchonoff' :
            if alarmstatus == 'active':
                switchdata = getSwitchIndex(parameters['EventTypeId'] )
                switchdata['value']=1  
                if debug_all: log.info('getSwitchValues: Email query switch data:alarmswitchonoff true %s: %s ', parameters['deviceid'], switchdata)
            else:
                switchdata = getSwitchIndex(parameters['EventTypeId'] )
                switchdata['value']=0  
                if debug_all: log.info('getSwitchValues: Email query switch data:alarmswitchonoff false %s: %s ', parameters['deviceid'], switchdata)

        # only turn switch off if alarm is active   and off if inactive         
        elif series_parameters['alarmmode'] == 'alarmswitchoffon' :
            if alarmstatus == 'active':
                switchdata = getSwitchIndex(parameters['EventTypeId'] )
                switchdata['value']=0                    
                if debug_all: log.info('getSwitchValues: Email query switch data:alarmswitchoffon true %s: %s ', parameters['deviceid'], switchdata)
            else:
                switchdata = getSwitchIndex(parameters['EventTypeId'] )
                switchdata['value']=1                    
                if debug_all: log.info('getSwitchValues: Email query switch data:alarmswitchoffon false %s: %s ', parameters['deviceid'], switchdata)

        # only turn switch on if alarm is active                 
        elif series_parameters['alarmmode'] == 'alarmswitchon' :
            if alarmstatus == 'active':
                switchdata = getSwitchIndex(parameters['EventTypeId'] )
                switchdata['value']=1  
                if debug_all: log.info('getSwitchValues: Email query switch data:alarmswitchon true %s: %s ', parameters['deviceid'], switchdata)


        # only turn switch off if alarm is active             
        elif series_parameters['alarmmode'] == 'alarmswitchoff' :
            if alarmstatus == 'active':
                switchdata = getSwitchIndex(parameters['EventTypeId'] )
                switchdata['value']=0                    
                if debug_all: log.info('getSwitchValues: Email query switch data:alarmswitchoff true %s: %s ', parameters['deviceid'], switchdata)


    if switchdata != {}:
      if debug_all: log.info('getSwitchValues: parameters %s: switchdata %s ', parameters['deviceid'], switchdata)
    return switchdata


  except KeyError as e:
      if debug_all: log.info('getSwitchValues: KeyError in EmailAlertPost-Cloud %s:  ' % str(e))

  except ValueError as e:
      if debug_all: log.info('getSwitchValues: ValueError in EmailAlertPost-Cloud %s:  ' % str(e))

  except TypeError as e:
      if debug_all: log.info('getSwitchValues: TypeError in EmailAlertPost-Cloud %s:  ' % str(e))

  except NameError as e:
      if debug_all: log.info('getSwitchValues: NameError in EmailAlertPost-Cloud %s:  ' % str(e))

  except UnboundLocalError as e:
      if debug_all: log.info('getSwitchValues: UnboundLocalError in EmailAlertPost-Cloud %s:  ' % str(e))
      
  except:
      e = sys.exc_info()[0]
      if debug_all: log.info("getSwitchValues: Error: %s" % e)

# ****************************************************************
# 
# takes alert message sensor key and returns the dimmer values
# *************************************************************************
def getDimmerValues(parameters, alarmstatus):

  
  dimmerdata = {}

  # extract the series alarm paramterts
  series_parameters = parameters.get('series_1',"")

  try:
    if series_parameters['alarmmode'] == 'alarmleddimmer' or series_parameters['alarmmode'] == 'alarmrgbdimmer' or series_parameters['alarmmode'] == 'alarmblinkdimmer' or series_parameters['alarmmode'] == 'alarmblinkdimmeronoff' or series_parameters['alarmmode'] == 'alarmdimmeroverride':
      if series_parameters['alarmmode'] == 'alarmleddimmer' :
          if alarmstatus == 'active':
              dimmerdata = getDimmerIndex(parameters['EventTypeId'] )
              dimmerdata['value']=parameters['alertaction_value']   
              if debug_all: log.info('getDimmerValues: Email query dimmer data:alarmleddimmer true %s: %s ', parameters['deviceid'], dimmerdata)
          else:
              #dimmerdata = getDimmerIndex(parameters['EventTypeId'] )
              #dimmerdata['value']=0  
              if debug_all: log.info('getDimmerValues: Email query dimmer data:alarmleddimmer false %s: %s ', parameters['deviceid'], dimmerdata)

          
      elif series_parameters['alarmmode'] == 'alarmrgbdimmer' :
          if alarmstatus == 'active':
              dimmerdata = getDimmerIndex(parameters['EventTypeId'] )
              dimmerdata['value']=parameters['alertaction_value']                       
              if debug_all: log.info('getDimmerValues: Email query dimmer data:alarmrgbdimmer true %s: %s ', parameters['deviceid'], dimmerdata)
          else:
              #dimmerdata = getDimmerIndex(parameters['EventTypeId'] )
              #dimmerdata['value']=0                    
              if debug_all: log.info('getDimmerValues: Email query dimmer data:alarmrgbdimmer false %s: %s ', parameters['deviceid'], dimmerdata)

          
      elif series_parameters['alarmmode'] == 'alarmblinkdimmer' :
          if alarmstatus == 'active':
              dimmerdata = getDimmerIndex(parameters['EventTypeId'] )
              dimmerdata['value']=parameters['alertaction_value']                       
              if debug_all: log.info('Telemetrypost: Email query dimmer data:alarmblinkdimmer true %s: %s ', parameters['deviceid'], dimmerdata)
          else:
              #dimmerdata = getDimmerIndex(parameters['EventTypeId'] )
              #dimmerdata['value']=0                    
              if debug_all: log.info('getDimmerValues: Email query dimmer data:alarmblinkdimmer false %s: %s ', parameters['deviceid'], dimmerdata)

      elif series_parameters['alarmmode'] == 'alarmblinkdimmeronoff' :
          if alarmstatus == 'active':
              dimmerdata = getDimmerIndex(parameters['EventTypeId'] )
              dimmerdata['value']=parameters['alertaction_value']                       
              if debug_all: log.info('getDimmerValues: Email query dimmer data:alarmblinkdimmeronoff true %s: %s ', parameters['deviceid'], dimmerdata)
          else:
              dimmerdata = getDimmerIndex(parameters['EventTypeId'] )
              dimmerdata['value']=0                    
              if debug_all: log.info('Telemetrypost: Email query dimmer data:alarmblinkdimmeronoff false %s: %s ', parameters['deviceid'], dimmerdata)

      elif series_parameters['alarmmode'] == 'alarmdimmeroverride' :
          if alarmstatus == 'active':
              dimmerdata = getDimmerIndex(parameters['EventTypeId'] )
              dimmerdata['value']=parameters['alertaction_value']
              dimmerdata['override']=2
              if debug_all: log.info('getDimmerValues: Email query dimmer data:alarmdimmeroverride true %s: %s ', parameters['deviceid'], dimmerdata)
          else:
              dimmerdata = getDimmerIndex(parameters['EventTypeId'] )
              dimmerdata['value']=255
              dimmerdata['override']=1
              if debug_all: log.info('getDimmerValues: Email query dimmer data:alarmdimmeroverride false %s: %s ', parameters['deviceid'], dimmerdata)

    if dimmerdata != {}:
      if debug_all: log.info('getDimmerValues: parameters %s: dimmerdata = %s ', parameters['deviceid'], dimmerdata)
    return dimmerdata


  except KeyError as e:
      if debug_all: log.info('getDimmerValues error: KeyError in EmailAlertPost-Cloud %s:  ' % str(e))

  except ValueError as e:
      if debug_all: log.info('getDimmerValues error: ValueError in EmailAlertPost-Cloud %s:  ' % str(e))

  except TypeError as e:
      if debug_all: log.info('getDimmerValues error: TypeError in EmailAlertPost-Cloud %s:  ' % str(e))

  except NameError as e:
      if debug_all: log.info('getDimmerValues error: NameError in EmailAlertPost-Cloud %s:  ' % str(e))

  except UnboundLocalError as e:
      if debug_all: log.info('getDimmerValues error: UnboundLocalError in EmailAlertPost-Cloud %s:  ' % str(e))
      
  except:
      e = sys.exc_info()[0]
      if debug_all: log.info("getDimmerValues error: Error: %s" % e)

# ****************************************************************
# SEND EMAIL ALERT
# *************************************************************************
def SendEMAILAlert(parameters, alarmresult):


  alarmstatus = alarmresult.get('status', "")

  if alarmstatus != "active":
    if debug_all: log.info('SendEMAILAlert: Email alarm is not active - returning ')
    return

  try:    

    # extract the series alarm paramterts
    series_parameters = parameters.get('series_1',"")

    email_body = alarmresult['message']

    if debug_all: log.info('SendEMAILAlert: Email query %s: %s ', parameters['deviceid'], email_body)
    
    if email_body != "":
        #alertemail = parameters['email']
        alertemail = ""
        
        conn = db_pool.getconn()

        #query = "select alertemail, smsnumber from user_devices where deviceid = %s"
        query = "select alertemail, devicename from user_devices where deviceid = %s"
        
        if debug_all: log.info('SendEMAILAlert: Email query  %s ', query)
        
        try:
            # first check db to see if user id is matched to device id
            cursor = conn.cursor()
            cursor.execute(query, (parameters['deviceid'],))
            records = cursor.fetchall()

            if cursor.rowcount == 0:
                if debug_all: log.info('SendEMAILAlert: Email query -> no records found')
                return
              
            if debug_info: log.info('SendEMAILAlert: records is %s:  ', records)

            for row in records:     
                if debug_info: log.info('SendEMAILAlert: row is %s:  ', row)
                alertemail = str(row[0])
                devicename = str(row[1])
                #smsnumber = str(row[1]) 
                if debug_info: log.info('SendEMAILAlert: Email is %s: devicename %s ', alertemail, devicename)
                if alertemail != "" and alertemail !="None" and alertemail is not None:
                    try:
                      #sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
                      #from_email = Email("alerts@seasmart.net")
                      #subject = parameters['subject']
                      #to_email = Email(alertemail)
                      #to_email = Email("joe@seagauge.com")
                      #content = Content("text/plain", email_body)
                      #mail = Mail(from_email, subject, to_email, content)
                      #sgresponse = sg.client.mail.send.post(request_body=mail.get())

                      #if debug_all: log.info('SendEMAILAlert: Email SenGrid response.status %s',sgresponse.status_code)
                      #if debug_all: log.info('SendEMAILAlert: Email SenGrid response.body %s',sgresponse.body)
                      #if debug_all: log.info('SendEMAILAlert: Email SenGrid response.headers %s',sgresponse.headers)


                      # sender
                      sender_user = 'alerts'
                      sender_email = "@".join([sender_user, mailertogo_domain])
                      sender_name = 'HelmSmart Sensor Alert'

                      if debug_all: log.info("SendEMAILAlert mailertogo send sender_email %s:  ", sender_email)

                      # recipient
                      #recipient_email = 'joe@seagauge.com' # change to recipient email. Make sure to use a real email address in your tests to avoid hard bounces and protect your reputation as a sender.
                      recipient_email = alertemail # change to recipient email. Make sure to use a real email address in your tests to avoid hard bounces and protect your reputation as a sender.
                      recipient_name = devicename
                      if debug_all: log.info("SendEMAILAlert mailertogo send sender_email %s:  ", recipient_email)
                      
                      # subject
                      subject = parameters['subject']
                      if debug_all: log.info("SendEMAILAlert mailertogo send subject %s:  ", subject)

                      # text body
                      #body_plain = ("Hi,\n"  "Test from Mailer To Go 😊\n"   )
                      body_plain = (email_body  )
                      if debug_all: log.info("SendEMAILAlert mailertogo send body_plain %s:  ", body_plain)

                      # html body
                      line_break = '\n' #used to replace line breaks with html breaks
                      body_html = f'''<html><head></head> <body> {'<br/>'.join(body_plain.split(line_break))} </body> </html>'''
                      if debug_all: log.info("SendEMAILAlert mailertogo send body_html %s:  ", body_html)

                      # create message container
                      message = MIMEMultipart('alternative')
                      message['Subject'] = parameters['subject']
                      message['From'] = email.utils.formataddr((sender_name, sender_email))
                      message['To'] = email.utils.formataddr((recipient_name, recipient_email))

                      if debug_all: log.info("SendEMAILAlert mailertogo send message %s:  ", message)

                      # prepare plain and html message parts
                      part1 = MIMEText(body_plain, 'plain')
                      part2 = MIMEText(body_html, 'html')

                      # attach parts to message

                      message.attach(part1)
                      message.attach(part2)

                      if debug_all: log.info("SendEMAILAlert mailertogo send message %s:  ", message)

                      # send the message.
                      try:
                        server = smtplib.SMTP(mailertogo_host, mailertogo_port)
                        server.ehlo()
                        server.starttls()
                        server.ehlo()
                        server.login(mailertogo_user, mailertogo_password)
                        server.sendmail(sender_email, recipient_email, message.as_string())
                        server.close()

                      except TypeError as e:
                        if debug_all: log.info("SendEMAILAlert mailertogo send alertemail %s:  ", alertemail)
                        if debug_all: log.info('SendEMAILAlert  mailertogo send TYPE Error %s:  ' % e)
                      except NameError as e:
                        if debug_all: log.info("SendEMAILAlert mailertogo send alertemail %s:  ", alertemail)
                        if debug_all: log.info('SendEMAILAlert  mailertogo send NAME Error %s:  ' % e)
                      except Exception as e:
                        if debug_all: log.info('SendEMAILAlert: mailertogo Error %s:  ' % str(e)) 
                      else:
                        if debug_all: log.info("SendEMAILAlert mailertogo sent %s:  ", part1)


                    except TypeError as e:
                      if debug_all: log.info("SendEMAILAlert mailertogo alertemail %s:  ", alertemail)
                      if debug_all: log.info('SendEMAILAlert  mailertogo TYPE Error %s:  ' % e)                     
                    except NameError as e:
                      if debug_all: log.info("SendEMAILAlert mailertogo alertemail %s:  ", alertemail)
                      if debug_all: log.info('SendEMAILAlert  mailertogo NAME Error %s:  ' % e)
                    except:
                      e = sys.exc_info()[0]   
                      if debug_all: log.info('SendEMAILAlert: sendgrid Error %s:  ' % str(e))                                

                else:
                  if debug_info: log.info('SendEMAILAlert: no alertemail number found - returnig : devicename %s ', devicename)
                  
        except TypeError as e:
          if debug_all: log.info("SendEMAILAlert mailertogo alertemail %s:  ", alertemail)
          if debug_all: log.info('SendEMAILAlert  mailertogo TYPE Error %s:  ' % e)     
        except NameError as e:
          if debug_all: log.info("SendEMAILAlert mailertogo alertemail %s:  ", alertemail)
          if debug_all: log.info('SendEMAILAlert  mailertogo NAME Error %s:  ' % e)                        
        except:
            alertemail = ''
            smsnumber = ''
            e = sys.exc_info()[0]   
            if debug_all: log.info('SendEMAILAlert: Error %s:  ' % str(e))      

        finally:
            db_pool.putconn(conn)

  except TypeError as e:
    if debug_all: log.info("SendEMAILAlert alertemail %s:  ", alertemail)
    if debug_all: log.info('SendEMAILAlert  TYPE Error %s:  ' % e)
  except NameError as e:
    if debug_all: log.info("SendEMAILAlert alertemail %s:  ", alertemail)
    if debug_all: log.info('SendEMAILAlert  NAME Error %s:  ' % e)
    
  except:
    e = sys.exc_info()[0]   
    if debug_all: log.info('SendEMAILAlert: Error %s:  ' % str(e))

    

# ****************************************************************
# SEND SMS ALERT
# *************************************************************************
def SendSMSAlert(parameters, alarmresult):

  alarmstatus = alarmresult.get('status', "")

  if alarmstatus != "active":
    if debug_all: log.info('SendSMSAlert: Email alarm is not active - returning ')
    return

  alertesms = ""
  
  try:    

    # extract the series alarm paramterts
    series_parameters = parameters.get('series_1',"")

    email_body = alarmresult['message']

    if debug_all: log.info('SendSMSAlert: SMS query %s: %s ', parameters['deviceid'], email_body)
    
    if email_body != "":
        #alertemail = parameters['email']
        alertesms = ""
        
        conn = db_pool.getconn()

        #query = "select alertemail, smsnumber from user_devices where deviceid = %s"
        query = "select smsnumber, devicename from user_devices where deviceid = %s"
        
        if debug_all: log.info('SendSMSAlert: Email query  %s ', query)
        
        try:
            # first check db to see if user id is matched to device id
            cursor = conn.cursor()
            cursor.execute(query, (parameters['deviceid'],))
            records = cursor.fetchall()

            if cursor.rowcount == 0:
                if debug_all: log.info('SendSMSAlert: Email query -> no records found')
                return
              
            if debug_info: log.info('SendSMSAlert: records is %s:  ', records)

            for row in records:     
                if debug_info: log.info('SendSMSAlert: row is %s:  ', row)
                alertesms = str(row[0])
                devicename = str(row[1])
                #smsnumber = str(row[1]) 
                if debug_info: log.info('SendSMSAlert: alertesms is %s: devicename %s ', alertesms, devicename)
                if alertesms != "" and alertesms != "None" and alertesms is not None:
                  try:
                    # Find your Account SID and Auth Token at twilio.com/console
                    # and set the environment variables. See http://twil.io/secure
                    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
                    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
                    
                    if debug_info: log.info('SendSMSAlert: good alertesms is %s: devicename %s ', alertesms, devicename)
                    client = smsClient(account_sid, auth_token)
                    message = client.messages.create(  body=email_body, from_='+18449794144', to='+15416612051')

                    if message.error_message:
                      raise Exception(f"Failed to send : {message.error_message}")
                    else:
                      log.info("SendSMSAlert twilio send message.sid %s:  ", message.sid)


                  except TypeError as e:
                    if debug_all: log.info("SendSMSAlert twilio alertemail %s:  ", alertesms)
                    if debug_all: log.info('SendSMSAlert  twilio TYPE Error %s:  ' % e)                     
                  except NameError as e:
                    if debug_all: log.info("SendSMSAlert twilio alertemail %s:  ", alertesms)
                    if debug_all: log.info('SendSMSAlert  twilio NAME Error %s:  ' % e)
                  except:
                    e = sys.exc_info()[0]   
                    if debug_all: log.info('SendSMSAlert: twilio Error %s:  ' % str(e))
                    
                else:
                  if debug_info: log.info('SendSMSAlert: no alertesms number found - returnig : devicename %s ', devicename)
                  
        except TypeError as e:
          if debug_all: log.info("SendSMSAlert twilio alertesms %s:  ", alertesms)
          if debug_all: log.info('SendSMSAlert  twilio TYPE Error %s:  ' % e)     
        except NameError as e:
          if debug_all: log.info("SendSMSAlert twilio alertesms %s:  ", alertesms)
          if debug_all: log.info('SendSMSAlert  twilio NAME Error %s:  ' % e)                        
        except:
            alertemail = ''
            smsnumber = ''
            e = sys.exc_info()[0]   
            if debug_all: log.info('SendSMSAlert: Error %s:  ' % str(e))      

        finally:
            db_pool.putconn(conn)

  except TypeError as e:
    if debug_all: log.info("SendSMSAlert alertemail %s:  ", alertesms)
    if debug_all: log.info('SendSMSAlert  TYPE Error %s:  ' % e)
  except NameError as e:
    if debug_all: log.info("SendSMSAlert alertemail %s:  ", alertesms)
    if debug_all: log.info('SendSMSAlert  NAME Error %s:  ' % e)
    
  except:
    e = sys.exc_info()[0]   
    if debug_all: log.info('SendSMSAlert: Error %s:  ' % str(e))


  
# ****************************************************************
# SEND HelmSmart ALERT
# Creates a 'SSEA00' message and puts into SQS Que for the sqs_poller theads to process
# contains the alert messages and any switch or dimmer data
# *************************************************************************
def SendHSAlert(alertkey, parameters, alarmresult, sensorValueUnits, switchdata, dimmerdata, timmerdata):


  payload = {}
  data = {}

  try:    
    if debug_info: log.info('SendHSAlert: parameters %s:  ', parameters)
    # extract the series alarm paramterts
    series_parameters = parameters.get('series_1',"")

    nowtime = datetime.datetime.now()
  
    data['subject']= parameters.get('subject',"")
    data['interval']= parameters.get('Interval',"")
    data['AlertId']= alertkey

    data['alertmode']= parameters.get('alertmode', "disabled")
    data['alerttype']= parameters.get('alerttype', "mean")
    data['alertaction_value']= parameters.get('alertaction_value', "---")
    data['locationcity']= parameters.get('locationcity', "---")


    data['alert_sunrise']=  alarmresult.get('sunrise', "---")
    data['alert_sunset']=   alarmresult.get('sunset', "---")

    data['timestamp']= nowtime.strftime("%Y-%m-%d %H:%M:%S")

    
    #if debug_all: log.info('Posting to AlertPosts make_HSAlert_json ')

    if sensorValueUnits == "---":
        if debug_all: log.info('Posting to AlertPosts make_HSAlert_json empty points')

        

        if series_parameters.get('parameter',"") == "latlng":
            data['series_1']=make_HSAlert_json("series_1", parameters, "", "missing", alarmresult['status'] )
            data['series_2']=make_HSAlert_json("series_1", parameters, "", "missing", alarmresult['status'] )
        else:
            data['series_1']=make_HSAlert_json("series_1", parameters, "",  "missing",  alarmresult['status'])

    # todo - add latlng precessing here
                
    elif sensorValueUnits != None: 
        data['series_1']=make_HSAlert_json("series_1", parameters, "", sensorValueUnits, alarmresult['status'])
        
    else:
        data['series_1']=make_HSAlert_json("series_1", parameters, "",  "error", "")



    payload['data']=data

    if debug_all: log.info('SendHSAlert: EmailAlertPost-Cloud payload %s:  ', payload)
    if debug_all: log.info('SendHSAlert: EmailAlertPost-Cloud switch %s:  ', switchdata)

    remote_mode = parameters.get('remotemode','singleevent')
    if debug_all: log.info('SendHSAlert: EmailAlertPost-Cloud remote mode %s:  ', remote_mode)

    if remote_mode == 'singleevent':
        timmerdata_key = ""
        dimmerdata_key = dimmerdata
    elif remote_mode == 'dailytimmertable':
        dimmerdata_key = ""
        timmerdata_key = timmerdata
    elif remote_mode == 'dailytimmerspan':
        dimmerdata_key = ""
        timmerdata_key = timmerdata
     

    if debug_all: log.info('SendHSAlert:  payload %s:  ', payload)     

    # que up HSAlert message
    """
    sqs_queue.write(queue.new_message(json.dumps(
        dict(
              partition = "SSEA00_000000_00"+myTime+".txt",
              device_id = parameters['deviceid'],
              subject = parameters['subject'] ,
              payload =  data,
              switchdata = switchdata,
              
              dimmerdata = dimmerdata_key,
              timmerdata = timmerdata_key,

              
              content_type = 'application/json',
              dyno_id = os.environ['DYNO']
                )
        )))          
    # end of message queing ,cls = MyEncoder
    mymessage='qued SQS message for Alerts updaate'
    """

    try:

      device_id = parameters.get('deviceid', "")

      #"partition": "SSA300_000051_01231026203849.txt"
      #partition = "SSEA00"
      #partition = "SSEA00_000000_00"+myTime+".txt",
      myTime = nowtime.strftime("%y%m%d%H%M%S")

      
      if debug_all: log.info("SendHSAlert SQS:Parse JSON payload %s:  ", payload)
      
      device_json = json.dumps(
        dict(
                partition = "SSEA00_000000_00"+myTime+".txt",
                device_id = parameters['deviceid'],
                subject = parameters['subject'] ,
                payload =  data,
                switchdata = switchdata,
                dimmerdata = dimmerdata_key,
                timmerdata = timmerdata_key,
                content_type = 'application/json',
                dyno_id = os.environ['DYNO']
              ),
        cls=DateEncoder)

      #takes the switch/dimmer/timmer values and sends to helmsmart uri so they can be appened to any SeaSmart post message responce
      proccess_http_alerts(device_json)

      
      #if debug_all: log.info("Que SQS:Parse JSON device_id %s: partition: %s data: %s ", device_id, partition, device_json)
      if debug_all: log.info("SendHSAlertSQS:Parse JSON device_id %s:  ", device_id)
      if debug_all: log.info("SendHSAlert:Parse JSON device_json %s:  ", device_json)

    except SystemExit as e:
      if debug_all: log.info("SendHSAlert SQS:SystemExitError device_id %s: partition: %s  ", device_id, partition, )
      if debug_all: log.info('Que SQS:SystemExitError  Error in que SQS %s:  ' % e)

    except NameError as e:
      if debug_all: log.info("SendHSAlert SQS:NameError device_id %s:  ", device_id)
      if debug_all: log.info('SendHSAlert SQS:NameError  Error in que SQS %s:  ' % e)

    except TypeError as e:
      if debug_all: log.info("Que SQS:TypeError device_id %s: ", device_id)
      if debug_all: log.info('Que SQS:TypeError  Error in que SQS %s:  ' % e)
      
    except UnicodeDecodeError as e:
      if debug_all: log.info("SendHSAlert SQS:UnicodeDecodeError device_id %s: ", device_id)
      if debug_all: log.info('SendHSAlert SQS:UnicodeDecodeError  Error in que SQS %s:  ' % e)
      
    except:
      e = sys.exc_info()[0]
      if debug_all: log.info("SendHSAlert SQS:device_id %s: partition: %s ", device_id, partition)
      if debug_all: log.info('SendHSAlert SQS: Error in que SQS %s:  ' % e)

  

  except NameError as e:
    if debug_all: log.info('process_message: NameError in SendHSAlert %s:  ' % str(e))
    
  except AttributeError as e:
    if debug_all: log.info('process_message: AttributeError in SendHSAlert %s:  ' % str(e))

  except TypeError as e:
    if debug_all: log.info('process_message: TypeError in SendHSAlert %s:  ' % str(e))
        
  except:
    e = sys.exc_info()[0]   
    if debug_all: log.info('SendHSAlert: Error %s:  ' % str(e))



def proccess_http_alerts(message_body):

  #062914 JLB
  # test to read custom message from SQS que
  try:
    #message_body = json.loads(message['Body'])
    #message_body =message
    message =json.loads(message_body)
    #partition = message_body['partition'][:-4]


    #if debug_all: log.info('sqs_poller proc Got SQS message_body %s:  ', message_body)

    mpartition = message.get('partition')
    device_id = message.get('device_id')

    #if debug_all: log.info('s3_poller Got SQS message %s: ', partition)
    if debug_all: log.info('sqs_alerts_poller Got SQS message %s: device %s ', mpartition,device_id)
    #partition = message['partition'][:-4]
    #if debug_all: log.info('s3_poller Got SQS message %s: ', partition)
    #if debug_all: log.info('sqs_poller Got SQS message %s: device %s ', partition, message['device_id'])
    
    #if debug_all: log.info('sqs_poller proc Got SQS message_body %s:  ', message_body)

    partition = mpartition[:-4]
    if debug_all: log.info('sqs_alerts_poller Got SQS message partition %s: ', partition)
    

    try:
      if debug_all: log.info('Got Alert message %s: %s ', device_id, partition)


      try:
        records = message['payload']
        device = message['device_id']
        partition = message['partition'][:-4]
        switchdata = message.get('switchdata', {})
        if debug_all: log.info('sqs_alerts_poller:SSEA00 switch %s: %s ', device, switchdata)

        dimmerdata = message.get('dimmerdata', {})
        if debug_all: log.info('sqs_alerts_poller:SSEA00 dimmerdata %s: %s ', device, dimmerdata)

        timmerdata = message.get('timmerdata', {})
        if debug_all: log.info('sqs_alerts_poller:SSEA00 timmerdata %s: %s ', device, timmerdata)       
        
  
        if debug_all: log.info('sqs_alerts_poller got EmailAlert %s: %s', device, records)
        #dump_firebase(device,  "Alert", partition, json.dumps(records))
        dump_pcdinfirebase(device,  "Alert", partition, json.dumps(records))
        
        
        #if debug_all: log.info('sqs_poller: Alert message update_firebase_index %s: %s ', device, partition)
        #update_firebase_index(device, "Alert", partition)
        
        if debug_all: log.info('Inserted Alert message %s: %s ', device, partition)
        
      except:
        if debug_all: log.info('sqs_alerts_poller:: Error in proc SSEA00 %s:', partition)

        e = sys.exc_info()[0]
        if debug_all: log.info("sqs_alerts_poller::  in proc SSEA00 Error: %s" % e)
        pass


      #if timmerdata or (timmerdata != ""  and timmerdata != None and timmerdata is not None):
      #if timmerdata  is not {}:
      if timmerdata :
        #url = "https://api.telemetryapp.com/data"
        if debug_all: log.info('sqs_alerts_poller:SSEA00 timmerdata  %s ', timmerdata)
        timmerInstance  =timmerdata.get('instance',0)
        timmerType  =timmerdata.get('type','LED Dimmer 4 Channel')
        timmerParameter  =timmerdata.get('parameter','value0')
        timmerArray =timmerdata.get('timmer_array',"")
        
        devicedataurl = "http://helmsmart-cloud.herokuapp.com/settimmerapi?deviceid=" + str(device)
        devicedataurl = devicedataurl + "&instance=" + str(timmerInstance)
        devicedataurl = devicedataurl + "&type=" + str(timmerType)
        devicedataurl = devicedataurl + "&parameter=" + str(timmerParameter)
        devicedataurl = devicedataurl + "&array=" + str(timmerArray)

        if debug_all: log.info("sqs_poller:  in proc SSEA00 timmer: %s", devicedataurl)

        
        headers = {'content-type': 'application/json'}
        response = requests.get(devicedataurl)

      #if switchdata or (switchdata != ""  and switchdata != None and switchdata is not None):
      #if switchdata  is not {}:
      if switchdata :          
        #url = "https://api.telemetryapp.com/data"
        if debug_all: log.info('sqs_alerts_poller:SSEA00 switchdata  %s ', switchdata)
        switchInstance  =switchdata.get('instance',15)
        switchid  =switchdata.get('index',15)
        switchvalue =switchdata.get('value',3)

        devicedataurl = "http://helmsmart-cloud.herokuapp.com/setswitchapi?deviceid=" + str(device)
        devicedataurl = devicedataurl + "&instance=" + str(switchInstance)
        devicedataurl = devicedataurl + "&switchid=" + str(switchid)
        devicedataurl = devicedataurl + "&switchvalue=" + str(switchvalue)

        if debug_all: log.info("sqs_alerts_poller:  in proc SSEA00 switch: %s", devicedataurl)

        
        headers = {'content-type': 'application/json'}
        response = requests.get(devicedataurl)


      #if dimmerdata or (dimmerdata != ""  and dimmerdata != None and dimmerdata is not None):
      #if dimmerdata  is not {}:
      if dimmerdata  :                
        if debug_all: log.info('sqs_alerts_poller:SSEA00 dimmer  %s ', dimmerdata)
        dimmerInstance  =dimmerdata.get('instance',15)
        dimmerid  =dimmerdata.get('index',15)
        dimmervalue =dimmerdata.get('value',255)
        dimmeroverride =dimmerdata.get('override',0)
        
        devicedataurl = "http://helmsmart-cloud.herokuapp.com/setdimmerapi?deviceid=" + str(device)
        devicedataurl = devicedataurl + "&instance=" + str(dimmerInstance)
        devicedataurl = devicedataurl + "&dimmerid=" + str(dimmerid)
        devicedataurl = devicedataurl + "&dimmervalue=" + str(dimmervalue)
        devicedataurl = devicedataurl + "&dimmeroverride=" + str(dimmeroverride)
        
        if debug_all: log.info("sqs_alerts_poller:  in proc SSEA00 dimmer: %s", devicedataurl)

        
        headers = {'content-type': 'application/json'}
        response = requests.get(devicedataurl)






      
    except:
      if debug_all: log.info('sqs_alerts_poller:: Error in proc SSEA00 %s:', partition)

      e = sys.exc_info()[0]
      if debug_all: log.info("sqs_alerts_poller::  in proc SSEA00 Error: %s" % str(e))
      pass


    

  except AttributeError as e:
    #if debug_all: log.info('sqs_poller:: TypeError in proc  %s:  ', partition)

    if debug_all: log.info('sqs_alerts_poller:: TypeError in proc  %s:  ' % str(e))
    
  except TypeError as e:
    #if debug_all: log.info('sqs_poller:: TypeError in proc  %s:  ', partition)

    if debug_all: log.info('sqs_alerts_poller:: TypeError in proc  %s:  ' % str(e))
      
  except KeyError as e:
    #if debug_all: log.info('sqs_poller:: KeyError in proc %s:  ', partition)

    if debug_all: log.info('sqs_alerts_poller:: KeyError in proc  %s:  ' % str(e))

  except NameError as e:
    #if debug_all: log.info('sqs_poller:: NameError in proc  %s:  ', partition)

    if debug_all: log.info('sqs_alerts_poller:: NameError in proc  %s:  ' % str(e))
      
  except:
    #if debug_all: log.info('sqs_poller:: Error in proc  %s:', partition)

    e = sys.exc_info()[0]
    if debug_all: log.info("sqs_alerts_poller::  in proc Error: %s" % e)
    pass     



  
# ****************************************************************
# Main message processor
# takes alert message parameters and does a InfluxDB lookup to get sensor values
# then preforms alert analytics to determine event
# *************************************************************************
def process_message(alert_message):

    parameters = alert_message['parameters']
    alertkey = alert_message['key']
    starttime = alert_message['starttime']

    posttype = parameters['posttype']
    alerttype=parameters.get('alerttype', "mean")

    if debug_info: log.info('Posting to Web Services %s:%s', posttype, starttime)
    #mymessage='returning from Telemetry post'  
    #return mymessage

    #conn = db_pool.getconn()

    #if debug_all: log.info('Device ID  = ' + records[0][0])
    #deviceid = records[0][0]

    API_KEY = '7be1d82569414dceaa82fd93fadd7940'
    API_SECRET = '0447ec319c3148cb98d96bfc96c787e1'
  
    points={}
    times={}
    timesiso={}

    #initialize current time
    nowtime = datetime.datetime.now()
    myTime = nowtime.strftime("%y%m%d%H%M%S")
    

    posttypecloud=None

    if posttype == "EmailAlertPost":
        posttypecloud = "EmailAlertPost-Cloud"


        
    # get sensor values from influxdb
    sensorValues = getSensorValues(parameters)
    if sensorValues == None:
        sensorValues='missing'
        #return mymessage

    if debug_all: log.info('process_message: sensor values %s', sensorValues)

    

    
# **************************************************************************************
# If Email alert then check values for High/Low alarms and send out email if active
#****************************************************************************************
    try:

        if posttypecloud == "EmailAlertPost-Cloud":
          #if debug_all: log.info('Posting to AlertPosts :')

          if debug_info: log.info('Posting to EmailAlertPost-Cloud deviceid = %s:', parameters['deviceid'])
          if debug_all: log.info('Posting to EmailAlertPost-Cloud %s:', parameters)

          email_body = ""
          timmer_array = ""
          timmerdata={}
          distance = ""

          # extract the series alarm paramterts
          #{'title': '/M2M/LED Dimmer/Value 0 Zone 1', 'alarmtype': 'sensor', 'units': '42', 'alarmlow': 'Brookings', 'alarmhigh': 'Brookings', 'key': 'deviceid:001EC0359C2B.sensor:seasmartdimmer.source:.*.instance:1.type:LED 1 Channel.parameter:value0.HelmSmart', 'alarmmode': 'alarmleddimmer'} 
          series_parameters = parameters.get('series_1',"")
          
          #'key': 'deviceid:001EC0359C2B.sensor:seasmartdimmer.source:.*.instance:1.type:LED 1 Channel.parameter:value0.HelmSmart'
          series_key = series_parameters.get('key',"")

          # #########################################################
          # First lets process sensor values and check for any alarms and create email messages
          # #########################################################
          
          if sensorValues == "missing":
              
              if debug_all: log.info('Posting to EmailAlertPost empty points ')
              alarmresult = process_emailalert(email_body,  parameters, nowtime.strftime("%Y-%m-%d %H:%M:%S"), "missing")
              email_body = alarmresult['message']
              if debug_all: log.info('Posting to EmailAlertPost empty points email_body = %s', email_body)

              sensorValueUnits = "---"
              
              timmer_array = alarmresult.get('timmerArray', "")
              if timmer_array != "":

                timmerdata['type'] =""
                timmerdata['instance'] =""
                timmerdata['parameter'] =""
                timmerdata['timmer_array'] = timmer_array
                  
                if series_parameters != "":
                  timmerdata['instance'] = getSensorTag(series_key, 3)
                  timmerdata['type'] = getSensorTag(series_key, 4)
                  timmerdata['parameter'] = getSensorTag(series_key, 5)


          else:
            if len(sensorValues) != 0:
              sensorValueUnits = convertunits(sensorValues[0], series_parameters['units'])
              if debug_all: log.info('process_message: sensor value units %s', sensorValueUnits)
              alarmresult = process_emailalert(email_body,  parameters, nowtime.strftime("%Y-%m-%d %H:%M:%S"), sensorValueUnits)

            else:
              alarmresult = process_emailalert(email_body,  parameters, nowtime.strftime("%Y-%m-%d %H:%M:%S"), "missing")


            alarm_status = alarmresult['status']
            if debug_all: log.info('Posting to EmailAlertPost alarmresult alarm_status = %s', alarm_status)

            email_body = alarmresult['message']
            if debug_all: log.info('Posting to EmailAlertPost alarmresult email_body = %s', email_body)

            
            timmer_array = alarmresult.get('timmerArray', "")
            if timmer_array != "":

              timmerdata['type'] =""
              timmerdata['instance'] =""
              timmerdata['parameter'] =""
              timmerdata['timmer_array'] = timmer_array
                
              if series_parameters != "":
                timmerdata['instance'] = getSensorTag(series_key, 3)
                timmerdata['type'] = getSensorTag(series_key, 4)
                timmerdata['parameter'] = getSensorTag(series_key, 5)
              

          if email_body != "":        
              if debug_all: log.info('Posting to EmailAlertPost-Cloud   email_body= %s:', email_body)
          else:
              if debug_all: log.info('Posting to EmailAlertPost-Cloud   email_body= blank ' )


          if timmer_array != "":        
              if debug_all: log.info('Posting to EmailAlertPost-Cloud   timmer_array= %s:', timmer_array)
          else:
              if debug_all: log.info('Posting to EmailAlertPost-Cloud   timmer_array= blank ' )

          # #########################################################
          # second lets check for any switch data and get switch states
          # #########################################################
          switchdata = getSwitchValues(parameters, alarmresult['status'])

          if debug_all: log.info('Posting to EmailAlertPost-Cloud: Email query switch data %s: %s ', parameters['deviceid'], switchdata)
          # #########################################################
          # third lets check for any dimmer data and get dimmer states
          # #########################################################
          dimmerdata = getDimmerValues(parameters, alarmresult['status'])

          if debug_all: log.info('Posting to EmailAlertPost-Cloud: Email query dimmer data %s: %s ', parameters['deviceid'], dimmerdata)

          # #########################################################
          # Now send out EMAIL using SendGrid if enabled
          # #########################################################
          if series_parameters['alarmmode'] == 'alarmemail' or series_parameters['alarmmode'] == 'alarmemailsms':
  
            if debug_all: log.info('Posting to EmailAlertPost-Cloud: sending out email deviceid= %s', parameters['deviceid'])
            SendEMAILAlert(parameters, alarmresult)

          # #########################################################
          # Now send out SMS using BLOWERIO if enabled
          # #########################################################
          if series_parameters['alarmmode'] == 'alarmsms' or series_parameters['alarmmode'] == 'alarmemailsms':
  
            if debug_all: log.info('Posting to EmailAlertPost-Cloud: sending out sms deviceid= %s', parameters['deviceid'])
            SendSMSAlert(parameters, alarmresult)          

          # ################################################################
          #Finally we will put a alert message in the SQS que for the main app to process using the SSEA00 partition
          # ################################################################
  
          if debug_all: log.info('Posting to EmailAlertPost-Cloud: sending out HelmSmart Alert via SQS que = deviceid=%s', parameters['deviceid'])
          SendHSAlert(alertkey, parameters, alarmresult, sensorValueUnits, switchdata, dimmerdata,timmerdata)




            
          
    except KeyError as e:
        #if debug_all: log.info('process_message: KeyError in EmailAlertPost-Cloud %s:  ', SERIES_KEY1)

        if debug_all: log.info('process_message: KeyError in EmailAlertPost-Cloud %s:  ' % str(e))
        mymessage='KeyError in EmailAlertPost-Cloud'
        return mymessage

    except ValueError as e:
        #if debug_all: log.info('process_message: Value Error in EmailAlertPost-Cloud %s:  ', SERIES_KEY1)

        if debug_all: log.info('process_message: ValueError in EmailAlertPost-Cloud %s:  ' % str(e))
        mymessage='ValueError in EmailAlertPost-Cloud'
        return mymessage

    except TypeError as e:
        #if debug_all: log.info('process_message: TypeError in EmailAlertPost-Cloud %s:  ', SERIES_KEY1)

        if debug_all: log.info('process_message: TypeError in EmailAlertPost-Cloud %s:  ' % str(e))
        mymessage='TypeError in EmailAlertPost-Cloud'
        return mymessage
    
    except NameError as e:
        #if debug_all: log.info('process_message: TypeError in EmailAlertPost-Cloud %s:  ', SERIES_KEY1)

        if debug_all: log.info('process_message: NameError in EmailAlertPost-Cloud %s:  ' % str(e))
        mymessage='NameError in EmailAlertPost-Cloud'
        return mymessage
    
    except UnboundLocalError as e:
        #if debug_all: log.info('process_message: UnboundLocalError in EmailAlertPost-Cloud %s:  ', SERIES_KEY1)

        if debug_all: log.info('process_message: UnboundLocalError in EmailAlertPost-Cloud %s:  ' % str(e))
        mymessage='UnboundLocalError in EmailAlertPost-Cloud'
        return mymessage

    except:
        #if debug_all: log.info('process_message: Error in geting EmailAlertPost-Cloud parameters %s:  ', posttype)
        e = sys.exc_info()[0]

        if debug_all: log.info("Error: %s" % e)
        mymessage='Error in geting Alert Parameters'
        return mymessage
        #pass
    
# ****************************************************************
# end of Main message processor
# *************************************************************************
