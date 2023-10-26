import os
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

# *******************************************************************
# Debug Output defines
# Comment to enable/disable
# ********************************************************************
#debug_all = False
debug_all = True


requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.INFO)

logging.basicConfig(level=logging.INFO)
log = logging


from influxdb.influxdb08 import InfluxDBClient

from influxdb import InfluxDBClient as InfluxDBCloud
from influxdb.client import InfluxDBClientError

import psycopg
from psycopg_pool import ConnectionPool
#db_pool = ThreadedConnectionPool( 1,  **connection_from(os.environ['DATABASE_URL']))
#db_pool = ConnectionPool( 1,  **connection_from(os.environ['DATABASE_URL']))
db_pool = ConnectionPool(os.environ.get('DATABASE_URL'))


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

    if debug_all: log.info('Posting to Web Services %s:%s', posttype, starttime)
    #mymessage='returning from Telemetry post'  
    #return mymessage

    #conn = db_pool.getconn()

    #if debug_all: log.info('Device ID  = ' + records[0][0])
    #deviceid = records[0][0]

    API_KEY = '7be1d82569414dceaa82fd93fadd7940'
    API_SECRET = '0447ec319c3148cb98d96bfc96c787e1'
  
    #client = Client(API_KEY, API_KEY, API_SECRET)

    host = 'pinheads-wedontneedroads-1.c.influxdb.com' 
    port = 8086
    username = 'root'
    password = 'c73d5a8b1b07d17b'
    database = 'pushsmart-final'

    dchost = 'hilldale-670d9ee3.influxcloud.net' 
    dcport = 8086
    dcusername = 'helmsmart'
    dcpassword = 'Salm0n16'
    dcdatabase = 'pushsmart-cloud'

    posttypecloud=None

    #db = influxdb.InfluxDBClient(host, port, username, password, database)
    #db = InfluxDBClient(host, port, username, password, database)
    dbc = InfluxDBCloud(dchost, dcport, dcusername, dcpassword, dcdatabase,  ssl=True)
    
    points={}
    times={}
    timesiso={}

    if posttype == "EmailAlertPost":
        posttypecloud = "EmailAlertPost-Cloud"


# **************************************************************************************
# If Email alert then check values for High/Low alarms and send out email if active
#****************************************************************************************
    try:

        if posttypecloud == "EmailAlertPost-Cloud":
            #if debug_all: log.info('Posting to AlertPosts :')
            log.info('Posting to EmailAlertPost-Cloud %s:', jsondata)

            email_body = ""
            timmer_array = ""
            timmer_json={}
            distance = ""

            
    except KeyError as e:
        #if debug_all: log.info('Telemetrypost: KeyError in EmailAlertPost-Cloud %s:  ', SERIES_KEY1)

        if debug_all: log.info('Telemetrypost: KeyError in EmailAlertPost-Cloud %s:  ' % str(e))
        mymessage='KeyError in EmailAlertPost-Cloud'
        return mymessage

    except ValueError as e:
        #if debug_all: log.info('Telemetrypost: Value Error in EmailAlertPost-Cloud %s:  ', SERIES_KEY1)

        if debug_all: log.info('Telemetrypost: ValueError in EmailAlertPost-Cloud %s:  ' % str(e))
        mymessage='ValueError in EmailAlertPost-Cloud'
        return mymessage

    except TypeError as e:
        #if debug_all: log.info('Telemetrypost: TypeError in EmailAlertPost-Cloud %s:  ', SERIES_KEY1)

        if debug_all: log.info('Telemetrypost: TypeError in EmailAlertPost-Cloud %s:  ' % str(e))
        mymessage='TypeError in EmailAlertPost-Cloud'
        return mymessage
    
    except UnboundLocalError as e:
        #if debug_all: log.info('Telemetrypost: UnboundLocalError in EmailAlertPost-Cloud %s:  ', SERIES_KEY1)

        if debug_all: log.info('Telemetrypost: UnboundLocalError in EmailAlertPost-Cloud %s:  ' % str(e))
        mymessage='UnboundLocalError in EmailAlertPost-Cloud'
        return mymessage

    except:
        #if debug_all: log.info('Telemetrypost: Error in geting EmailAlertPost-Cloud parameters %s:  ', posttype)
        e = sys.exc_info()[0]

        if debug_all: log.info("Error: %s" % e)
        mymessage='Error in geting Alert Parameters'
        return mymessage
        #pass
    
# ****************************************************************
# end of Main message processor
# *************************************************************************
